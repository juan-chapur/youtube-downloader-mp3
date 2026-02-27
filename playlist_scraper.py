import yt_dlp

def scrape_playlist(playlist_url):
    """
    Extrae todos los links de videos de una playlist de YouTube
    y los guarda en links_scrapeados.txt
    """
    print(f"Scrapeando playlist: {playlist_url}")
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Solo extrae URLs sin descargar
        'force_generic_extractor': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' not in info:
                print("No se encontraron videos en la playlist.")
                return
            
            # Extraer todos los links
            video_urls = []
            for entry in info['entries']:
                if entry:
                    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    video_urls.append(video_url)
            
            # Guardar en archivo
            with open("links_scrapeados.txt", "w", encoding="utf-8") as f:
                for url in video_urls:
                    f.write(url + "\n")
            
            print(f"Se scrapearon {len(video_urls)} videos de la playlist.")
            print(f"Links guardados en: links_scrapeados.txt")
            
    except Exception as e:
        print(f"Error al scrapear la playlist: {e}")

if __name__ == "__main__":
    # Pedir el link de la playlist al usuario
    playlist_url = input("Ingrese el link de la playlist de YouTube: ")
    scrape_playlist(playlist_url)
