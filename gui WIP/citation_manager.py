from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pyperclip
import webbrowser
import json

import sys
sys.path.append('../')
from scripts import book_cite, save_to_bib, paper_cite, web_cite, tag_from_ref

class CitMan(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("Citation manager")
        self.geometry("650x400")
        self.configure(background="white")

        self.settings = {}
        self.get_settings()
        self.reset()
        self.create_menu_options()

        # self.theme = ttk.Style()
        # self.theme.theme_use("default")

        self.padding = ttk.Label(self)
        self.padding.config(background="white")
        self.padding.grid(column=0, row=0, padx=10, pady=2)

        self.bib_path_field = ttk.Label(self, width=50)
        self.bib_path_field.config(text=self.settings["bib_path"], background="white")
        self.bib_path_field.grid(column=1, row=1, columnspan=2)

        self.browse_button = ttk.Button(text='Browse', command=self.ask_bib_dir)
        self.browse_button.grid(column=3, row=1)

        self.search_entry = ttk.Entry(self, width=50)
        self.search_entry.focus_set()
        self.search_entry.grid(column=1, row=5, columnspan=2)
        self.search_entry.bind("<Return>", self.search)
        self.search_entry.bind("<Tab>", lambda e: self.menu.focus_set())
        self.bind("<Control-l>", lambda e: self.search_entry.focus_set())

        self.menu = ttk.OptionMenu(self, self.selected_option, self.options[0], *self.options)
        self.menu.grid(column=3, row=5)
        self.menu.bind("<Return>", self.search)

        self.search_button = ttk.Button(text="Search for citations", command=self.search)
        self.search_button.grid(column=4, row=5)

        self.previous_button = ttk.Button(text="Previous", command=self.previous_ref)
        self.previous_button.grid(column=1, row=13)
    
        self.next_button = ttk.Button(text="Next", command=self.next_ref)
        self.next_button.grid(column=2, row=13)
        
        self.link_field = ttk.Label(self, text="", width=100, cursor="hand2")
        self.link_field.grid(column=1, row=7, columnspan=5, pady=10)
        self.link_field.bind("<Button-1>", lambda e: webbrowser.open_new(self.current_link()))

        self.ref_field = ttk.Label(self, text="", width=100)
        self.ref_field.grid(column=1, row=8, columnspan=5, pady=10)
        # focus is automatically set to ref_field after a search
        self.ref_field.bind("<Tab>", lambda e: self.search_entry.focus_set())
        self.ref_field.bind("p", self.previous_ref)
        self.ref_field.bind("<Left>", self.previous_ref)
        self.ref_field.bind("n", self.next_ref)
        self.ref_field.bind("<Right>", self.next_ref)
        self.ref_field.bind("<Control-s>", self.ref_save)
        self.ref_field.bind("<Control-c>", self.tag_to_clipboard)

        self.save_button = ttk.Button(text="Save to Bibliography", command=self.ref_save)
        self.save_button.grid(column=3, row=13)
        
        self.copy_tag_button = ttk.Button(text="Copy tag to clipboard", command=self.tag_to_clipboard)
        self.copy_tag_button.grid(column=4, row=13)
        
        self.numbers_field = ttk.Label(self, background="white")
        self.numbers_field.grid(column=1, row=15, columnspan=2)

        self.notifications_field = ttk.Label(self, background="white")
        self.notifications_field.grid(column=3, row=15, columnspan=2)

        for i in range(0, 4):
            shortcuts = ["p / left", "n / right", "ctrl-s", "ctrl-c"]
            label = ttk.Label(self)
            label.configure(text=shortcuts[i], background="white")
            label.grid(column=i+1, row=10)

        self.search_bar_shortcut = ttk.Label(self)
        self.search_bar_shortcut.configure(text="ctrl-L / Tab (after search)", background="white")
        self.search_bar_shortcut.grid(column=1, row=6, columnspan=2)

    def ask_bib_dir(self):
        self.settings["bib_path"] = filedialog.askopenfilename()
        self.update_settings_file()
        self.update_fields()

    def search(self, *args):
        self.reset()
        self.notifications_field.config(text="Searching...")
        self.search_type = self.selected_option.get()
        query = self.search_entry.get()
        if self.search_type == self.options[0]:
            self.links_list = book_cite.goodreads_results(query)
            if self.links_list:
                new_ref = book_cite.citation_from_url(self.current_link())
            else:
                new_ref = "No results found on goodreads"

        elif self.search_type == self.options[1]:
            self.links_list = paper_cite.google_scholar_query(query)
            if self.links_list:
                new_ref = paper_cite.return_bib(self.current_link())
            else:
                new_ref = "No results found on Google scholar"

        elif self.search_type == self.options[2]:
            self.links_list.append(query)
            new_ref = web_cite.bibtex_from_link(self.current_link())

        self.refs.append(new_ref)
        self.update_fields()
        self.notifications_field.config(text="Reference found")
        self.ref_field.focus_set()

    def reset(self):
        self.counter = 0
        self.refs = []
        self.links_list = []
        self.search_type = ""

    def create_menu_options(self):
        self.options = ["Book - goodreads",
            "Paper - Google scholar",
            "Cite web resource"]
        self.selected_option = StringVar(self)
        self.selected_option.set(self.options[0])

    def update_fields(self):
        self.link_field.config(text=self.current_link())
        self.ref_field.config(text=self.current_ref())
        self.numbers_field.config(text=str(self.counter + 1))
        self.bib_path_field.config(text=self.settings["bib_path"])

    def previous_ref(self, *args):
        if self.counter == 0:
            pass
        else:
            self.counter = self.counter - 1
            self.update_fields()

    def next_ref(self, *args):
        if self.current_ref():        
            self.counter = self.counter + 1
            if self.counter >= len(self.links_list):
                new_ref = "No more references available"
                self.refs.append(new_ref)
            elif self.counter == len(self.refs):
                self.notifications_field.config(text="Searching...")
                if self.search_type == self.options[0]:
                    new_ref = book_cite.citation_from_url(self.current_link())
                elif self.search_type == self.options[1]:
                    new_ref = paper_cite.return_bib(self.current_link())
                else:
                    new_ref = ""
                self.refs.append(new_ref)
                self.notifications_field.config(text="Reference found")
            self.update_fields()

    def ref_save(self, *args):
        if self.current_ref():        
            save_to_bib.save_to_bib(self.current_ref(), self.settings["bib_path"])
            self.notifications_field.config(text="Reference successfully added")


    def tag_to_clipboard(self, *args):
        if self.current_ref():
            tag = tag_from_ref.get_tag(self.current_ref())
            if tag == "No tag found":
                self.notifications_field.config(text=tag)
            else:
                pyperclip.copy(tag)
                self.notifications_field.config(text=tag + " added to clipboard")

    def current_ref(self):
        if self.refs:
            return self.refs[self.counter]
        else:
            return ""

    def current_link(self):
        if self.links_list:
            return self.links_list[self.counter]
        else:
            return ""

    def update_settings_file(self):
        with open('../settings.json', 'w+') as fp:
            json.dump(self.settings, fp)

    def get_settings(self):
        with open('../settings.json', 'r+') as fp:
            self.settings = json.load(fp)
        if not self.settings:
            self.settings = {"bib_path":""}


def show():
    x = CitMan()
    x.mainloop()
show()
