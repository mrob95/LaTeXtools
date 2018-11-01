
bibliography_path = ""

def save_to_bib(ref):
    file = open(bibliography_path, "a")
    file.write(ref)
    print("Reference added:\n" + ref)
