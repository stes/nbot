'''
Created on 23.07.2012

@author: stes
'''

from src.nbot.htmlparser import *

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
        while q:
            url = q.pop(0)
            page = fetch_content(url)
            q.extend(get_hyperlinks(page))
        # TODO