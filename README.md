# LaTeXtools

Some simple but useful scripts for improving productivity with LaTeX. Current functionality:

* `book_cite.py` - Take the title of an academic work, search Google scholar for it and then return a bibTeX citation for the first result, of the form:
```
@article{alesina2018or,
  title={Is it the "How" or the "When" that Matters in Fiscal Adjustments?},
  author={Alesina, Alberto and Azzalini, Gualtiero and Favero, Carlo and Giavazzi, Francesco and Miano, Armando},
  journal={IMF Economic Review},
  volume={66},
  number={1},
  pages={144--188},
  year={2018},
  publisher={Springer}
}
```

* `paper_cite.py` Take the title of a book, search goodreads for it, scrape the key data from the first result and return a citation of the form:
```
@book{wedgwood1938thirty,
 title={The Thirty Years War},
 author={C.V. Wedgwood and Anthony Grafton},
 year={1938/2005},
 publisher={New York Review of Books}
}
```

* `web_cite.py` - Take a url and build an online resource citation:
```
@online{Higheroilprices,
 title = {Higher oil prices push Shell profits up 50% | Business | The Times},
 author = {},
 year = {},
 url = {https://www.thetimes.co.uk/edition/business/higher-oil-prices-push-shell-profits-up50-x7kk3dg90},
 urldate = {2018-11-01},
}
```

* All of which can be appended to a .bib file using `save_to_bib.py` and then cited using `\parencite{}`

* `html_table.py` - converts a HTML table into a simple latex table.

* `word_counter.py` - WIP, takes a latex file, strips out headers, tables, figures, comments etc to give an accurate word count.
