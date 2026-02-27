import os
import yt_dlp
from pydub import AudioSegment
from datetime import datetime
import re


def download_audio(url, output_dir='output'):
    """Descarga audio de YouTube"""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Cambiar extensión a mp3
            filename = filename.rsplit('.', 1)[0] + '.mp3'
            return filename
    except Exception as e:
        print(f"Error descargando audio: {e}")
        return None


def download_video(url, output_dir='output'):
    """Descarga video de YouTube en 720p"""
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Asegurar que tenga extensión mp4
            if not filename.endswith('.mp4'):
                filename = filename.rsplit('.', 1)[0] + '.mp4'
            return filename
    except Exception as e:
        print(f"Error descargando video: {e}")
        return None


def merge_audio_files(file_paths, output_dir='output'):
    """Une múltiples archivos MP3 en uno solo"""
    try:
        combined = AudioSegment.empty()
        
        for file_path in file_paths:
            audio = AudioSegment.from_mp3(file_path)
            combined += audio
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"merged_audio_{timestamp}.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        combined.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        raise Exception(f"Error al unir audios: {e}")


def merge_video_files(file_paths, output_dir='output'):
    """Une múltiples archivos MP4 usando FFmpeg"""
    try:
        import subprocess
        
        # Crear archivo de lista temporal
        list_file = os.path.join(output_dir, 'merge_list.txt')
        with open(list_file, 'w', encoding='utf-8') as f:
            for file_path in file_paths:
                # Usar path absoluto y escapar para FFmpeg
                abs_path = os.path.abspath(file_path)
                # En Windows, convertir backslashes a forward slashes
                abs_path = abs_path.replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"merged_video_{timestamp}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"Uniendo {len(file_paths)} videos...")
        
        # Intentar primero con copy (más rápido)
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file,
            '-c', 'copy',
            '-y',  # Sobrescribir si existe
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Si falla con copy, intentar con re-encoding
        if result.returncode != 0:
            print("Falló con -c copy, intentando con re-encoding...")
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-y',
                output_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Limpiar archivo temporal
        if os.path.exists(list_file):
            os.remove(list_file)
        
        print(f"Videos unidos exitosamente: {output_filename}")
        return output_path
    except subprocess.CalledProcessError as e:
        error_msg = f"Error FFmpeg: {e.stderr if hasattr(e, 'stderr') else str(e)}"
        print(error_msg)
        raise Exception(error_msg)
    except Exception as e:
        print(f"Error general al unir videos: {e}")
        raise Exception(f"Error al unir videos: {e}")


def is_playlist(url):
    """Detecta si una URL es una playlist de YouTube"""
    playlist_patterns = [
        r'[?&]list=',
        r'/playlist\?',
    ]
    return any(re.search(pattern, url) for pattern in playlist_patterns)


def expand_playlist(url):
    """
    Extrae todos los links de videos de una playlist de YouTube
    Retorna una lista de URLs de videos
    """
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,  # Solo extrae URLs sin descargar
            'force_generic_extractor': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' not in info:
                print(f"No se encontraron videos en la playlist: {url}")
                return []
            
            # Extraer todos los links
            video_urls = []
            for entry in info['entries']:
                if entry and 'id' in entry:
                    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    video_urls.append(video_url)
            
            print(f"Se encontraron {len(video_urls)} videos en la playlist")
            return video_urls
            
    except Exception as e:
        print(f"Error al expandir playlist: {e}")
        return []


def process_links(links):
    """
    Procesa una lista de links, expandiendo las playlists automáticamente
    Retorna una lista de URLs de videos individuales
    """
    processed_links = []
    
    for link in links:
        if is_playlist(link):
            print(f"Detectada playlist, expandiendo: {link}")
            playlist_videos = expand_playlist(link)
            processed_links.extend(playlist_videos)
        else:
            processed_links.append(link)
    
    return processed_links
