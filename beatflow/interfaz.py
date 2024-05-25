import vlc
import tkinter
import os
from beatflow.beatflow import *
import threading
import tkinter as tk
from tkinter import filedialog
import threading
import vlc
import time
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Beatflow Music Player")
        self.root.geometry("400x200")

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.playlist = []
        self.current_index = 0

        self.is_playing = False

        # Botones de UI
        self.load_button = tk.Button(self.root, text="Cargar", command=self.load_music)
        self.load_button.pack()

        self.play_button = tk.Button(self.root, text="Reproducir", command=self.play_music)
        self.play_button.pack()

        self.stop_button = tk.Button(self.root, text="Pausar", command=self.stop_music)
        self.stop_button.pack()

        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack()

    def load_music(self):
        directory = filedialog.askdirectory()
        if directory:
            self.playlist = self.get_mp3_files(directory)
            print("cargando canciones:", self.playlist)

    def get_mp3_files(self, directory):
        mp3_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
        return mp3_files

    def play_music(self):
        if not self.is_playing and self.playlist:
            self.is_playing = True
            threading.Thread(target=self.play_queue).start()

    def play_queue(self):
        while self.current_index < len(self.playlist) and self.is_playing:
            self.play_song(self.current_index)
            while self.player.is_playing():
                time.sleep(1)
            self.current_index += 1
        self.is_playing = False

    def play_song(self, index):
        media = self.instance.media_new(self.playlist[index])
        self.player.set_media(media)
        self.player.play()
        time.sleep(1)

    def stop_music(self):
        self.is_playing = False
        self.player.stop()

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))
