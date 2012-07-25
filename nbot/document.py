'''
Created on 24.07.2012

@author: stes
'''

from hashlib import sha1
import os

def load_document(path):
    '''
    Loads the document at the specified location of the file system
    
    @param path: the path of the document file
    '''
    try:
        with open(path, 'r') as doc:
            content = doc.readlines()
            #TODO improve this? always list?
            return Document(content[0])
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