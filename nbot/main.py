'''
> nbot

> www.github.com/stes/nbot
> by Redix & stes

> This is the main program routine of nbot, a lightweight and effective web crawler
that autonomously searches the internet for news articles that may be relevant and
interesting for the user.

> Running this script involves loading the urls specified in the corresponding url
list file, creating or loading a recommender system that classifies new pages
depending on user ratings of previously viewed pages and crawling the web for new
potentially interesting articles.
Finally, the results of the search are presented to the user, with the possibility
to rate the new articles, so that the recommender system can give even better results
when run again.

> This program and all parts of it that written by stes and/or Redix are licensed
under the terms of the BSD 3 license, meaning that you are free to redistribute and
modify this software under the following conditions:

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of
    conditions and the following disclaimer.
    
    Redistributions in binary form must reproduce the above copyright notice, this list
    of conditions and the following disclaimer in the documentation and/or other
    materials provided with the distribution.
    
    The names of its contributors may not be used to endorse or promote products
    derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

Note that this software also includes BeautifulSoup 3, a nice HTML parser written
in python licensed by Leonard Richardson (2004-2007). For detailed information,
please refer to the corresponding source file.

We hope you enjoy this software. If you feel like improving it, visit the project
page at github (www.github.com/stes/nbot).

Copyright (c) 2012, Alex Belke, Steffen Schneider
All rights reserved.

@author: stes, Redix
@version: 0.1.0
'''

from random import shuffle
from nbot.recsys import RecommenderSystem
from nbot.crawler import Crawler

__author__ = "stes (stes94@ymail.com), Redix"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2012 stes, Redix"
__license__ = "New-style BSD"

def get_urllist():
    return ['http://news.google.com',
            'http://golem.de'] #replace by proper load function

def train_recsys():
    from nbot.document import Document, Library, VocabList, load_document
    
    doc0 = load_document('res/sample/blubb.html')
    doc1 = load_document('res/sample/page.html')
    doc2 = load_document('res/sample/dislikepage.html')
    
    lib_like = Library()
    lib_like.load('res/like', False)
    lib_dislike = Library()
    lib_dislike.load('res/dislike', False)
    
    like_cv = []
    keys = lib_like.get_keys()
    shuffle(keys)
    for key in keys[:5]:
        like_cv.append(lib_like.rmv_document(key))
    
    dislike_cv = []
    keys = lib_dislike.get_keys()
    shuffle(keys)
    for key in keys[:5]:
        dislike_cv.append(lib_dislike.rmv_document(key))
    
    vlist_like = lib_like.gen_vocablist()
    vlist_dislike = lib_dislike.gen_vocablist()
    
    vlist_like.clean(10)
    vlist_dislike.clean(10)
    
    like_mask = vlist_like.gen_mask()
    dislike_mask = vlist_dislike.gen_mask()
    
    mask = []
    mask.extend(like_mask)
    mask.extend(dislike_mask)
    
    rsys = RecommenderSystem(mask, len(mask))
    for key in lib_like.get_keys():
        doc = lib_like.get_document(key)
        rsys.set_rate(doc.content(), 1.)
    
    for key in lib_dislike.get_keys():
        doc = lib_dislike.get_document(key)
        rsys.set_rate(doc.content(), 0.)
    
    rsys.train(10000000, 0.1)

    likes = lib_like.get_keys()
    shuffle(likes)
    for key in likes[:5]:
        doc = lib_like.get_document(key)
        print rsys.rate(doc.content())
    
    dislikes = lib_dislike.get_keys()
    shuffle(dislikes)
    for key in dislikes[:5]:
        doc = lib_dislike.get_document(key)
        print rsys.rate(doc.content())
    
    print '---------------------------------------'
    print rsys.rate(doc0.content())
    print rsys.rate(doc1.content())
    print rsys.rate(doc2.content())
    print '---------------------------------------'
    print 'CV data'
    print '(1) LIKE'
    for doc in like_cv:
        print rsys.rate(doc.content())
    
    print '(2) DISLIKE'
    for doc in dislike_cv:
        print rsys.rate(doc.content())
    
    # This seems to work, however, more training/cv data will be necessary!  
    
    print '---------------------------------------'
    return rsys

def present_data():
    # TODO
    pass

if __name__ == '__main__':
    # TODO [Redix] load urls from list
    urllist = get_urllist()
    
    # TODO create & train/load a recommender system
    rsys = train_recsys()
    
    # TODO construct a crawler, pass the recommender system and the
    # url list and start crawling
    crawler = Crawler(urllist, rsys)
    crawler.crawl(4)
    
    while True:
        print 'blubb'
    
    # TODO present the received data in some form
    present_data()