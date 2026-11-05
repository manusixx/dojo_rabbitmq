FROM python:3.13-slim
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
# Este servicio no expone ningún puerto (no es un servidor web), así que
# el CMD simplemente ejecuta el script que arranca el bucle del consumidor.
CMD ["python", "main.py"]
