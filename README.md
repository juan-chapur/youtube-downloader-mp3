# YouTube Downloader - Web Application

Este proyecto permite descargar audios y videos de YouTube a través de una interfaz web moderna con diseño oscuro.

## Características

- 🎨 Interfaz web moderna con diseño oscuro
- 🎵 Descarga de audios en formato MP3
- 🎥 Descarga de videos en formato MP4 (720p)
- 📦 Opción para unir múltiples archivos en uno solo (mejorado con re-encoding automático)
- 📋 Soporte para múltiples links simultáneos
- 🎼 **Detección automática de playlists** - Pega un link de playlist y descargará todos los videos
- 📊 Barra de progreso en tiempo real
-  **Descarga directa desde el navegador** - Botones de descarga al finalizar para guardar donde quieras
- 🌐 **Acceso desde red local** - Usa desde tu celular o tablet en la misma red WiFi
- 🐳 Soporte completo para Docker



## Requisitos

### Para usar con Docker (Recomendado):
- **Docker Desktop** instalado
- Conexión a internet

### Para usar sin Docker:
- **Python 3.10+**
- **FFmpeg** instalado en el sistema
- Conexión a internet



## Inicio Rápido con Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone https://github.com/juan-chapur/youtube-downloader-mp3.git
cd youtube-downloader-mp3
```

2. Ejecuta el script automatizado:
```bash
.\run_process.bat
```

Este script automáticamente:
- ✅ Verifica si Docker está corriendo (lo inicia si es necesario)
- ✅ **Muestra la dirección IP local** para acceder desde otros dispositivos
- ✅ **Abre el navegador inmediatamente**
- ✅ Construye la imagen Docker si no existe
- ✅ Levanta la aplicación web
- ✅ Permite acceso desde celulares/tablets en la misma red WiFi

3. Usa la interfaz web para:
   - Seleccionar tipo de descarga (Audio/Video)
   - Pegar uno o varios links de YouTube (videos individuales o playlists completas)
   - **Las playlists se detectan y expanden automáticamente** - no necesitas extraer los links manualmente
   - Opcionalmente unir todos los archivos en uno solo
   - Ver el progreso en tiempo real
   - **Descargar archivos directamente** - Al finalizar aparecerán botones de descarga para guardar los archivos donde quieras en tu dispositivo

### 💾 Descarga de archivos:

Después de completar las descargas, la interfaz mostrará:
- ✅ Lista de todos los archivos descargados
- 📊 Tamaño de cada archivo en MB
- ⬇️ Botón de descarga individual para cada archivo
- 📁 Ubicación donde se guardaron en el servidor

Esto te permite:
- **Descargar archivos directamente desde el navegador** a tu dispositivo (PC, celular, tablet)
- **Elegir dónde guardarlos** usando el diálogo de descarga de tu navegador
- Los archivos permanecen almacenados en el servidor para descargas futuras
### 📱 Acceso desde celular/tablet:

Cuando ejecutes `run_process.bat`, verás algo como:

```
================================================
 SERVIDOR INICIADO
================================================
 Accede desde este dispositivo:
   http://localhost:8000

 Accede desde otro dispositivo (celular/tablet):
   http://192.168.1.100:8000
================================================
```

Desde tu celular conectado a la misma red WiFi, abre el navegador y usa la dirección IP mostrada.

Los archivos descargados aparecerán en la carpeta especificada (por defecto `output/`).



## Instalación Manual (Sin Docker)

### 1. Clonar el repositorio

```bash
git clone https://github.com/juan-chapur/youtube-downloader-mp3.git
cd youtube-downloader-mp3
```

### 2. Ejecutar setup automático

```bash
.\setup.bat
```

O manualmente:

```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
pip install -r requirements.txt
python manage.py migrate
```

### 3. Iniciar servidor

```bash
.\run_django.bat
```

O manualmente:
```bash
python manage.py runserver
```

Luego abre tu navegador en `http://localhost:8000`



## Uso Avanzado

### Scripts de Consola (Modo Clásico)

Estos scripts funcionan directamente sin la interfaz web:

#### Descarga individual de audios:
```bash
python youtube_audio_downloader.py
```

#### Descarga individual de videos:
```bash
python youtube_video_downloader_720.py
```

#### Scrapear playlist:
```bash
python playlist_scraper.py
```
Scrapea todos los links de una playlist y los guarda en `links_scrapeados.txt`.

#### Unir archivos MP3:
```bash
python merge_mp3.py
```
Une todos los archivos MP3 de la carpeta `output/` en un solo archivo.

#### Gestor completo:
```bash
python run_manager.py
```
Ejecuta secuencialmente los scripts de descarga de audio y video.

#### Llenar inputs interactivamente:
```bash
python populate_inputs.py
```
Te permite ingresar links interactivamente para llenar los archivos de entrada.



## Comandos Docker Manuales

Si prefieres usar Docker manualmente en lugar del script automatizado:

#### Compilar imagen:
```bash
docker-compose build
```

#### Ejecutar aplicación web:
```bash
docker-compose up
```

Luego abre tu navegador en `http://localhost:8000`

#### Detener contenedores:
```bash
docker-compose down
```

El contenedor leerá los enlaces desde el archivo `input/input.txt`, descargará los audios en formato `.webm`, los convertirá a `.mp3`, y los guardará en la carpeta `output`.



## Resultados

- Los archivos `.mp3` se guardarán en la carpeta `output` con los nombres basados en los títulos de los videos.



## Estructura del proyecto

```
youtube-audio-downloader/
├── Dockerfile
├── docker-compose.yml
├── youtube_audio_downloader.py
├── input/
│   └── input.txt
├── output/
└── README.md
```



## Notas

- Asegúrate de que los enlaces en `input.txt` sean válidos y accesibles.
- Si necesitas ajustar el formato de salida o la calidad del audio, puedes modificar las opciones de `yt-dlp` en el archivo `youtube_audio_downloader.py`.