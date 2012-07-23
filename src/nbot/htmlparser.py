'''
Created on 23.07.2012

@author: stes
'''

from src.nbot.google.google import search
import httplib
import re

def fetch_content(url):
    conn = httplib.HTTPConnection(url)
    conn.request("GET", "/index.html")
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

def google_search(query, results):
    url_gen = search(query, stop=results)
    urls = []
    for url in url_gen:
        urls.append(url)
        if (len(urls) >= results):
            break
    return urls

'''
i = 0
tmp = ''
for c in remove_spaces(remove_tags(content)):
    tmp+=c
    if i > 80:
        print(tmp)
        tmp = ''
        i = 0
    else:
        i+=1
'''
