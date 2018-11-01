try:
    from urllib.request import Request, urlopen, quote
except ImportError:
    from urllib2 import Request, urlopen, quote

from bs4 import BeautifulSoup
import re

# takes URL, returns beautiful soup
def request_page(url):
    header = {'User-Agent': 'Mozilla/5.0', "Cookie":"GSP=CF=4"}
    request = Request(url, headers=header)
    response = urlopen(request)
    html = response.read()
    htmlsoup = BeautifulSoup(html, features="lxml")
    return htmlsoup

'''
Takes any search string, returns a list of links to google scholar bibTeX citations
'''
def google_scholar_query(searchstr):
    searchstr = '/scholar?q=' + quote(searchstr)
    url = "https://scholar.google.com" + searchstr
    htmlsoup = request_page(url)
    links_list = []
    refre = re.compile(r'https://scholar.googleusercontent.com(/scholar\.bib\?[^"]*)')
    for link in htmlsoup.find_all("a"):
        link_url = link.get("href")
        if refre.search(link_url):
            links_list.append(link_url)
    return links_list

def return_bib(scholar_bib_url):
    bib = request_page(scholar_bib_url).p.text
    return bib

'''
Example:
Running bib_from_title("is it the how or the when that matters in fiscal adjustments?")
returns:
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
'''
def bib_from_title(query):
    link_list = google_scholar_query(query)
    bib = return_bib(link_list[0])
    return bib
