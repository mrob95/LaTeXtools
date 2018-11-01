import pandas

def to_latex(html_table):
    df = pandas.read_html(html_table)[0]
    latex = df.to_latex(index=False)
    latex = latex.replace("\n\\toprule", "")
    latex = latex.replace("\n\\bottomrule", "")
    latex = latex.replace("\\midrule", "\\hline")
    return latex
