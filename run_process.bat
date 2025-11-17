@echo off

REM Navegar al directorio del proyecto
cd C:\desarrollo\youtube-downloader-mp3

REM Ejecutar el script para llenar los inputs
python populate_inputs.py

REM Ejecutar Docker Compose
powershell -Command "docker-compose up; if ($LASTEXITCODE -ne 0) { docker-compose up --build }"

REM Abrir la carpeta de salida
start "" "C:\desarrollo\youtube-downloader-mp3\output"

REM Cerrar automáticamente la ventana al finalizar
exit