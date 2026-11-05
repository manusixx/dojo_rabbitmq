from contextlib import asynccontextmanager
from fastapi import FastAPI
from producer import publish_notificacion, start_producer, stop_producer
from schemas import NotificacionEvent

 
# El lifespan es el código que corre antes de que la app empiece a recibir
# requests y después de que termine de recibirlas. Se usa para abrir y
# cerrar la conexión con RabbitMQ una sola vez.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_producer()
    yield
    await stop_producer()
 
app = FastAPI(title='Notificador API', lifespan=lifespan)
 
@app.get('/health')
def health():
    return {'status': 'UP', 'service': 'notificador-api'}

# response_model le dice a FastAPI qué forma tiene la respuesta, y por eso
# Swagger sabe mostrarla. Como el parámetro 'evento' está tipado con
# NotificacionEvent, FastAPI valida el body contra ese esquema antes de
# ejecutar el código de la función.
@app.post('/notificaciones', response_model=NotificacionEvent)
async def crear_notificacion(evento: NotificacionEvent) -> NotificacionEvent:
    # El cliente solo necesita enviar {'mensaje': '...'}. Como evento_id y
    # timestamp tienen default_factory, Pydantic los genera al construir
    # el objeto, aunque el cliente nunca los haya enviado.
    #
    # model_dump(mode='json') convierte el objeto a un diccionario donde el
    # timestamp (un datetime de Python) queda como string ISO 8601. Sin
    # mode='json', json.dumps (en producer.py) fallaría, porque no sabe
    # convertir un datetime por sí solo.
    await publish_notificacion(evento.model_dump(mode='json'))
 
    # Se devuelve el mismo evento publicado, para que quien llamó al
    # endpoint vea el evento_id y el timestamp generados en el servidor.
    return evento
