from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import sys
sys.path.append('../')
from scripts import book_cite, save_to_bib, paper_cite, web_cite

def update_path_file(new_path):
    with open("../bib_path.txt", "a+") as t:
        t.write("\n" + new_path)

def path_from_file():
    t = open("../bib_path.txt", "r+")
    lines = t.readlines()
    if lines:
        path = lines[-1]
    else:
        path = ""
    return path

def ask_bib_dir():
    global bib_path
    bib_path = filedialog.askopenfilename()
    update_path_file(bib_path)
    bib_path_field.config(text=bib_path)

def book_search():
    book_name = search_entry.get()
    global ref
    ref = book_cite.citation_from_name(book_name)
    ref_field.config(text=ref)
    print(ref)

def paper_search():
    paper_name = search_entry.get()
    global ref
    ref = paper_cite.bib_from_title(paper_name)
    ref_field.config(text=ref)
    print(ref)

def web_search():
    web_url = search_entry.get()
    global ref
    ref = web_cite.bibtex_from_link(web_url)
    ref_field.config(text=ref)
    print(ref)

def ref_save():
    save_to_bib.save_to_bib(ref, bib_path)
    saved_field.config(text="Reference successfully added")

global bib_path
bib_path = path_from_file()
print(bib_path)
ref = ""

window = Tk()

window.title("Citation manager")
window.geometry("600x400")

bib_path_field = ttk.Label(window)
bib_path_field.config(text = bib_path)
bib_path_field.grid(column=1, row=1)

browse_button = ttk.Button(text='Browse', command=ask_bib_dir)
browse_button.grid(column=2, row=1)

search_entry = ttk.Entry(window)
search_entry.grid(column=1, row=3)

book_search_button = ttk.Button(text="Search for books", command=book_search)
book_search_button.grid(column=2, row=3)

paper_search_button = ttk.Button(text="Search for papers", command=paper_search)
paper_search_button.grid(column=3, row=3)

web_cite_button = ttk.Button(text="Cite website", command=web_search)
web_cite_button.grid(column=4, row=3)

ref_field = ttk.Label(window, text = ref)
ref_field.grid(column=1, row=4)

save_button = ttk.Button(text="Save to Bibliography", command=ref_save)
save_button.grid(column=2, row=5)

saved_field = ttk.Label(window)
saved_field.grid(column=1, row=5)

window.mainloop()

# print(book_cite.citation_from_name("the case against education"))
