'''
Created on 23.07.2012

@author: stes
'''

from nbot.google.BeautifulSoup import BeautifulSoup, SoupStrainer
from nbot.google.google import *
from tools import *
import re
import urllib2

def fetch_content(uri):
    '''
    fetches content from the specified webpage and returns
    the html document
    '''
    response = urllib2.urlopen(uri)
    return response.read()

def remove_tags(data):
    return ''.join(BeautifulSoup(data).findAll(text=True))

def remove_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)

def get_hyperlinks(html):
    '''
    extracts all hyperlinks from the given html document
    and returns them in a list
    '''
    urllist = []
    for link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
        if link.has_key('href'):
            urllist.append(link['href'])
    return urllist

def google_search(query, results):
    '''
    performs a google search using the given query. Returns
    a list with urls when the specified number of results was
    found
    '''
    url_gen = search(query, stop=results)
    urls = []
    for url in url_gen:
        urls.append(url)
        if (len(urls) >= results):
            break
    return urls

if __name__ == "__main__":
    #TODO fix this
    content = fetch_content('http://www.codinghorror.com/blog/' \
                            '2012/07')
    print (remove_tags(content))
    printlist(get_hyperlinks(content))