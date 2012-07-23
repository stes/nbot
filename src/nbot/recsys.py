'''
Created on 23.07.2012

@author: stes
'''

from numpy import *
from numpy.linalg import *
from htmlparser import *


content = fetch_content('codinghorror.com', '/blog')
#print content
content = remove_spaces(remove_tags(content))
content = content.lower()

i = 0
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

class Dictionary(): 
    '''
    dictionary to store all possible words in order to generate
    a feature vector
    '''   
    
    def __init__(self):
        '''
        Constructor
        '''