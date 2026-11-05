import json
import os
import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message
from aio_pika.abc import AbstractExchange, AbstractRobustConnection
 
# Se lee de variable de entorno con un valor por defecto para desarrollo
# local. Al dockerizar (Paso 10), 'localhost' cambiará a 'rabbitmq' (el
# nombre del servicio dentro de la red de Docker) y este archivo no se
# toca: solo la variable de entorno en el compose.
RABBITMQ_URL = os.environ.get(
    'RABBITMQ_URL', 'amqp://notificador:notificador123@localhost:5672/'
)
 
# Nombres que el worker también debe conocer. Son parte del contrato, igual
# que el esquema del evento.
EXCHANGE_NAME = 'notificaciones.exchange'
ROUTING_KEY = 'notificacion.creada'
 
# La conexión y el exchange se crean una sola vez y se reutilizan durante
# toda la vida del proceso. Abrir una conexión por cada request sería
# costoso e innecesario.
connection: AbstractRobustConnection | None = None
exchange: AbstractExchange | None = None
 
 
async def start_producer() -> None:
    """Abre la conexión con RabbitMQ y declara el exchange.
 
    Se llama una sola vez, en el lifespan de FastAPI (ver main.py). Si
    RabbitMQ no está disponible en este punto, connect_robust lanza una
    excepción aquí mismo: este es el checkpoint donde se detecta si el
    contenedor no está corriendo o no es alcanzable.
    """
    global connection, exchange
    # connect_robust reconecta solo si la conexión se cae después de haberse
    # establecido.
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    # Con la configuración por defecto, el canal usa publisher confirms:
    # publish() espera la confirmación del broker antes de retornar.
    channel = await connection.channel()
    # Declarar es idempotente: si el exchange ya existe con los mismos
    # parámetros, no pasa nada. durable=True hace que sobreviva a un
    # reinicio del broker.
    exchange = await channel.declare_exchange(
        EXCHANGE_NAME, ExchangeType.DIRECT, durable=True
    )
 
 
async def stop_producer() -> None:
    """Cierra la conexión limpiamente al apagar la aplicación."""
    if connection is not None:
        await connection.close()
 
 
async def publish_notificacion(evento: dict) -> None:
    """Publica un evento en el exchange de notificaciones."""
    if exchange is None:
        raise RuntimeError('El productor de RabbitMQ no ha sido inicializado.')
 
    mensaje = Message(
        # RabbitMQ transporta bytes, no objetos Python: dict -> JSON -> bytes.
        body=json.dumps(evento).encode('utf-8'),
        content_type='application/json',
        # PERSISTENT hace que el broker escriba el mensaje en disco. Junto
        # con una cola durable, el mensaje sobrevive a un reinicio de
        # RabbitMQ. Sin esto, el mensaje solo vive en memoria.
        delivery_mode=DeliveryMode.PERSISTENT,
        message_id=evento['evento_id'],
    )
    await exchange.publish(mensaje, routing_key=ROUTING_KEY)
