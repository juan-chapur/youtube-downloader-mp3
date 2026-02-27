@echo off
setlocal enabledelayedexpansion
echo ========================================
echo  YouTube Downloader - Django Web App
echo ========================================
echo.

REM Navegar al directorio del proyecto
cd C:\desarrollo\youtube-downloader-mp3

REM Obtener y mostrar la IP local usando PowerShell
echo Obteniendo direccion IP local...
for /f "delims=" %%a in ('powershell -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like '192.168.*' -and $_.InterfaceAlias -like '*Wi-Fi*'}).IPAddress"') do set "IP=%%a"

REM Si no encuentra WiFi específicamente, buscar cualquier IP 192.168.x.x
if "%IP%"=="" (
    for /f "delims=" %%a in ('powershell -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like '192.168.*'} | Select-Object -First 1).IPAddress"') do set "IP=%%a"
)

REM Si aún no hay IP, usar localhost
if "%IP%"=="" set "IP=localhost"

echo.
echo ================================================
echo  SERVIDOR INICIADO
echo ================================================
echo  Accede desde este dispositivo:
echo    http://localhost:8000
echo.
echo  Accede desde otro dispositivo (celular/tablet):
echo    http://%IP%:8000
echo ================================================
echo.

REM Abrir el navegador inmediatamente
echo Abriendo navegador...
start "" "http://localhost:8000"
timeout /t 2 /nobreak >nul
echo.

REM Verificar si Docker está corriendo
echo Verificando Docker...
powershell -Command "if (-not (Get-Process docker -ErrorAction SilentlyContinue)) { Write-Host 'Iniciando Docker Desktop...'; Start-Process 'Docker Desktop'; Start-Sleep -Seconds 10 }"
echo.

REM Ejecutar Docker Compose
echo Iniciando aplicacion web...
echo.
powershell -Command "docker-compose up; if ($LASTEXITCODE -ne 0) { Write-Host 'Construyendo imagen...'; docker-compose up --build }"