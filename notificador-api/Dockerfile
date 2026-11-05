# Imagen base ligera: 'slim' trae solo lo esencial para correr Python,
# sin las herramientas de compilación de la imagen completa.
FROM python:3.13-slim
 
# Todo lo que sigue se ejecuta dentro de esta carpeta del contenedor.
WORKDIR /app
 
# Se copia primero solo requirements.txt para aprovechar el caché de
# capas de Docker: si el código cambia pero las dependencias no, la capa
# de instalación no se vuelve a ejecutar.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Ahora sí se copia el resto del código.
COPY . .
 
# host 0.0.0.0 (no 127.0.0.1) es obligatorio: dentro de un contenedor,
# 'localhost' solo acepta conexiones del mismo contenedor. Para que Docker
# pueda exponer el puerto hacia afuera, uvicorn debe escuchar en todas las
# interfaces.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
