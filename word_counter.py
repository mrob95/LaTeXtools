# coding=utf-8
import re
from dragonfly import Clipboard

file_path = "minimum wage essay.tex"

def compile_regex_list(list):
    regex_list = []
    for raw_regex in list:
        regex_list.append(re.compile(raw_regex))
    return regex_list

def regex_match(regex_list, string):
    contained = False
    for regex in regex_list:
        if regex.search(string):
            contained = True
    return contained

ignore_ends = [r"%.*", r"\\begin{document}", r"\\end{table}", r"\\end{figure}", r"\\end{equation}"]
ignore_starts = [r"%.*", r"\\end{document}", r"\\begin{table}", r"\\begin{figure}", r"\\begin{equation}"]
ignore_ends_compiled = compile_regex_list(ignore_ends)
ignore_starts_compiled = compile_regex_list(ignore_starts)

ignore_words = [r"^$", r"^\-$", r"\\parencite.*",
    r"\\textcite.*", r"\\printbibliography",
    r"\\maketitle", r"\\newpage", r"\\ldots", r"\\end{itemize}", r"\\begin{itemize}",
    r"\\item", r"^\\$"]
ignore_words_compiled = compile_regex_list(ignore_words)

# First pass iterates through lines, removing unwanted chunks
# (starting to ignore when it hits something in ignore_starts, ending...)
def extract_sentences(line_list):
    sentence_list=[]
    flag=False
    for line in line_list:
        line = line.replace("\n", "")
        line = line.strip()
        if regex_match(ignore_starts_compiled, line):
            flag = False
        if flag:
            sentence_list.append(line)
        if regex_match(ignore_ends_compiled, line):
            flag = True
    return sentence_list

# Second pass iterates through words, removing unwanted words (ignore_words)
def extract_words(sentence_list):
    words_list = []
    for sentence in sentence_list:
        words = sentence.split(" ")
        for word in words:
            if not regex_match(ignore_words_compiled, word):
                words_list.append(word)
    return words_list

# This just gets a list of lines from a text file
def list_of_lines(path):
    with open(path,'r') as f:
        raw_line_list = []
        for line in f:
            raw_line_list.append(line)
    return raw_line_list

def file_to_words_list(path):
    raw_line_list = list_of_lines(path)
    sentence_list = extract_sentences(raw_line_list)
    words_list = extract_words(sentence_list)
    return words_list

def word_count(file_path):
    return len(file_to_words_list(file_path))
