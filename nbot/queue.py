'''
Created on 27.07.2012

@author: stes
'''

import bisect
from time import sleep
from threading import Lock

class PriorityQueue():
    '''
    Synchronized sorted queue
    
    Enqueues element/priority pairs. The order of the elements in the queue is
    determined by the corresponding priority values
    '''


    def __init__(self):
        '''
        Constructs an empty priority queue
        '''
        self.__queue = []
        self.__lock = Lock()
        self.__open_tasks = 0
    
    def enqueue(self, element, priority):
        '''
        Enqueues the specified element. The given priority value determines the
        position of this particular element in the queue
        
        @param element: the element to be enqueued
        @param priority: the element's priority value
        '''
        with self.__lock:
            #self.__queue.append([priority, element])
            bisect.insort(self.__queue, [priority, element])
    
    def dequeue(self, block=False):
        '''
        Returns the element with the highest priority and removes it from the queue.
        Note that after processing the element, calling task_done() is necessary
        
        @param block: specifies whether the method should block until there is an
        element in the queue
        
        @return: The element with the highest priority within the queue
        '''
        yielding = block
        while yielding:
            sleep(0)
            with self.__lock:
                yielding = block and len(self.__queue) == 0
        with self.__lock:
            if len(self.__queue) > 0:
                self.__open_tasks += 1
                return self.__queue.pop(0)[1]
            return None
    
    def task_done(self):
        '''
        Removes a task opened by the dequeue() method
        '''
        self.__open_tasks -= 1
    
    def join(self):
        '''
        Blocks until the queue is empty and all open tasks are finished
        '''
        while len(self.__queue) > 0 or self.__open_tasks > 0:
            sleep(0)