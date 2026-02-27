import os
from pydub import AudioSegment

def merge_mp3_files(output_folder="output", output_filename="merged_audio.mp3"):
    """
    Une todos los archivos MP3 de una carpeta en un solo archivo MP3
    """
    print("Buscando archivos MP3 en la carpeta output...")
    
    # Obtener todos los archivos MP3
    mp3_files = [f for f in os.listdir(output_folder) if f.endswith('.mp3')]
    
    if not mp3_files:
        print("No se encontraron archivos MP3 en la carpeta output.")
        return
    
    # Ordenar alfabéticamente
    mp3_files.sort()
    
    print(f"Encontrados {len(mp3_files)} archivos MP3:")
    for i, file in enumerate(mp3_files, 1):
        print(f"  {i}. {file}")
    
    print("\nUniendo archivos...")
    
    # Crear el audio combinado
    combined = AudioSegment.empty()
    
    for i, mp3_file in enumerate(mp3_files, 1):
        file_path = os.path.join(output_folder, mp3_file)
        print(f"Procesando ({i}/{len(mp3_files)}): {mp3_file}")
        
        try:
            audio = AudioSegment.from_mp3(file_path)
            combined += audio
        except Exception as e:
            print(f"Error al procesar {mp3_file}: {e}")
    
    # Guardar el archivo combinado
    output_path = os.path.join(output_folder, output_filename)
    print(f"\nGuardando archivo combinado en: {output_path}")
    combined.export(output_path, format="mp3")
    
    print(f"¡Listo! Archivo combinado creado: {output_filename}")
    
    # Mostrar duración total
    duration_seconds = len(combined) / 1000
    duration_minutes = duration_seconds / 60
    print(f"Duración total: {duration_minutes:.2f} minutos ({duration_seconds:.2f} segundos)")

if __name__ == "__main__":
    merge_mp3_files()
