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
import bisect

class Crawler():
    '''
    classdocs
    '''

    def __init__(self, urllist, recsys):
        '''
        Constructs a new crawler using the specified url list and the specified
        recommender system to rate the relevance of the downloaded pages
        
        @param urllist: A list of urls to start with
        @param recsys: A recommender system to rate pages
        '''
        self.__urllist = urllist
        self.__queue = Queue()
        self.__recsys = recsys
        self.__threads = []

    def crawl(self, threads=2):
        '''
        Starts crawling using the (optional) specified number of threads
        Blocks until crawling is finished
        
        @param threads: The number of threads used for crawling, default is 2
        '''
        for i in range(threads):
            t = _CrawlThread(i, self.__queue)
            self.__threads.append(t)
            t.deamon = True
            t.start()
        for url in self.__urllist:
            self.__queue.put([1, url])
        self.__queue.join()
    
    def abort(self):
        '''
        Safely aborts the crawling threads and saves the downloaded
        webpages
        '''
        for t in self.__threads:
            t.request_stop()

class _CrawlThread(Thread):
    
    def __init__(self, id, queue):
        Thread.__init__(self)
        self.__id = id
        self.__queue = queue
        self.__running = True
        self.__recsys = None
        self.__lib = Library()
    
    def run(self):
        self.__crawl()
    
    def request_stop(self):
        self.__running = False
    
    def __crawl(self):
        while self.__running:
            url = self.__queue.get(True, None)[1]
            print '%d: getting %s' % (self.__id, url)
            try:
                page = fetch_content(url)
            except:
                continue
            self.__update_hrefs(page)
            self.__queue.task_done()
        lib.save('pages')
    
    def __update_hrefs(self, page):
        hrefs = get_hyperlinks(page)
        doc = Document(page)
        shuffle(hrefs)
        print 'found %d new hyperlinks' % len(hrefs)
        for href in hrefs[:50]:
            r = 1
            if self.__recsys:
                r = self.__recsys.rate(doc.content())
            self.__queue.put([r, href])
        self.__lib.add_document(doc)
        

if __name__ == '__main__':
    starttime = time()
    crawler = Crawler(['http://news.google.com'], None)
    crawler.crawl(4)
    print 'finished crawling'
    stoptime = time()
    print 'crawled for %f seconds' % (stoptime-starttime)