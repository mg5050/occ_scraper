"""
OCC Scraper:
    scrape.py:
        occ specific & non-specific scraper functions

Author: Mike Gonzalez (mgonz50@rutgers.edu)
"""

from bs4 import BeautifulSoup
from occ_vars import *
from io import BytesIO
import pycurl

def post_Text(contents): # stringize soup.contents
    post = ""
    for x in contents:
        post += str(x)
    return post

def post_Trim(text): # remove post signature
    pos = text.find(sig_trima) # find first trim
    if pos != -1: return text[:pos]
    pos = text.find(sig_trimb) # find second
    if pos != -1: return text[:pos]
    return text

def post_Sanitize(text): # replace line break with newline
    return text.replace(br, "\\n").replace(br_alt, "\\n")

def data_Sanitize(text): # replace newline and return carriage
    return text.replace('\n','').replace('\r','')

def date_Trim(text): # remove "Posted: "
    return text[len(date_trim):]

def qm(text): # add quotation marks
    return '\"' + text + '\"'

def curl_Page(url): # curl and return a decoded page
    buffer = BytesIO()
    data = pycurl.Curl()
    data.setopt(data.URL, url)
    data.setopt(data.WRITEDATA, buffer)
    data.perform()
    data.close()
    return buffer.getvalue().decode(encoding, 'ignore')

def represent_Int(text): # does text represent an integer?
    try:
        int(text)
        return True
    except ValueError:
        return False

def grab_Links(soup, remote=True): # grab links from nav bar, remote links are relative
    nav = soup.find("span", class_="gensmall").find_all('a')
    links = []
    for a in nav:
        if represent_Int(a.string): 
            links.append((absolute_path if remote else "") + a['href']) # links grabbed remotely are relative
    return links

def scrape_Page(page_soup): # scrape a page soup
    page_soup = page_soup.find_all("span", class_="name")
    data = ""
    for post in page_soup:
        parent_TR = post.parent.parent
        next_TD = parent_TR.td.next_sibling.next_sibling
        post_txt = post_Trim(post_Text(next_TD.find("span", class_="postbody").contents))

        if post_txt == "": # "user123 wrote: " + quote + user's actual post
            post_txt = \
            next_TD.find("span", class_="genmed").string + ' ' + \
            post_Text(next_TD.find("td", class_="quote").contents) + '\\n' + \
            post_Text(next_TD.find("span", class_="postbody").find_next("span", class_="postbody").contents[2:])

        data += \
        data_Sanitize \
        (
            post.a['name'] + # id
            delim + 
            qm(post.b.string) + # user name
            delim + 
            qm(date_Trim(next_TD.span.contents[0])) + # date
            delim + 
            qm(post_Sanitize(post_txt)) # post text
        ) + '\n'
    return data.encode(write_enc)

def scrape_Site(links): # scrape a series of links
    f = open(output_fname, 'wb')
    for link in links:
        print("Scraping URL: " + link + '\n')
        soup = BeautifulSoup(curl_Page(link), 'html.parser') # remote curl
        f.write(scrape_Page(soup))
    f.close()

def local_Scrape(local_fname, file_output=True): # used for debugging, avoid bringing down the website
    soup = BeautifulSoup(open(local_fname, encoding = encoding).read(), 'html.parser') # local file
    data = scrape_Page(soup)
    if file_output: 
        f = open(output_fname, 'wb')
        f.write(data)
        f.close()
    return data

def remote_Scrape(url, all=False): # all? - scrape subsequent pages or just 'url'?
    soup = BeautifulSoup(curl_Page(url), 'html.parser')
    if all: scrape_Site([url] + grab_Links(soup)) # scrape all links?
    else: print(scrape_Page(url))