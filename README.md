# YouTube Audio Downloader

Este proyecto permite descargar audios de videos de YouTube en formato `.mp3`.



## Características

- Lee los enlaces de un archivo de texto (`input.txt`) ubicado en una carpeta `input`.
- Guarda los archivos `.mp3` en una carpeta `output`.



## Requisitos

- **Docker** y **Docker Compose** instalados en tu sistema.
- Una conexión a internet para descargar los videos.



## Configuración

### 1. Clonar el repositorio

Clona este repositorio en tu máquina local:
```bash
git clone https://github.com/juan-chapur/youtube-downloader-mp3.git
cd youtube-downloader-mp3
```

### 2. Agregar enlaces de YouTube

En la carpeta `input`, crea un archivo llamado `input.txt` y agrega los enlaces de YouTube, uno por línea. Por ejemplo:
```txt
https://www.youtube.com/watch?v=fYxYe2Ug2os
https://www.youtube.com/watch?v=Ad5DvbHMHTo
```

## Cómo compilar

Para compilar el proyecto, usa Docker Compose para construir la imagen del contenedor:
```bash
docker-compose build
```

Esto descargará las dependencias necesarias y configurará el entorno para ejecutar el proyecto.



## Cómo ejecutar

Una vez compilado, ejecuta el contenedor con el siguiente comando:
```bash
docker-compose up
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