from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pyperclip
import webbrowser


import sys
sys.path.append('../')
from scripts import book_cite, save_to_bib, paper_cite, web_cite, tag_from_ref

class CitMan(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title("Citation manager")
        self.geometry("650x360")
        self.configure(background = "white")

        self.bib_path = self.path_from_file()
        self.reset()

        self.padding = ttk.Label(self)
        self.padding.config(background = "white")
        self.padding.grid(column = 0, row =0, padx = 10, pady = 2)

        self.bib_path_field = ttk.Label(self, width = 50)
        self.bib_path_field.config(text = self.bib_path, background = "white")
        self.bib_path_field.grid(column=1, row=1, columnspan=2)

        self.browse_button = ttk.Button(text='Browse', command=self.ask_bib_dir)
        self.browse_button.grid(column=3, row=1)

        self.search_entry = ttk.Entry(self, width = 50)
        self.search_entry.grid(column=1, row=3, columnspan=2)

        self.book_search_button = ttk.Button(text="Search for books", command=self.book_search)
        self.book_search_button.grid(column=3, row=3)

        self.paper_search_button = ttk.Button(text="Search for papers", command=self.paper_search)
        self.paper_search_button.grid(column=4, row=3)

        self.web_cite_button = ttk.Button(text="Cite website", command=self.web_search)
        self.web_cite_button.grid(column=5, row=3)

        self.previous_button = ttk.Button(text="Previous", command=self.previous_ref)
        self.previous_button.grid(column=1, row=6)

        self.next_button = ttk.Button(text="Next", command=self.next_ref)
        self.next_button.grid(column=2, row=6)

        self.link_field = ttk.Label(self, text = "", width = 100, cursor = "hand2")
        self.link_field.grid(column=1, row=4, columnspan = 5, pady=10)
        self.link_field.bind("<Button-1>", self.open_link)

        self.ref_field = ttk.Label(self, text = "", width = 100)
        self.ref_field.grid(column=1, row=5, columnspan = 5, pady=10)

        self.save_button = ttk.Button(text="Save to Bibliography", command=self.ref_save)
        self.save_button.grid(column=3, row=6)

        self.copy_tag_button = ttk.Button(text="Copy tag to clipboard", command=self.tag_to_clipboard)
        self.copy_tag_button.grid(column=4, row=6, columnspan = 2)

        self.numbers_field = ttk.Label(self)
        self.numbers_field.config(background = "white")
        self.numbers_field.grid(column=1, row=7, columnspan = 2)

        self.notifications_field = ttk.Label(self)
        self.notifications_field.config(background = "white")
        self.notifications_field.grid(column=3, row=7, columnspan = 2)

    def update_path_file(self, new_path):
        with open("../bib_path.txt", "a+") as t:
            t.write("\n" + new_path)

    def path_from_file(self):
        t = open("../bib_path.txt", "r+")
        lines = t.readlines()
        if lines:
            path = lines[-1]
        else:
            path = ""
        return path

    def ask_bib_dir(self):
        self.bib_path = self.filedialog.askopenfilename()
        update_path_file(self.bib_path)
        self.bib_path_field.config(text=self.bib_path)

    def ref_save(self):
        save_to_bib.save_to_bib(self.refs[self.counter], self.bib_path)
        self.notifications_field.config(text="Reference successfully added")

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

    def book_search(self):
        self.reset()
        self.search_type = "book"
        book_name = self.search_entry.get()
        self.links_list = book_cite.goodreads_results(book_name)
        if self.links_list:
            new_ref = book_cite.citation_from_url(self.current_link())
        else:
            new_ref = "No results found on goodreads"
        self.refs.append(new_ref)
        self.update_fields()

    def paper_search(self):
        self.reset()
        self.search_type = "paper"
        paper_name = self.search_entry.get()
        self.links_list = paper_cite.google_scholar_query(paper_name)
        if self.links_list:
            new_ref = paper_cite.return_bib(self.current_link())
        else:
            new_ref = "No results found on Google scholar"
        self.refs.append(new_ref)
        self.update_fields()

    def web_search(self):
        self.reset()
        self.search_type = "web"
        web_url = self.search_entry.get()
        new_ref = web_cite.bibtex_from_link(web_url)
        self.refs.append(new_ref)
        self.update_fields()

    def open_link(self, event=None):
        webbrowser.open_new(self.current_link())

    def reset(self):
        self.search_type = ""
        self.counter = 0
        self.refs = []
        self.links_list = []

    def update_fields(self):
        self.link_field.config(text = self.current_link())
        self.ref_field.config(text=self.current_ref())
        self.numbers_field.config(text=str(self.counter + 1))

    def previous_ref(self):
        if self.counter == 0:
            pass
        else:
            self.counter = self.counter - 1
            self.update_fields()

    def next_ref(self):
        self.counter = self.counter + 1
        if self.counter >= len(self.links_list):
            new_ref = "Limit reached"
            self.refs.append(new_ref)
        else:
            if self.counter < len(self.refs):
                pass
            else:
                if self.search_type == "book":
                    new_ref = book_cite.citation_from_url(self.current_link())
                elif self.search_type == "paper":
                    new_ref = paper_cite.return_bib(self.current_link())
                else:
                    new_ref = ""
                self.refs.append(new_ref)
        self.update_fields()

    def tag_to_clipboard(self):
        tag = tag_from_ref.get_tag(self.current_ref())
        if tag == "No tag found":
            self.notifications_field.config(text = tag)
        else:
            pyperclip.copy(tag)
            self.notifications_field.config(text = tag + " added to clipboard")

x = CitMan()
x.mainloop()
