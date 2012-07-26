'''
Created on 23.07.2012

@author: stes
'''

from nbot.htmlparser import *
from nbot.document import *
from hashlib import sha1
from random import shuffle

class Crawler():
    '''
    classdocs
    '''

    def __init__(self, urllist, depth):
        '''
        Constructor
        '''
        self.__urllist = urllist
        self.__depth = depth
        self.__queue = urllist
    
    def crawl(self):
        q = []
        q.extend(self.__queue)
        lib = Library()
        i = 200
        visited = []
        while q and i > 0:
            i -= 1
            url = q.pop(0)
            urlhash = sha1(url)
            if urlhash in visited:
                continue
            visited.append(urlhash)
            print 'getting %s' % url
            try:
                page = fetch_content(url)
            except:
                continue
            hrefs = get_hyperlinks(page)
            shuffle(hrefs)
            print 'found %d new hyperlinks' % len(hrefs)
            q.extend(hrefs)
            doc = Document(page)
            lib.add_document(doc)
        lib.save('pages')
            
        # TODO

if __name__ == '__main__':
    crawler = Crawler(['http://www.news.google.com'], 5)
    crawler.crawl()