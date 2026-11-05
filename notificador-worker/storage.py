import os
import sqlite3
 
# SQLite es parte de la librería estándar de Python: no agrega ninguna
# dependencia al proyecto y da un archivo de base de datos real y
# consultable.
#
# Los datos persistentes viven bajo data/, separados del código de la
# app. Esto permite montar después (Paso 11) un volumen de Docker solo
# sobre data/, sin tapar el código que se copia al construir la imagen.
DATA_DIR = 'data'
DB_PATH = os.path.join(DATA_DIR, 'notificaciones.db')
 
 
def init_db() -> None:
    # makedirs crea la carpeta data/ si no existe todavía (por ejemplo, la
    # primera vez que el contenedor arranca con un volumen vacío).
    os.makedirs(DATA_DIR, exist_ok=True)
    # CREATE TABLE IF NOT EXISTS permite llamar esta función en cada
    # arranque sin verificar antes si la tabla ya existe.
    with sqlite3.connect(DB_PATH) as conexion:
        conexion.execute(
            '''
            CREATE TABLE IF NOT EXISTS notificaciones (
                evento_id TEXT PRIMARY KEY,
                mensaje TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            '''
        )
 
 
def guardar_notificacion(evento_id: str, mensaje: str, timestamp: str) -> None:
    # INSERT OR IGNORE (en vez de un INSERT normal) es importante: RabbitMQ
    # garantiza entrega 'al menos una vez' cuando se usa ack manual, no
    # 'exactamente una vez'. Si el worker se cae justo después de guardar
    # pero antes de enviar el ack, RabbitMQ reentrega el mismo mensaje al
    # reconectarse. Como evento_id es la clave primaria, el segundo intento
    # de insertar el mismo evento_id se ignora en silencio en vez de fallar
    # o duplicar la fila.
    with sqlite3.connect(DB_PATH) as conexion:
        conexion.execute(
            'INSERT OR IGNORE INTO notificaciones (evento_id, mensaje, timestamp) '
            'VALUES (?, ?, ?)',
            (evento_id, mensaje, timestamp),
        )
