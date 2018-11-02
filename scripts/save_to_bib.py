def save_to_bib(ref, bib_path):
    file = open(bib_path, "a")
    file.write(ref)
    print("Reference added:\n" + ref)
