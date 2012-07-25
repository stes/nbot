'''
Created on 23.07.2012

@author: stes
'''

from nbot.google.google import *
from nbot.google.BeautifulSoup import BeautifulSoup, SoupStrainer
from tools import *
import httplib
import httplib2
import re

def fetch_content(uri):
    '''
    fetches content from the specified webpage and returns
    the html document
    '''
    http = httplib2.Http()
    status, response = http.request(uri)
    return response

def remove_tags(data):
    p = re.compile(r'<.*?>', re.DOTALL)
    return p.sub('', data)

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
    content = fetch_content('http://www.codinghorror.com/blog/\
                        2012/07')
    print (BeautifulSoup(content)).prettify()
    printlist(get_hyperlinks(content))