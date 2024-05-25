import vlc
import os
import threading
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from BEATFLOW.model.beatflow import *

class ReproductorMusica:
    def __init__(self, root):
        self.root = root
        self.root.title("Beatflow Reproductor de Música")
        self.root.geometry("400x300")

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.playlist = []
        self.current_index = 0

        self.is_playing = False

        # Inicializar BeatFlow
        self.beatflow = BeatFlow()

        # Botones de UI
        self.boton_cargar = tk.Button(self.root, text="Cargar", command=self.cargar_musica)
        self.boton_cargar.pack()

        self.boton_reproducir = tk.Button(self.root, text="Reproducir", command=self.reproducir_musica)
        self.boton_reproducir.pack()

        self.boton_pausar = tk.Button(self.root, text="Pausar", command=self.pausar_musica)
        self.boton_pausar.pack()

        self.control_volumen = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.ajustar_volumen)
        self.control_volumen.set(50)
        self.control_volumen.pack()

        # Botones y eventos asociados a BeatFlow
        self.boton_crear_lista = tk.Button(self.root, text="Crear Lista de Reproducción", command=self.crear_lista)
        self.boton_crear_lista.pack()

        self.boton_ver_listas = tk.Button(self.root, text="Ver Listas de Reproducción", command=self.ver_listas)
        self.boton_ver_listas.pack()

        self.boton_ver_canciones_lista = tk.Button(self.root, text="Ver Canciones de Lista de Reproducción", command=self.ver_canciones_lista)
        self.boton_ver_canciones_lista.pack()

        self.boton_agregar_cancion_lista = tk.Button(self.root, text="Agregar Canción a Lista de Reproducción", command=self.agregar_cancion_lista)
        self.boton_agregar_cancion_lista.pack()

        self.boton_eliminar_cancion_lista = tk.Button(self.root, text="Eliminar Canción de Lista de Reproducción", command=self.eliminar_cancion_lista)
        self.boton_eliminar_cancion_lista.pack()

    def cargar_musica(self):
        directorio = filedialog.askdirectory()
        if directorio:
            self.playlist = self.obtener_archivos_mp3(directorio)
            print("Cargando canciones:", self.playlist)

    def obtener_archivos_mp3(self, directorio):
        archivos_mp3 = [os.path.join(directorio, f) for f in os.listdir(directorio) if f.endswith('.mp3')]
        return archivos_mp3

    def reproducir_musica(self):
        if not self.is_playing and self.playlist:
            self.is_playing = True
            threading.Thread(target=self.reproducir_cola).start()

    def reproducir_cola(self):
        while self.current_index < len(self.playlist) and self.is_playing:
            self.reproducir_cancion(self.current_index)
            while self.player.is_playing():
                time.sleep(1)
            self.current_index += 1
        self.is_playing = False

    def reproducir_cancion(self, index):
        media = self.instance.media_new(self.playlist[index])
        self.player.set_media(media)
        self.player.play()
        time.sleep(1)

    def pausar_musica(self):
        self.is_playing = False
        self.player.stop()

    def ajustar_volumen(self, volumen):
        self.player.audio_set_volume(int(volumen))

    # Métodos para interactuar con BeatFlow
    def crear_lista(self):
        nombre = simpledialog.askstring("Crear Lista de Reproducción", "Ingrese el nombre de la nueva lista de reproducción:")
        if nombre:
            self.beatflow.crear_lista_reproduccion(nombre)

    def ver_listas(self):
        listas = self.beatflow.ver_listas_reproduccion()
        if isinstance(listas, list):  # Verifica que se devuelve una lista
            listas_str = "\n".join(listas)
            messagebox.showinfo("Listas de Reproducción", listas_str)
        else:
            messagebox.showerror("Error", "No se pudieron obtener las listas de reproducción.")

    def ver_canciones_lista(self):
        nombre = simpledialog.askstring("Ver Canciones de Lista de Reproducción", "Ingrese el nombre de la lista de reproducción:")
        if nombre:
            canciones = self.beatflow.ver_canciones_lista(nombre)
            if isinstance(canciones, list):  # Verifica que se devuelve una lista
                canciones_str = "\n".join(canciones)
                messagebox.showinfo("Canciones en " + nombre, canciones_str)
            else:
                messagebox.showerror("Error", "No se pudieron obtener las canciones de la lista de reproducción.")

    def agregar_cancion_lista(self):
        nombre_lista = simpledialog.askstring("Agregar Canción a Lista de Reproducción", "Ingrese el nombre de la lista de reproducción:")
        if nombre_lista:
            nombre_cancion = simpledialog.askstring("Agregar Canción a Lista de Reproducción", "Ingrese el nombre de la canción:")
            nombre_artista = simpledialog.askstring("Agregar Canción a Lista de Reproducción", "Ingrese el nombre del artista:")
            if nombre_cancion and nombre_artista:
                cancion = Cancion(nombre_cancion, nombre_artista)
                self.beatflow.agregar_cancion(nombre_lista, cancion)

    def eliminar_cancion_lista(self):
        nombre_lista = simpledialog.askstring("Eliminar Canción de Lista de Reproducción", "Ingrese el nombre de la lista de reproducción:")
        if nombre_lista:
            nombre_cancion = simpledialog.askstring("Eliminar Canción de Lista de Reproducción", "Ingrese el nombre de la canción:")
            nombre_artista = simpledialog.askstring("Eliminar Canción de Reproducción", "Ingrese el nombre del artista:")
            if nombre_cancion and nombre_artista:
                canciones = self.beatflow.ver_canciones_lista(nombre_lista)
                cancion_str = f"{nombre_cancion} - {nombre_artista}"
                if canciones and cancion_str in canciones:
                    indice = canciones.index(cancion_str)
                    self.beatflow.eliminar_cancion(nombre_lista, indice)
                else:
                    messagebox.showerror("Error", "Canción no encontrada en la lista de reproducción.")