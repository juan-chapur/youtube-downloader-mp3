@echo off
echo ========================================
echo  YouTube Downloader - Setup Inicial
echo ========================================
echo.

REM Navegar al directorio del proyecto
cd C:\desarrollo\youtube-downloader-mp3

echo [1/4] Creando entorno virtual...
python -m venv venv
echo.

echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
echo.

echo [3/4] Instalando dependencias...
pip install -r requirements.txt
echo.

echo [4/4] Ejecutando migraciones de Django...
python manage.py migrate
echo.

echo ========================================
echo  Setup completado exitosamente!
echo ========================================
echo.
echo Para iniciar la aplicacion web, ejecuta:
echo   run_django.bat
echo.

pause
