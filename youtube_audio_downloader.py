import subprocess
import os
from pydub import AudioSegment

# Configurar la ruta de ffmpeg para pydub
AudioSegment.converter = "/usr/bin/ffmpeg"

def descargar_audio(link):
    try:
        print(f"Descargando audio de: {link}")
        
        # Descargar el título del video
        result = subprocess.run(
            ["yt-dlp", "--get-title", link],
            capture_output=True,
            text=True,
            check=True
        )
        title = result.stdout.strip().replace(" ", "_").replace("/", "_")  # Reemplazar espacios y caracteres no válidos
        
        # Definir el formato de salida del archivo descargado
        output_template = f"/app/output/{title}.%(ext)s"  # Guardar con el título del video
        
        # Descargar el archivo usando yt-dlp
        subprocess.run(["yt-dlp", "-f", "bestaudio", "-o", output_template, "--restrict-filenames", link], check=True)
        print(f"Descarga completada: {title}")
        
        # Nombre del archivo descargado con ruta relativa completa
        downloaded_file = f"/app/output/{title}.webm"  # Ajusta la extensión si es diferente
        
        # Verificar si el archivo existe
        if not os.path.exists(downloaded_file):
            print(f"Archivo no encontrado: {downloaded_file}")
            return
        
        # Convertir el archivo descargado a MP3
        convertir_a_mp3(downloaded_file, title)
    except Exception as e:
        print(f"Error al descargar o convertir el audio: {e}")

def convertir_a_mp3(input_file, title):
    try:
        # Definir el nombre del archivo de salida
        output_file = input_file.replace(".webm", ".mp3")
        
        # Cargar el archivo de audio descargado
        audio = AudioSegment.from_file(input_file)
        
        # Exportar el archivo como MP3
        audio.export(output_file, format="mp3")
        print(f"Archivo convertido a MP3: {output_file}")
        
        # Renombrar el archivo MP3 para reemplazar los guiones bajos con espacios
        renamed_file = output_file.replace("_", " ")
        os.rename(output_file, renamed_file)
        print(f"Archivo renombrado a: {renamed_file}")
        
        # Eliminar el archivo original .webm
        os.remove(input_file)
        print(f"Archivo .webm eliminado: {input_file}")
    except Exception as e:
        print(f"Error al convertir el archivo a MP3: {e}")

if __name__ == "__main__":
    input_file = "/app/input/input_audios.txt"  # Ruta al archivo de texto con enlaces
    if not os.path.exists(input_file):
        print(f"Archivo de entrada no encontrado: {input_file}")
        exit(1)
    
    with open(input_file, "r") as file:
        links = file.readlines()
    
    for link in links:
        link = link.strip()
        if link:
            descargar_audio(link)