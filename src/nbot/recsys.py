'''
Created on 23.07.2012

@author: stes
'''

from htmlparser import *
from numpy import *
from numpy.linalg import *

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
    return text

class RecommenderSystem():
    '''
    System to rate new pages and estimate the relevance for the user
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def rate(self, document):
        '''
        rates the specified document
        @return: a value between 0 and 1 that specifies how well this
        document suits to the user
        '''
        pass
    
    def set_rate(self, document, rating):
        '''
        Lets the user rate a particular document
        @param rating: The user rating, between 0 (no interest) and 1 (great interest)
        '''
        pass
    
    def train(self, iterations, learnrate):
        '''
        Trains the classifier
        @param iterations: the number of iterations
        @param learnrate: the learning rate
        '''
        pass

class VocabList(): 
    '''
    Vocabulary list used to create a 'bag of words' model out of a given text document.
    '''   
    
    def __init__(self):
        '''
        Constructs a new, empty vocabulary list
        '''
        self.__dict = dict()
    
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
            self.__dict.pop(item)
    
    def __str__(self):
        string = ''
        for item in self.__dict:
            string += "%s : %d\n" % (item, self.__dict[item])
        return string
    
if __name__ == '__main__':
    # some tests
    content = fetch_content('codinghorror.com', '/blog')
    content = preprocess(content)
    tmp = ''
    for c in content:
        tmp+=c
        if len(tmp) > 80:
            print(tmp)
            tmp = ''
    vlist = VocabList()
    vlist.expand_with(content)
    vlist.clean(10)
    print vlist