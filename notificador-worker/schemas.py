from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel, Field
 
# Esta clase es una copia de la que está en notificador-api/schemas.py,
# no una importación. Es intencional: en el mundo real estos dos
# servicios viven en repositorios y despliegues separados. Lo que los
# mantiene compatibles es que ambos respeten los mismos nombres de campo
# y tipos, no que reutilicen una clase en común.
class NotificacionEvent(BaseModel):
    evento_id: str = Field(default_factory=lambda: str(uuid4()))
    mensaje: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
