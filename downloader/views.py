from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
import os
import threading
import uuid
import mimetypes
from .utils import download_audio, download_video, merge_audio_files, merge_video_files, process_links

# Almacenamiento en memoria de tareas
download_tasks = {}


def index(request):
    """Vista principal con el formulario"""
    return render(request, 'downloader/index.html')


@csrf_exempt
def download(request):
    """Procesa la solicitud de descarga"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        download_type = data.get('type')  # 'audio' o 'video'
        links = data.get('links', [])
        merge = data.get('merge', False)
        output_folder = data.get('output_folder', 'output')  # Carpeta de salida personalizada
        
        if not links:
            return JsonResponse({'error': 'No se proporcionaron links'}, status=400)
        
        if download_type not in ['audio', 'video']:
            return JsonResponse({'error': 'Tipo de descarga no válido'}, status=400)
        
        # Crear ID único para la tarea
        task_id = str(uuid.uuid4())
        
        # Expandir playlists automáticamente
        expanded_links = process_links(links)
        
        if not expanded_links:
            return JsonResponse({'error': 'No se pudieron procesar los links'}, status=400)
        
        # Inicializar estado de la tarea
        download_tasks[task_id] = {
            'status': 'processing',
            'progress': 0,
            'total': len(expanded_links),
            'current': 0,
            'files': [],
            'error': None,
            'merged_file': None,
            'playlist_expanded': len(expanded_links) > len(links),
            'output_folder': output_folder
        }
        
        # Ejecutar descarga en un hilo separado
        thread = threading.Thread(
            target=process_download,
            args=(task_id, download_type, expanded_links, merge, output_folder)
        )
        thread.start()
        
        return JsonResponse({
            'task_id': task_id,
            'message': 'Descarga iniciada'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def download_status(request, task_id):
    """Obtiene el estado de una descarga"""
    if task_id not in download_tasks:
        return JsonResponse({'error': 'Tarea no encontrada'}, status=404)
    
    return JsonResponse(download_tasks[task_id])


def process_download(task_id, download_type, links, merge, output_dir='output'):
    """Procesa la descarga en segundo plano"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        downloaded_files = []
        
        for i, link in enumerate(links):
            download_tasks[task_id]['current'] = i + 1
            download_tasks[task_id]['progress'] = int((i + 1) / len(links) * 100)
            
            try:
                if download_type == 'audio':
                    file_path = download_audio(link, output_dir)
                else:
                    file_path = download_video(link, output_dir)
                
                if file_path:
                    downloaded_files.append(file_path)
                    download_tasks[task_id]['files'].append(os.path.basename(file_path))
            except Exception as e:
                print(f"Error descargando {link}: {e}")
        
        # Si se deben unir los archivos
        if merge and len(downloaded_files) > 1:
            download_tasks[task_id]['status'] = 'merging'
            try:
                if download_type == 'audio':
                    merged_file = merge_audio_files(downloaded_files, output_dir)
                else:
                    merged_file = merge_video_files(downloaded_files, output_dir)
                
                download_tasks[task_id]['merged_file'] = os.path.basename(merged_file)
            except Exception as e:
                download_tasks[task_id]['error'] = f"Error al unir archivos: {str(e)}"
        
        download_tasks[task_id]['status'] = 'completed'
        download_tasks[task_id]['progress'] = 100
        
    except Exception as e:
        download_tasks[task_id]['status'] = 'error'
        download_tasks[task_id]['error'] = str(e)


def list_files(request):
    """Lista todos los archivos disponibles para descarga"""
    output_folder = request.GET.get('folder', 'output')
    
    try:
        files = []
        if os.path.exists(output_folder):
            for filename in os.listdir(output_folder):
                filepath = os.path.join(output_folder, filename)
                if os.path.isfile(filepath) and (filename.endswith('.mp3') or filename.endswith('.mp4')):
                    size = os.path.getsize(filepath)
                    size_mb = round(size / (1024 * 1024), 2)
                    files.append({
                        'name': filename,
                        'size': size_mb,
                        'folder': output_folder
                    })
        
        return JsonResponse({'files': files})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def download_file(request, filename):
    """Descarga un archivo específico"""
    folder = request.GET.get('folder', 'output')
    file_path = os.path.join(folder, filename)
    
    if not os.path.exists(file_path):
        raise Http404("Archivo no encontrado")
    
    # Determinar el tipo MIME
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    # Abrir y retornar el archivo
    response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
