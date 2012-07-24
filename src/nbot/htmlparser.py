'''
Created on 23.07.2012

@author: stes
'''

from src.nbot.google.google import search
from src.nbot.tools import *
import httplib
import re

def fetch_content(authority, path):
    '''
    fetches content from the specified webpage and returns
    the html document
    '''
    conn = httplib.HTTPConnection(authority)
    conn.request("GET", path+"/index.html")
    response = conn.getresponse()
    content = response.read()
    conn.close()
    return content

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
    p = re.compile(r'href="(.*?)".*?', re.DOTALL)
    return p.findall(html)

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

if __name__ == '__main__':
    page = fetch_content('news.google.de', '')
    urls = get_hyperlinks(page)
    printlist(urls)