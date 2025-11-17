def populate_inputs():
    print("Llenando archivos de entrada para audios y videos...")

    # Llenar input de audios
    with open("input/input_audios.txt", "w") as audio_file:
        print("Ingrese links de audios (Enter para terminar):")
        while True:
            link = input("Link de audio: ")
            if link.lower() == "":
                break
            audio_file.write(link + "\n")

    # Llenar input de videos
    with open("input/input_videos.txt", "w") as video_file:
        print("Ingrese links de videos (Enter para terminar):")
        while True:
            link = input("Link de video: ")
            if link.lower() == "":
                break
            video_file.write(link + "\n")

    print("Archivos de entrada llenados correctamente.")

if __name__ == "__main__":
    populate_inputs()