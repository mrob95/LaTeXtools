from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import json

import sys
sys.path.append('../')
from scripts import word_counter

class Counter(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("Word counter")
        self.geometry("460x100")
        self.configure(background = "white")

        self.settings = {}
        self.get_settings()
        self.count = ""

        self.path_label = ttk.Label(self, width = 60, anchor = "w")
        self.path_label.config(background = "white")
        self.path_label.grid(column=1, row=1, padx=5, pady=5)

        self.browse_button = ttk.Button(text='Browse', command=self.ask_file_path)
        self.browse_button.grid(column=2, row=1)

        self.count_label = ttk.Label(self)
        self.count_label.config(background = "white", text = str(self.count))
        self.count_label.grid(column=1, row=3, pady = 5)

        self.count_button = ttk.Button(text="Count", command=self.get_count)
        self.count_button.grid(column=1, row=2, pady = 5)

        self.get_count()
        self.update_path_label()

    def update_settings_file(self):
        with open('../settings.json', 'w+') as fp:
            json.dump(self.settings, fp)

    def get_settings(self):
        with open('../settings.json', 'r+') as fp:
            self.settings = json.load(fp)
        if not self.settings:
            self.settings = {"bib_path":"", "count_file_path":""}

    def ask_file_path(self):
        self.settings["count_file_path"] = filedialog.askopenfilename()
        self.update_settings_file()
        self.update_path_label()

    def get_count(self):
        path = self.settings["count_file_path"]
        if path:
            self.count = word_counter.word_count(path)
            self.count_label.config(text = str(self.count))
        else:
            self.count = 0

    def update_path_label(self):
        if len(self.settings["count_file_path"])>57:
            visible_path = "..." + self.settings["count_file_path"][-57:]
        else:
            visible_path = self.settings["count_file_path"]
        self.path_label.config(text = visible_path)

x = Counter()
x.mainloop()
