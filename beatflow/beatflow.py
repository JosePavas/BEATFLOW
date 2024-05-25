import vlc
import time
import os
import sys


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

# Ajustar la ruta del directorio de música
directory = os.path.join(os.path.dirname(__file__), '..', 'music')
print(f"Directorio de música: {directory}")

canciones = Canciones(directory)
mp3_files = canciones.get_mp3_files()
print("Archivos mp3 encontrados:")
for mp3 in mp3_files:
    print(mp3)

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
            print(f"\nLista de reproducción '{self.nombre}':")
            for i, cancion in enumerate(self.canciones):
                print(f"{i+1}. {cancion}")
        else:
            print(f"\nLa lista de reproducción '{self.nombre}' está vacía.")

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
        print("\nListas de reproducción disponibles:")
        for nombre_lista in self.listas_reproduccion:
            print(nombre_lista)
    
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
            self.listas_reproduccion[nombre_lista].mostrar_lista()
        else:
            print("No existe una lista de reproducción con ese nombre.")
    
#class Reproductor:
    #def __init__(self):
       # self.instance = vlc.Instance()
        #self.player = self.instance.media_player_new()
        #self.playlist = []
        #self.current_index = 0
    
    #def agregar_cancion_cola(self, cancion):
        #self.playlist.append(cancion)
    
    #def reproducir_cancion(self, index):
        #if index < len(self.playlist):
            #media = self.instance.media_new(self.playlist[index])
            #self.player.set_media(media)
            #self.player.play()
            #self.current_index = index
            #time.sleep(1)

    #def reproducir_siguiente(self):
        #if self.current_index + 1 < len(self.playlist):
            #self.reproducir_cancion(self.current_index + 1)

    #def reproducir_anterior(self):
        #if self.current_index - 1 >= 0:
            #self.reproducir_cancion(self.current_index - 1)

    #def pausar_musica(self):
        #self.player.stop()

    #def set_volume(self, volume):
        #if 0 <= volume <= 100:
            #self.player.audio_set_volume(volume)
    
    #def get_volume(self):
        #return self.player.audio_get_volume()
    
    #def add_to_queue(self, song):
        #self.agregar_cancion_cola(song)

    #def play_queue(self):
        #while self.current_index < len(self.playlist):
            #self.reproducir_cancion(self.current_index)
            #while self.player.is_playing():
                #time.sleep(1)
            #self.current_index += 1
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

    def set_volume(self, volume):
        if 0 <= volume <= 100:
            self.player.audio_set_volume(volume)

    def get_volume(self):
        return self.player.audio_get_volume()            

