from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import datetime


# takes URL, returns beautiful soup
def request_page(url):
    header = {'User-Agent': 'Mozilla/5.0', "Cookie": "GSP=CF=4"}
    request = Request(url, headers=header)
    response = urlopen(request)
    html = response.read()
    htmlsoup = BeautifulSoup(html, features="lxml")
    return htmlsoup

'''
Returns a bibTeX citation for online resources given a url.
eg running bibtex_from_link("https://www.thetimes.co.uk/edition/business/higher-oil-prices-push-shell-profits-up50-x7kk3dg90")
returns:
@online{Higheroilprices,
 title = {Higher oil prices push Shell profits up 50% | Business | The Times},
 author = {},
 year = {},
 url = {https://www.thetimes.co.uk/edition/business/higher-oil-prices-push-shell-profits-up50-x7kk3dg90},
 urldate = {2018-11-01},
}
author and year need to be entered manually.
'''


def bibtex_from_link(url):
    if url[-4:] == ".pdf":
        tag = ""
        title = ""
    else:
        htmlsoup = request_page(url)
        title = htmlsoup.title.text.replace("\n", "").replace(":", "").replace(",", "").strip()
        title_split = title.split()
        if len(title_split) == 0:
            tag = ""
        if len(title_split) == 1:
            tag = title_split[0]
        elif len(title_split) == 2:
            tag = title_split[0] + title_split[1]
        else:
            tag = title_split[0] + title_split[1] + title_split[2]

    author_search = re.search(r'([a-z0-9]*\.(uk|com|co\.uk|org))', url)
    if author_search:
        author = author_search.group(1)
    else:
        author = ""

    year_search = re.search(r'(19|20)[8901]\d', url)
    if year_search:
        year = year_search.group(0)
    else:
        year = ""

    date = datetime.datetime.today().strftime('%Y-%m-%d')
    ref = "@online{" + tag + ",\n title = {" + str(title) + "},\n author = {" + author + "},\n year = {" + year + "},\n url = {" + url + "},\n urldate = {" + date + "}\n}\n"
    return ref
