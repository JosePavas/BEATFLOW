import vlc
import time
import os

class Canciones:
    def __init__(self, directory):
        self.directory = directory
    
    def get_mp3_files(self):
        if not os.path.isdir(self.directory):
            print(f"Error: El directorio {self.directory} no existe.")
            return []

        mp3_files = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.mp3'):
                mp3_files.append(os.path.join(self.directory, filename))
        return mp3_files

class Cancion:
    def __init__(self, nombre, artista):
        self.nombre = nombre
        self.artista = artista

    def __str__(self):
        return f"{self.nombre} - {self.artista}"    

class ListaReproduccion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)
        print(f"Canción '{cancion}' agregada a la lista '{self.nombre}'.")

    def eliminar_cancion(self, indice):
        if 0 <= indice < len(self.canciones):
            cancion_eliminada = self.canciones.pop(indice)
            print(f"Canción '{cancion_eliminada}' eliminada de la lista '{self.nombre}'.")
        else:
            print("Índice de canción fuera de rango.")

    def mostrar_lista(self):
        if self.canciones:
            return [str(cancion) for cancion in self.canciones]
        else:
            return []

class BeatFlow:
    def __init__(self):
        self.listas_reproduccion = {}

    def crear_lista_reproduccion(self, nombre_lista):
        if nombre_lista not in self.listas_reproduccion:
            self.listas_reproduccion[nombre_lista] = ListaReproduccion(nombre_lista)
            print(f"Lista de reproducción '{nombre_lista}' creada exitosamente.")
        else:
            print("Ya existe una lista de reproducción con ese nombre.")

    def ver_listas_reproduccion(self):
        return list(self.listas_reproduccion.keys())
    
    def agregar_cancion(self, nombre_lista, cancion):
        if nombre_lista in self.listas_reproduccion:
            self.listas_reproduccion[nombre_lista].agregar_cancion(cancion)
        else:
            print("No existe una lista de reproducción con ese nombre.")

    def eliminar_cancion(self, nombre_lista, indice):
        if nombre_lista in self.listas_reproduccion:
            self.listas_reproduccion[nombre_lista].eliminar_cancion(indice)
        else:
            print("No existe una lista de reproducción con ese nombre.")

    def ver_canciones_lista(self, nombre_lista):
        if nombre_lista in self.listas_reproduccion:
            return self.listas_reproduccion[nombre_lista].mostrar_lista()
        else:
            return None

class Reproductor:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.playlist = []
        self.current_index = 0

    def agregar_cancion_cola(self, cancion):
        self.playlist.append(cancion)

    def reproducir_cancion(self, index):
        if index < len(self.playlist):
            media = self.instance.media_new(self.playlist[index])
            self.player.set_media(media)
            self.player.play()
            self.current_index = index

    def pausar_musica(self):
        self.player.stop()
        
    def reanudar_musica(self):
        self.player.resume()    

    def set_volume(self, volume):
        if 0 <= volume <= 100:
            self.player.audio_set_volume(volume)

    def get_volume(self):
        return self.player.audio_get_volume()