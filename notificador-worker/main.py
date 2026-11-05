import asyncio
from consumer import consumir_notificaciones
from storage import init_db
 
# A diferencia de notificador-api (que usa uvicorn como punto de entrada),
# este worker no es un servidor web: es un proceso que corre un bucle
# infinito por su cuenta.
# init_db() debe correr ANTES de que el consumidor empiece a recibir
# mensajes: si la tabla no existe todavía y llega un mensaje, el primer
# guardar_notificacion() fallaría.

if __name__ == '__main__':
    init_db()
    try:
        asyncio.run(consumir_notificaciones())
    except KeyboardInterrupt:
        # Sin este bloque, Ctrl+C muestra un traceback completo de asyncio.
        # No es un error real; se captura para que la salida se vea
        # intencional.
        print('Worker detenido.')
