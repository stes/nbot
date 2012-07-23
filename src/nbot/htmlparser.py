'''
Created on 23.07.2012

@author: stes
'''

import re
import httplib

def fetch_content(url):
    conn = httplib.HTTPConnection(url)
    conn.request("GET", "/index.html")
    response = conn.getresponse()
    content = response.read()
    conn.close()
    return content

def remove_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def remove_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)

content = fetch_content("python.org")
i = 0
tmp = ''
for c in remove_spaces(remove_tags(content)):
    tmp+=c
    if i > 80:
        print tmp
        tmp = ''
        i = 0
    else:
        i+=1