'''
Created on 24.07.2012

@author: stes
'''

from hashlib import sha1
from operator import itemgetter
import string
import os
import re
from nbot.htmlparser import *
from stemming.porter import stem

def preprocess(text):
    '''
    preprocesses the given text before feeding it to the classification
    system
    '''
    p = re.compile(r'<script.*?</script>', re.DOTALL)
    text = p.sub('', text)
    p = re.compile(r'<a href.*?</a>', re.DOTALL)
    #TODO use some better name for this
    text = p.sub('hyperlinkk', text)
    text = remove_spaces(remove_tags(text))
    text = text.lower()
    p = re.compile(r'[^a-z\s]', re.DOTALL)
    text = p.sub('', text)
    
    stemmed_text = ''
    for word in text.split():
        stemmed_text += stem(word) + " "
    return stemmed_text

def load_document(path):
    '''
    Loads the document at the specified location of the file system
    
    @param path: the path of the document file
    '''
    try:
        with open(path, 'r') as doc:
            content = doc.readlines()
            #TODO improve this? always list?
            return Document(string.join(content))
    except IOError:
        pass

class Document():
    '''
    A text document
    '''
    def __init__(self, content):
        '''
        Constructs a new Document with the specified content and generates
        the corresponding sha1 hash
        
        @param content: the document content
        '''
        self.__content = content
        self.__hash = sha1(self.__content).hexdigest()
    
    def save(self, path):
        '''
        Stores the document at the specified path in the file system
        '''
        savef = open(path, 'w')
        savef.write(self.__content)
        savef.close()
    
    def hash(self):
        '''
        Returns a hash representing this document
        @return: a hash representing this document
        '''
        return self.__hash
    
    def content(self):
        '''
        Returns the content of this document
        @return: the content of this document
        '''
        return self.__content

class VocabList(): 
    '''
    Vocabulary list used to create a 'bag of words' model out of a given text document.
    '''   
    
    def __init__(self):
        '''
        Constructs a new, empty vocabulary list
        '''
        self.__dict = dict()
        self.__totalwords = 0
    
    def expand_with(self, text):
        '''
        expands the vocabulary list using the specified (preprocessed) text
        @param text: the text whose words should be added to the vocabulary list
        '''
        for word in text.split():
            if self.__dict.has_key(word):
                self.__dict[word] += 1
            else:
                self.__dict[word] = 1
            self.__totalwords += 1
    
    def clean(self, threshold):
        '''
        removes all entries with a quantity less or equals the threshold value
        @param threshold: the threshold
        '''
        rmv = []
        for item in self.__dict:
            if (self.__dict[item] <= threshold):
                rmv.append(item)
        for item in rmv:
            self.__totalwords -= self.__dict[item]
            self.__dict.pop(item)
    
    def gen_mask(self):
        '''
        Generates an array with a list of all words in this vocabulary list
        '''
        array = []
        for item in self.sort():
            array.append(item[0])
        return array        
    
    def sort(self):
        '''
        Returns a sorted dictionary containing the elements of this dictionary
        '''
        return sorted(self.__dict.items(), key=itemgetter(1), reverse=True)
    
    def quantity_of(self, word):
        '''
        Returns the number of occurrences of the specified word in the texts
        added to this vocabulary list so far
        
        @param word: the word
        
        @param return: the quantity of the specified word, 0 if not in the list
        '''
        if not self.__dict.has_key(word):
            return 0
        return self.__dict[word]
    
    def get_total_word_count(self):
        return self.__totalwords
    
    def __str__(self):
        string = ''
        for item in self.__dict:
            string += "%s : %d\n" % (item, self.__dict[item])
        return string

def __sort_dic(dic):
    # TODO
    keylist = dic.keys()
    keylist.sort()
    sorted_dic = dict()
    for key in keylist:
        sorted_dic[key] = dic[key]
    return sorted_dic

class Library():
    '''
    A collection of documents, accessible in a key-value fashion
    '''
    def __init__(self):
        '''
        Constructs a new, empty library
        '''
        self.__dict = dict()
    
    def add_document(self, document):
        '''
        Adds the specified document to this library
        
        @param document: the document to be added
        '''
        self.__dict[document.hash()] = document
    
    def get_document(self, sha1):
        '''
        Returns the document corresponding to the specified sha1 hash
        
        @param sha1: the sha1 hash of the document that should be returned
        
        @return: the document with the specified sha1 hash
        '''
        return self.__dict.get(sha1)
    
    def get_keys(self):
        return self.__dict.keys()
    
    def sort(self):
        '''
        Sorts the documents in this library according to their sha1 hashes
        '''
        self.__dict = __sort_dic(self.__dict)
    
    def save(self, path):
        '''
        Stores the documents in this library in the specified directory 
        '''
        for item in self.__dict:
            doc = self.__dict[item]
            doc.save(os.path.join(path, item))
    
    def load(self, path, check_hash = True):
        '''
        loads the documents stored in the specified place in the file system
        
        @param path: the path were the documents are stored
        @param check_hash: True, if documents should only be added if their
        filename corresponds to their sha1 hash 
        '''
        for filename in os.listdir(path):
            doc = load_document(os.path.join(path, filename))
            if (not check_hash) or filename == doc.hash():
                self.add_document(doc)
    
    def gen_vocablist(self):
        vlist = VocabList()
        for doc in self.__dict.values():
            content = preprocess(doc.content())
            vlist.expand_with(content)
        return vlist
    
    def __str__(self):
        string = ''
        for item in self.__dict:
            string+= item + ' : ' + self.__dict[item].content() + '\n'
        return string

# some test routines
if __name__ == '__main__':
    lib = Library('foo')
    lib.load('res')
    print lib
    '''
    doc1 = Document("Dies ist ein Test")
    print doc1.content(), doc1.hash()
    doc2 = Document("Dies ist ein weiterer Test")
    print doc2.content(), doc2.hash()
    lib = Library('/foo')
    lib.add_document(doc1)
    lib.add_document(doc2)
    lib.add_document(Document('blubb'))
    lib.add_document(Document('blubb2'))
    lib.add_document(Document('blubb3'))
    sdoc = lib.get_document('46d35759feded708ecd4ac98368f9d4d0c2b61fd')
    print 'fetched doc: ', sdoc.content()
    print str(lib)
    lib.sort()
    print str(lib)
    lib.save('res')
    '''