'''
Created on 23.07.2012

@author: stes
'''

from nbot.htmlparser import *
from nbot.document import *
from hashlib import sha1
from random import shuffle
from time import time
from Queue import Queue
from threading import Thread

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
        self.__queue = Queue()
        self.__id = 0
    
    def crawl(self):
        q = [self.__urllist]
        lib = Library()
        i = 500
        visited = []
        while q and i > 0:
            print 'currently %d elements in the queue' % len(q)
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
            i -= 1
            hrefs = get_hyperlinks(page)
            shuffle(hrefs)
            print 'found %d new hyperlinks' % len(hrefs)
            q.extend(hrefs[:10])
            doc = Document(page)
            lib.add_document(doc)
        lib.save('pages')
    
    def crawl_url(self):
        id = self.__id
        self.__id += 1
        iterations = 100
        lib = Library()
        while iterations > 0:
            url = self.__queue.get(True, None)
            print '%d: getting %s' % (id, url)
            try:
                page = fetch_content(url)
            except:
                continue
            iterations -= 1
            hrefs = get_hyperlinks(page)
            shuffle(hrefs)
            print 'found %d new hyperlinks' % len(hrefs)
            for href in hrefs[:10]:
                self.__queue.put(href)
            doc = Document(page)
            lib.add_document(doc)
            self.__queue.task_done()
        return lib

    def crawl_threading(self, threads):
        for i in range(threads):
            t = Thread(target=self.crawl_url)
            t.daemon = True
            t.start()
        self.__queue.put(self.__urllist)
        self.__queue.join()
        print 'done'
        # TODO

if __name__ == '__main__':
    starttime = time()
    crawler = Crawler('http://news.google.com', 5)
    crawler.crawl_threading(8)
    print 'finished crawling'
    stoptime = time()
    print 'crawled for %f seconds' % (stoptime-starttime)