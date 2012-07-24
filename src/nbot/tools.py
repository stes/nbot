'''
Created on 24.07.2012

@author: stes
'''

def print80(text):
    tmp = ''
    for c in text:
        tmp+=c
        if len(tmp) > 80:
            print(tmp)
            tmp = ''
    print(tmp)

def printlist(list):
    for item in list:
        print(item)