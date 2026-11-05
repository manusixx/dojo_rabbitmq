import os
import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage
from schemas import NotificacionEvent
from storage import guardar_notificacion

# Misma lógica que en el productor: variable de entorno con valor por
# defecto para desarrollo local.
RABBITMQ_URL = os.environ.get(
    'RABBITMQ_URL', 'amqp://notificador:notificador123@localhost:5672/'
)

# Deben coincidir exactamente con lo que declara notificador-api.
EXCHANGE_NAME = 'notificaciones.exchange'
ROUTING_KEY = 'notificacion.creada'

# El nombre de la cola cumple aquí el papel que tenía el group_id en
# Kafka: es lo que identifica a este consumidor ante el broker. Si se
# levantara una segunda instancia de este worker con la MISMA cola,
# RabbitMQ repartiría los mensajes entre ambas en vez de entregarlos dos
# veces.
QUEUE_NAME = 'notificaciones.worker'

async def procesar(mensaje: AbstractIncomingMessage) -> None:
    try:
        # Reconstruir el evento contra el esquema da validación: si llegara
        # un mensaje que no cumple el contrato, falla aquí con un error
        # claro. ValidationError es subclase de ValueError.
        evento = NotificacionEvent.model_validate_json(mensaje.body)
    except ValueError:
        # Un mensaje inválido no mejora si se reintenta: se rechaza sin
        # devolverlo a la cola (requeue=False).
        await mensaje.reject(requeue=False)
        return

    try:
        # timestamp.isoformat() convierte el datetime a texto, porque
        # SQLite no tiene un tipo datetime nativo.
        guardar_notificacion(
            evento.evento_id, evento.mensaje, evento.timestamp.isoformat()
        )
    except Exception:
        # Si falla la persistencia, el mensaje vuelve a la cola para no
        # perderse, y se deja subir el error para que el fallo sea visible.
        await mensaje.nack(requeue=True)
        raise

    # El ack le dice a RabbitMQ que el mensaje ya fue procesado y puede
    # borrarlo de la cola. Va DESPUÉS de persistir: si se confirmara antes
    # y el worker se cayera al guardar, el mensaje se perdería para siempre.
    # Si el worker se cae antes de este punto, el mensaje sigue en la cola
    # y se reentrega.
    await mensaje.ack()
    print(f'Notificación recibida y persistida: {evento}')


async def consumir_notificaciones() -> None:
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    try:
        channel = await connection.channel()
        # prefetch_count=1: RabbitMQ no entrega un mensaje nuevo hasta que
        # el anterior fue confirmado. Sin este límite, el broker enviaría
        # al worker todos los mensajes de golpe.
        await channel.set_qos(prefetch_count=1)

        # Declarar es idempotente, siempre que los parámetros coincidan con
        # los de la cola ya existente (la creada a mano en el Paso 6).
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME, ExchangeType.DIRECT, durable=True
        )
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await queue.bind(exchange, routing_key=ROUTING_KEY)

        # 'async for' mantiene este bucle corriendo indefinidamente,
        # procesando un mensaje a la vez. Por defecto la entrega exige ack
        # manual.
        async with queue.iterator() as mensajes:
            async for mensaje in mensajes:
                await procesar(mensaje)
    finally:
        # Cierre ordenado de la conexión si el bucle se interrumpe (por
        # ejemplo, con Ctrl+C).
        await connection.close()