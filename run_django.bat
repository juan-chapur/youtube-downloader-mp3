@echo off

REM Navegar al directorio del proyecto
cd C:\desarrollo\youtube-downloader-mp3

REM Activar entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Iniciar servidor Django
python manage.py runserver

pause
