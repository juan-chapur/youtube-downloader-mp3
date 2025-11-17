import os
import subprocess

def descargar_video(link, output_path="/app/output"):
    try:
        print(f"Descargando video de: {link}")
        
        # Descargar el título del video
        result = subprocess.run(
            ["yt-dlp", "--get-title", link],
            capture_output=True,
            text=True,
            check=True
        )
        title = result.stdout.strip().replace(" ", "_").replace("/", "_")  # Reemplazar espacios y caracteres no válidos
        
        # Definir el formato de salida del archivo descargado
        output_template = f"{output_path}/{title}.%(ext)s"  # Guardar con el título del video
        
        # Descargar el archivo usando yt-dlp
        subprocess.run(["yt-dlp", "-f", "best[height<=720]", "-o", output_template, "--restrict-filenames", link], check=True)
        print(f"Descarga completada: {title}")
    except Exception as e:
        print(f"Error al descargar el video: {e}")

if __name__ == "__main__":
    input_file = "/app/input/input.txt"
    output_dir = "/app/output"

    if not os.path.exists(input_file):
        print(f"Archivo de entrada no encontrado: {input_file}")
        exit(1)

    with open(input_file, "r") as file:
        links = [line.strip() for line in file if line.strip()]

    for link in links:
        descargar_video(link, output_dir)