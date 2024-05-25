import sys
import os
import vlc
import tkinter
import threading
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import time

# Asegúrate de que el directorio que contiene el módulo BEATFLOW esté en el PYTHONPATH
sys.path.append(os.path.abspath("C:/Users/samue/Downloads/BEATFLOW-main/BEATFLOW-main/BEATFLOW"))

# Importa después de agregar al PYTHONPATH
from model.beatflow import *

class ReproductorMusica:
    def __init__(self, root):
        self.root = root
        self.root.title("Beatflow Reproductor de Música")
        self.root.geometry("600x400")

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.playlist = []
        self.queue = []
        self.current_index = 0

        self.is_playing = False

        # Inicializar BeatFlow
        self.beatflow = BeatFlow()

        # Configuración de la interfaz gráfica usando grid
        self.setup_ui()

    def setup_ui(self):
        # Configuración de botones y controles
        self.boton_cargar = tk.Button(self.root, text="Cargar", command=self.cargar_musica)
        self.boton_reproducir = tk.Button(self.root, text="Reproducir", command=self.reproducir_musica)
        self.boton_pausar = tk.Button(self.root, text="Pausar", command=self.pausar_musica)
        self.boton_siguiente = tk.Button(self.root, text="Siguiente", command=self.siguiente_cancion)
        self.boton_anterior = tk.Button(self.root, text="Anterior", command=self.anterior_cancion)
        self.boton_agregar_a_cola = tk.Button(self.root, text="Agregar a Cola", command=self.agregar_a_cola)
        self.boton_ver_cola = tk.Button(self.root, text="Ver Cola de Reproducción", command=self.ver_cola)
        self.boton_reproducir_cola = tk.Button(self.root, text="Reproducir Cola de Reproducción", command=self.reproducir_cola)
        self.control_volumen = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.ajustar_volumen)
        self.control_volumen.set(50)
        
        self.boton_crear_lista = tk.Button(self.root, text="Crear Lista de Reproducción", command=self.crear_lista)
        self.boton_ver_listas = tk.Button(self.root, text="Ver Listas de Reproducción", command=self.ver_listas)
        self.boton_ver_canciones_lista = tk.Button(self.root, text="Ver Canciones de Lista de Reproducción", command=self.ver_canciones_lista)
        self.boton_agregar_cancion_lista = tk.Button(self.root, text="Agregar Canción a Lista de Reproducción", command=self.agregar_cancion_lista)
        self.boton_eliminar_cancion_lista = tk.Button(self.root, text="Eliminar Canción de Lista de Reproducción", command=self.eliminar_cancion_lista)
        self.boton_agregar_cancion = tk.Button(self.root, text="Agregar Canción a Reproductor", command=self.agregar_cancion)
        self.boton_reproducir_lista = tk.Button(self.root, text="Reproducir Lista de Reproducción", command=self.reproducir_lista)

        # Posicionamiento de los widgets en una cuadrícula
        self.boton_cargar.grid(row=0, column=0, padx=5, pady=5)
        self.boton_anterior.grid(row=0, column=1, padx=5, pady=5)
        self.boton_reproducir.grid(row=0, column=2, padx=5, pady=5)
        self.boton_pausar.grid(row=0, column=3, padx=5, pady=5)
        self.boton_siguiente.grid(row=0, column=4, padx=5, pady=5)
        self.control_volumen.grid(row=1, column=0, columnspan=5, sticky="ew", padx=5, pady=5)
        
        self.boton_agregar_a_cola.grid(row=2, column=0, padx=5, pady=5)
        self.boton_ver_cola.grid(row=2, column=1, padx=5, pady=5)
        self.boton_reproducir_cola.grid(row=2, column=2, padx=5, pady=5)
        
        self.boton_crear_lista.grid(row=3, column=0, padx=5, pady=5)
        self.boton_ver_listas.grid(row=3, column=1, padx=5, pady=5)
        self.boton_ver_canciones_lista.grid(row=3, column=2, padx=5, pady=5)
        self.boton_agregar_cancion_lista.grid(row=3, column=3, padx=5, pady=5)
        self.boton_eliminar_cancion_lista.grid(row=3, column=4, padx=5, pady=5)
        
        self.boton_agregar_cancion.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.boton_reproducir_lista.grid(row=4, column=2, columnspan=3, padx=5, pady=5, sticky="ew")

    def cargar_musica(self):
        directorio = filedialog.askdirectory()
        if directorio:
            self.playlist = self.obtener_archivos_mp3(directorio)
            print("Cargando canciones:", self.playlist)

    def obtener_archivos_mp3(self, directorio):
        archivos_mp3 = [os.path.join(directorio, f) for f in os.listdir(directorio) if f.endswith('.mp3')]
        return archivos_mp3

    def agregar_cancion(self):
        archivo = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if archivo:
            self.playlist.append(archivo)
            print(f"Canción agregada: {archivo}")

    def agregar_a_cola(self):
        archivo = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if archivo:
            self.queue.append(archivo)
            print(f"Canción agregada a la cola: {archivo}")

    def ver_cola(self):
        if self.queue:
            canciones_str = "\n".join([os.path.basename(cancion) for cancion in self.queue])
            messagebox.showinfo("Cola de Reproducción", canciones_str)
        else:
            messagebox.showinfo("Cola de Reproducción", "La cola de reproducción está vacía.")

    def reproducir_musica(self):
        if not self.is_playing and self.playlist:
            self.is_playing = True
            if self.player.get_state() == vlc.State.Paused:
                self.player.play()
            else:
                threading.Thread(target=self.reproducir_cola_playlist).start()

    def reproducir_cola_playlist(self):
        while self.current_index < len(self.playlist) and self.is_playing:
            self.reproducir_cancion(self.current_index)
            while self.player.is_playing():
                time.sleep(1)
            self.current_index += 1
        self.is_playing = False

    def reproducir_cola(self):
        if not self.is_playing and self.queue:
            self.is_playing = True
            self.playlist = self.queue.copy()
            self.queue.clear()
            self.current_index = 0
            threading.Thread(target=self.reproducir_cola_playlist).start()

    def reproducir_cancion(self, index):
        media = self.instance.media_new(self.playlist[index])
        self.player.set_media(media)
        self.player.play()
        time.sleep(1)

    def pausar_musica(self):
        self.is_playing = False
        self.player.pause()

    def siguiente_cancion(self):
        if self.playlist and self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.reproducir_cancion(self.current_index)

    def anterior_cancion(self):
        if self.playlist and self.current_index > 0:
            self.current_index -= 1
            self.reproducir_cancion(self.current_index)

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
            archivo = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
            if archivo:
                nombre_cancion = os.path.basename(archivo)
                nombre_artista = simpledialog.askstring("Agregar Canción a Lista de Reproducción", "Ingrese el nombre del artista:")
                if nombre_cancion and nombre_artista:
                    cancion = Cancion(nombre_cancion, nombre_artista)
                    self.beatflow.agregar_cancion(nombre_lista, cancion)
                    self.beatflow.listas_reproduccion[nombre_lista].canciones[-1].archivo = archivo

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

    def reproducir_lista(self):
        nombre_lista = simpledialog.askstring("Reproducir Lista de Reproducción", "Ingrese el nombre de la lista de reproducción:")
        if nombre_lista:
            canciones = self.beatflow.ver_canciones_lista(nombre_lista)
            if isinstance(canciones, list) and canciones:
                self.playlist = [cancion.archivo for cancion in self.beatflow.listas_reproduccion[nombre_lista].canciones]
                self.current_index = 0
                self.reproducir_musica()
            else:
                messagebox.showerror("Error", "No se pudieron obtener las canciones de la lista de reproducción o la lista está vacía.")
