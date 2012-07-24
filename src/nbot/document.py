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

if __name__ == '__main__':
    doc = Document("Dies ist ein Test")
    print doc.content()
    print doc.hash()