'''
Created on 24.07.2012

@author: stes
'''

from hashlib import sha1

class Document():
    '''
    Represents a document
    '''
    def __init__(self, content):
        self.__content = content
        self.__hash = sha1(self.__content).hexdigest()
    
    def save(self, path):
        '''
        Stores the document at the specified path in the filesystem
        '''
        pass
    
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

def sort_dic(dic):
    # TODO
    keylist = dic.keys()
    keylist.sort()
    sorted_dic = dict()
    for key in keylist:
        sorted_dic[key] = dic[key]
    return sorted_dic

class Library():
    '''
    a collection of documents, accessible in a key-value fashion
    '''
    def __init__(self, path):
        self.__dict = dict()
    
    def add_document(self, document):
        self.__dict[document.hash()] = document
    
    def get_document(self, sha1):
        return self.__dict.get(sha1)
    
    def sort(self):
        self.__dict = sort_dic(self.__dict)
    
    def __str__(self):
        string = ''
        for item in self.__dict:
            string+= item + ' : ' + self.__dict[item].content() + '\n'
        return string


if __name__ == '__main__':
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