'''
Created on 23.07.2012

@author: Alex
'''

def read():
    try:
        with open('list.txt', 'r') as listfile:
            return listfile.readlines()
    except IOError:
        return []

def add_site(url):
    try:
        with open('list.txt', 'a') as listfile:
            listfile.write(url + "\n")
    except IOError: pass

def remove_site(url):
    sites = []
    try:
        with open('list.txt', 'r') as listfile:
            sites = listfile.readlines()
    except IOError: return
    
    try:
        sites.remove(url + "\n")
    except ValueError: return
    
    try:
        with open('list.txt', 'w') as listfile:
            listfile.writelines(sites)
    except IOError: return
