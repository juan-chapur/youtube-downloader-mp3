# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt /app/

# Instalar las dependencias del sistema necesarias para ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Crear los directorios de entrada y salida
RUN mkdir -p /app/input /app/output

# Ejecutar migraciones y colectar archivos estáticos
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput --clear || true

# Exponer el puerto 8000
EXPOSE 8000

# Comando para iniciar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]