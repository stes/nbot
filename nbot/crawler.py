'''
Created on 23.07.2012

@author: stes
'''

from nbot.htmlparser import *
from nbot.document import *
from hashlib import sha1
from random import random
from time import time
from time import sleep
from nbot.queue import PriorityQueue
from threading import Thread

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
        self.__queue = PriorityQueue()
        self.__recsys = recsys
        self.__threads = []
        self.__visited = []

    def crawl(self, threads=2, block=True):
        '''
        Starts crawling using the (optional) specified number of threads
        Blocks until crawling is finished if no other option is given
        
        @param threads: The number of threads used for crawling, default is 2
        
        @param block: False, if the method should be non-blocking (True by default)
        '''
        for i in range(threads):
            t = _CrawlThread(i, self.__queue, self.__recsys, self.__visited)
            self.__threads.append(t)
            t.deamon = True
            t.start()
        for url in self.__urllist:
            self.__queue.enqueue(url, 1.)
        self.__queue.join()
    
    def save(self):
        '''
        Sends a request to all running threads to safe the current state of their
        libraries
        '''
        for t in self.__threads:
            t.request_save()
    
    def abort(self):
        '''
        Safely aborts the crawling threads and saves the downloaded
        webpages
        '''
        for t in self.__threads:
            t.request_stop()

class _CrawlThread(Thread):
    
    def __init__(self, id, queue, recsys, visited):
        Thread.__init__(self)
        self.__id = id
        self.__queue = queue
        self.__running = True
        self.__recsys = recsys
        self.__visited = visited
        self.__lib = Library()
        self.__saving = False
    
    def run(self):
        self.__crawl()
    
    def request_stop(self):
        self.__running = False
        
    def request_save(self):
        self.__saving = True
    
    def __crawl(self):
        while self.__running:
            print '%d: %d elements enqueued' % (self.__id, len(self.__queue))
            url = self.__queue.dequeue(True)
            print '%d: getting %s' % (self.__id, url)
            try:
                page = fetch_content(url)
            except:
                continue
            self.__update_hrefs(page, get_host(url))
            self.__queue.task_done()
            if self.__saving:
                self.__saving = False
                self.__lib.save('pages')
            sleep(0)
        self.__lib.save('pages')
    
    def __update_hrefs(self, page, host):
        hrefs = get_hyperlinks(page, host)
        doc = Document(page)
        shuffle(hrefs)
        r = 1
        if self.__recsys != None:
            r = self.__recsys.rate(doc.content())
            print '%d: rated the document with %f' % (self.__id, r)
        else:
            r = random()
        # TODO improve this
        if len(self.__queue) < 100 or r > 0.5:
            print 'found %d new hyperlinks' % len(hrefs)
            for href in hrefs[:50]:
                if not(href in self.__visited):
                    self.__visited.append(href)
                    self.__queue.enqueue(href, r)
        self.__lib.add_document(doc)
        

if __name__ == '__main__':
    starttime = time()
    crawler = Crawler(['http://news.google.com'], None)
    crawler.crawl(4)
    print 'finished crawling'
    stoptime = time()
    print 'crawled for %f seconds' % (stoptime-starttime)