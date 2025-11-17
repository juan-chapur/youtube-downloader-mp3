import subprocess

def main():
    print("Ejecutando gestor para descargar audios y videos...")

    try:
        print("Ejecutando descarga de audios...")
        subprocess.run(["python", "youtube_audio_downloader.py"], check=True)

        print("Ejecutando descarga de videos...")
        subprocess.run(["python", "youtube_video_downloader_720.py"], check=True)

        print("Descargas completadas.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar uno de los scripts: {e}")

if __name__ == "__main__":
    main()