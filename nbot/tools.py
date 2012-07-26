'''
Created on 24.07.2012

@author: stes
'''

from random import shuffle
from nbot.htmlparser import *
import os

def print80(text):
    tmp = ''
    for c in text:
        tmp+=c
        if len(tmp) > 80:
            print(tmp)
            tmp = ''
    print(tmp)

def printlist(list):
    for item in list:
        print(item)

if __name__ == '__main__':
    from nbot.document import Document, Library
    q = ['file:///home/stes/dislike.html']
    lib = Library()
    url = q.pop(0)
    page = fetch_content(url)
    hrefs = get_hyperlinks(page)
    q.extend(hrefs)
    while q:
        print 'currently %d elements in the queue' % len(q)
        url = q.pop(0)
        print 'getting %s' % url

        page = fetch_content(url)

        doc = Document(page)
        lib.add_document(doc)
    lib.save('res/dislike')