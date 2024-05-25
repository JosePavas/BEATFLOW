import os
import sys
import tkinter as tk
from BEATFLOW.view.interfaz import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

root = tk.Tk()
root.title("BeatFlow Music Player")

player = ReproductorMusica(root)

root.mainloop()