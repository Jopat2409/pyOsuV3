""" ---------- OSU MODULES ---------- """
import MainMenu
""" ---------- PYTHON MODULES ---------- """
import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import threading
import os
import glob


def funct():
    print("funct")


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.m_label = None
        self.rListBox = None
        self.root = None
        self.m_replays = []
        self.lReplayPointer = 0
        self.m_addReplayButton = tk.Button(self.root, command=self.AddReplays, text="Add Replay Directory")
        self.m_cConfig = ""
        self.start()

    def callback(self):
        self.root.quit()

    def AddReplays(self):
        if not self.m_cConfig:
            return
        folder_selected = filedialog.askdirectory()
        self.rListBox.place_forget()

        offset = self.lReplayPointer
        for index, _replay in enumerate(glob.glob(os.path.join(folder_selected, "*.osr"))):
            self.m_replays.append(_replay)
            self.rListBox.insert(offset + index, os.path.basename(_replay))
            self.lReplayPointer = index

    def NewConfig(self):
        gsName = simpledialog.askstring("Name", "What would you like to call this config?",
                                        parent=self.root)
        if gsName is not None:
            self.root.title(f"Current Config: {gsName}")
            self.rListBox.place(x=350, y=25)
            self.m_label.place_forget()
            self.m_addReplayButton.place(x=0, y=0)

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("500x500+0+0")
        self.root.title("Configure Neural Network")
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)

        self.rListBox = tk.Listbox(self.root)

        menubar = tk.Menu(self.root)

        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Add Replays", command=self.AddReplays)
        fileMenu.add_command(label="Add Beatmap Folders", command=funct)
        menubar.add_cascade(label="File", menu=fileMenu)

        configMenu = tk.Menu(menubar, tearoff=0)
        configMenu.add_command(label="New Config", command=self.NewConfig)
        configMenu.add_command(label="Load Config", command=funct)
        menubar.add_cascade(label="Config", menu=configMenu)

        self.root.config(menu=menubar)

        self.m_label = tk.Label(self.root, text="+ Create a Config To Start!")
        self.m_label.config(font=("Courier", 14))
        self.m_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.root.mainloop()


class gsNeuralConfig:

    def __init__(self, parentClass):
        self.m_parent = parentClass
        self.KEY_MAP = {}

        self.m_window = App()

    def update(self):
        if not self.m_window.is_alive():
            self.m_parent.newGamestate(MainMenu.gsMenu(self.m_parent))

    def getRenderSnapshot(self, interpolation, surface):
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (100, 100, 100), (100, 100, 100, 100))
