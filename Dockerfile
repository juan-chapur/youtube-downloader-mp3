# Usar una imagen base de Python en Alpine Linux (ligera)
FROM python:3.10-alpine

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Crear los directorios de entrada y salida
RUN mkdir -p /app/input /app/output

# Instalar las dependencias del sistema necesarias para ffmpeg y Python
RUN apk add ffmpeg \
    bash \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev

# Instalar las dependencias de Python
RUN pip install yt-dlp pydub

# Cambiar el comando CMD para ejecutar el gestor
CMD ["python", "run_manager.py"]