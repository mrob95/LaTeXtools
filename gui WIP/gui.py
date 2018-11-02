from tkinter import *
from tkinter import filedialog

import sys
sys.path.append('../')
from scripts import book_cite, save_to_bib

bib_path = ""
ref = ""

window = Tk()

window.title("Citation manager")
window.geometry("1000x600")

def ask_bib_dir():
    global bib_path
    bib_path = filedialog.askopenfilename()
    print(bib_path)
    bib_path_field.config(text=bib_path)

def book_search():
    book_name = search_entry.get()
    global ref
    ref = book_cite.citation_from_name(book_name)
    ref_field.config(text=ref)
    print(ref)

def ref_save():
    save_to_bib.save_to_bib(ref, bib_path)
    saved_field.config(text="Reference successfully added")

bib_path_field = Label(window, text = bib_path)
bib_path_field.grid(column=1, row=1)

browse_button = Button(text='Browse', command=ask_bib_dir)
browse_button.grid(column=2, row=1)

search_entry = Entry(window)
search_entry.grid(column=1, row=3)

search_button = Button(text="Search for citations", command=book_search)
search_button.grid(column=2, row=3)

ref_field = Label(window, text = ref)
ref_field.grid(column=1, row=4)

save_button = Button(text="Save to Bibliography", command=ref_save)
save_button.grid(column=2, row=4)

saved_field = Label(window)
saved_field.grid(column=2, row=5)

window.mainloop()

# print(book_cite.citation_from_name("the case against education"))
