'''
Created on Oct 3, 2012

@author: stes
'''

import os
import metakit
from nbot import htmlparser
from nbot.document import Document, Library, preprocess, VocabList


FEED_DIR = os.path.expanduser('~/.kde4/share/apps/akregator/Archive')
__verbose__ = False

class Ratings(object):
    def __init__(self, savefile):
        self.__savepath__ = savefile
        self.__dictionary__ = dict()
        self.__load__()
    
    def __load__(self):
        if os.path.exists(self.__savepath__):
            try:
                f = open(self.__savepath__)
                for line in f.readlines():
                    [key, value] = line.split(',')
                    self.__dictionary__[int(key)] = int(value)
                f.close()
            except:
                log('loading failed', False)
    
    def __save__(self):
        f = open(self.__savepath__, 'w')
        f.write(str(self))
        f.flush()
        f.close()
        
    def set_rating(self, hash, rating):
        self.__dictionary__[hash] = rating
    
    def get_rating(self, hash):
        return self.__dictionary__[hash]
      
    def __str__(self):
        s = ''
        for keys in self.__dictionary__.keys():
            s += '%d,%d\n' % (keys, self.__dictionary__[keys])
        return s
    
    def __del__(self):
        self.__save__()

def read_database(db):
    '''
    reads the specified metakit database
    '''
    data = db.getas("articles[guid:S,title:S,\
    hash:I,guidIsHash:I,guidIsPermaLink:I,\
    description:S,link:S,comments:I,\
    commentsLink:S,status:I,pubDate:I,\
    tags[tag:S],hasEnclosure:I,enclosureUrl:S,\
    enclosureType:S,enclosureLength:I,\
    categories[catTerm:S,catScheme:S,catName:S],\
    authorName:S,content:S,authorUri:S,authorEMail:S]")

    return data

def read_data(feed, download=False):
    # download the feed
    log('fetch feed: %s' % feed.title)
    content = feed.description
    if download:
        content = htmlparser.fetch_content(feed.link)
    doc = Document(preprocess(content))
    log('content:\n%s' % content)
    return doc

def log(message, verboseonly=True):
    if __verbose__ or not verboseonly:
        print message

def test_db():
    gl_vlist = VocabList()
    log('searching directory: %s' % FEED_DIR)
    for dir in os.listdir(FEED_DIR):
        if '.mk4' in dir[-4:]:
            log('found database: %s' % dir)
            # open database
            db = metakit.storage(os.path.join(FEED_DIR, dir), 0)
            data = read_database(db)
            if len(data) > 0:
                # feed content in database
                log('create library')
                lib = Library()
                for feed in data:
                    lib.add_document(read_data(feed))
                vlist = lib.gen_vocablist()
                vlist.clean(5)
                gl_vlist.merge(vlist)
            db = None # close database
    print gl_vlist

def test_dict():
    r = Ratings(os.path.expanduser('nbot_ratings'))
    print r
    r.set_rating(25425, 1)
    r.set_rating(25634, 7)
    r.set_rating(12541, 7)
    r.set_rating(77412, 1)
    print r
    
if __name__ == '__main__':
    test_db()