'''
Created on 23.07.2012

@author: stes
'''

from numpy import *
from numpy.linalg import *
from htmlparser import *

def preprocess(text):
    p = re.compile(r'<script.*?</script>', re.DOTALL)
    text = p.sub('', text)
    p = re.compile(r'<a href.*?</a>', re.DOTALL)
    text = p.sub('hyperlinkk', text)
    text = remove_spaces(remove_tags(text))
    text = text.lower()
    p = re.compile(r'[^a-z\s]', re.DOTALL)
    text = p.sub('', text)
    return text

if __name__ == '__main__':
    content = fetch_content('codinghorror.com', '/blog')
    content = preprocess(content)
    tmp = ''
    for c in content:
        tmp+=c
        if len(tmp) > 80:
            print(tmp)
            tmp = ''

class RecommenderSystem():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

class VocabList(): 
    '''
    dictionary to store all possible words in order to generate
    a feature vector
    '''   
    
    def __init__(self):
        '''
        Constructor
        '''