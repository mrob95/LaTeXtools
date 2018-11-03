from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import sys
sys.path.append('../')
from scripts import book_cite, save_to_bib, paper_cite, web_cite

class CitMan(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title("Citation manager")
        self.geometry("600x320")

        self.bib_path = self.path_from_file()
        self.reset()

        self.bib_path_field = ttk.Label(self)
        self.bib_path_field.config(text = self.bib_path)
        self.bib_path_field.grid(column=0, row=1, columnspan=2)

        self.browse_button = ttk.Button(text='Browse', command=self.ask_bib_dir)
        self.browse_button.grid(column=2, row=1)

        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(column=0, row=3, columnspan=2)

        self.book_search_button = ttk.Button(text="Search for books", command=self.book_search)
        self.book_search_button.grid(column=2, row=3)

        self.paper_search_button = ttk.Button(text="Search for papers", command=self.paper_search)
        self.paper_search_button.grid(column=3, row=3)

        self.web_cite_button = ttk.Button(text="Cite website", command=self.web_search)
        self.web_cite_button.grid(column=4, row=3)

        self.previous_button = ttk.Button(text="Previous", command=self.previous_ref)
        self.previous_button.grid(column=0, row=5)

        self.next_button = ttk.Button(text="Next", command=self.next_ref)
        self.next_button.grid(column=1, row=5)

        self.ref_field = ttk.Label(self, text = "")
        self.ref_field.grid(column=0, row=4, columnspan = 5, pady=20)

        self.save_button = ttk.Button(text="Save to Bibliography", command=self.ref_save)
        self.save_button.grid(column=3, row=5)

        self.saved_field = ttk.Label(self)
        self.saved_field.grid(column=0, row=6)

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
        self.saved_field.config(text="Reference successfully added")

    def book_search(self):
        self.reset()
        self.type = "book"
        book_name = self.search_entry.get()
        self.links_list = book_cite.goodreads_results(book_name)
        if self.links_list:
            new_ref = book_cite.citation_from_url(self.links_list[self.counter])
        else:
            new_ref = "No results found on goodreads"
        self.refs.append(new_ref)
        self.update_ref_field()

    def paper_search(self):
        self.reset()
        self.type = "paper"
        paper_name = self.search_entry.get()
        self.links_list = paper_cite.google_scholar_query(paper_name)
        if self.links_list:
            new_ref = paper_cite.return_bib(self.links_list[self.counter])
        else:
            new_ref = "No results found on Google scholar"
        self.refs.append(new_ref)
        self.update_ref_field()

    def web_search(self):
        self.reset()
        self.type = "web"
        web_url = self.search_entry.get()
        new_ref = web_cite.bibtex_from_link(web_url)
        self.refs.append(new_ref)
        self.update_ref_field()

    def reset(self):
        self.type = ""
        self.counter = 0
        self.refs = []
        self.links_list = []

    def update_ref_field(self):
        self.ref_field.config(text=self.refs[self.counter])

    def previous_ref(self):
        if self.counter == 0:
            pass
        else:
            self.counter = self.counter - 1
            self.update_ref_field()

    def next_ref(self):
        self.counter = self.counter + 1
        if self.counter < len(self.refs):
            pass
        else:
            if self.type == "book":
                new_ref = book_cite.citation_from_url(self.links_list[self.counter])
            elif self.type == "paper":
                new_ref = paper_cite.return_bib(self.links_list[self.counter])
            else:
                new_ref = ""
            self.refs.append(new_ref)
        self.update_ref_field()

x = CitMan()
x.mainloop()
