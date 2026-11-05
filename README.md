# Dojo: Notificaciones asíncronas con RabbitMQ

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.13-blue)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-4-orange)

Laboratorio guiado de mensajería asíncrona entre microservicios con FastAPI, Docker y RabbitMQ. Material del curso 750027C Desarrollo de Software III, EISC - Universidad del Valle.

## Descripción

Una API REST recibe notificaciones y las publica en RabbitMQ. Un worker independiente las consume de una cola, confirma cada mensaje (ack) y las guarda en SQLite. Los dos servicios nunca se llaman directamente: solo comparten el contrato del evento y los nombres del exchange, la cola y la routing key.

## Arquitectura

```
Cliente --POST /notificaciones--> notificador-api --publica--> RabbitMQ --entrega--> notificador-worker --> SQLite
                                                           (exchange -> cola)
```

| Componente | Responsabilidad |
| --- | --- |
| notificador-api | Expone `POST /notificaciones`, valida el evento y lo publica en el exchange `notificaciones.exchange` |
| RabbitMQ | Enruta el mensaje por la routing key `notificacion.creada` a la cola durable `notificaciones.worker` |
| notificador-worker | Consume la cola con ack manual y persiste cada evento en SQLite |

## Stack tecnológico

| Capa | Tecnología |
| --- | --- |
| Servicios | Python 3.13, FastAPI, Pydantic |
| Cliente de mensajería | aio-pika |
| Broker | RabbitMQ 4 con consola de administración |
| Persistencia | SQLite |
| Infraestructura | Docker Compose |

## Requisitos previos

- Docker Desktop con Docker Compose v2
- Git
- Python 3.10 o superior (solo para ejecutar los servicios fuera de Docker)
- En Windows, Git Bash

## Inicio rápido

1. Clonar el repositorio:

```bash
git clone https://github.com/manusixx/dojo_rabbitmq.git
cd dojo_rabbitmq
```

2. Levantar los tres servicios:

```bash
docker-compose up -d --build
docker-compose ps
```

3. Publicar una notificación desde http://localhost:8000/docs (Swagger) o con curl:

```bash
curl -X POST http://localhost:8000/notificaciones -H "Content-Type: application/json" -d '{"mensaje": "Hola RabbitMQ"}'
```

4. Consola de RabbitMQ en http://localhost:15672, usuario `notificador` y clave `notificador123` (credenciales de laboratorio; escribirlas a mano, no pegarlas).

## Comandos útiles

```bash
# Logs de cada servicio
docker logs notificador-api
docker logs notificador-worker

# Estado de la cola (pendientes, sin confirmar, consumidores)
docker exec rabbitmq rabbitmqctl list_queues name messages_ready messages_unacknowledged consumers

# Contenido de la base de datos (en Git Bash de Windows se necesita el prefijo)
MSYS_NO_PATHCONV=1 docker exec notificador-worker python -c "import sqlite3; con = sqlite3.connect('/app/data/notificaciones.db'); print(con.execute('SELECT * FROM notificaciones').fetchall())"

# Detener conservando datos / borrando también los volúmenes
docker-compose down
docker-compose down -v
```

## Estructura del repositorio

```
dojo_rabbitmq/
├── .github/
│   └── pull_request_template.md
├── docs/                    # Guía paso a paso del dojo
├── notificador-api/         # API FastAPI (productor)
│   ├── Dockerfile
│   ├── main.py
│   ├── producer.py
│   ├── schemas.py
│   └── requirements.txt
├── notificador-worker/      # Worker (consumidor + SQLite)
│   ├── Dockerfile
│   ├── main.py
│   ├── consumer.py
│   ├── storage.py
│   ├── schemas.py
│   └── requirements.txt
├── docker-compose.yml       # RabbitMQ + API + worker
├── CONTRIBUTING.md
└── README.md
```

## Guía paso a paso

La guía completa del laboratorio, con explicación de cada paso y actividad de reflexión, está en la carpeta `docs/`.
- [Guía en PDF](docs/Dojo_Notificaciones_RabbitMQ_Guia.pdf)

## Flujo de trabajo

Ver `CONTRIBUTING.md` para el detalle completo. Resumen:

1. Trabajar en la rama personal (`mpastrana`).
2. Validar localmente: `docker-compose config -q` y la prueba de extremo a extremo.
3. Push y PR a `develop`.
4. Atender los comentarios y mergear a `develop`.
5. Al cerrar una versión validada, PR de `develop` a `main`.

## Créditos

Dirección de desarrollo: Manuel Alejandro Pastrana Pardo, PhD.
Universidad del Valle, Escuela de Ingeniería de Sistemas y Computación.

## Licencia

MIT, ver `LICENSE`.