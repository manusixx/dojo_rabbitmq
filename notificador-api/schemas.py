from datetime import datetime, timezone
from uuid import uuid4
 
from pydantic import BaseModel, Field
 
 
# evento_id y timestamp tienen default_factory: se generan solos al
# construir el objeto, sin que quien llame a la API tenga que enviarlos.
# El cliente solo necesita enviar 'mensaje'.
#
# El timestamp usa datetime.now(timezone.utc) y no datetime.utcnow(),
# que está deprecado desde Python 3.12 y devuelve una fecha sin zona
# horaria.
class NotificacionEvent(BaseModel):
    evento_id: str = Field(default_factory=lambda: str(uuid4()))
    mensaje: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
