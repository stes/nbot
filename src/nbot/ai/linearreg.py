'''
Created on 24.07.2012

@author: stes
'''

from numpy import *
from numpy.linalg import *

class LinearRegression(object):
    '''
    Performs linear regression on a data set
    '''

    def __init__(self, n):
        self.__n = n
        self.__weights = zeros((n, 1))
    
    def estimate(self, X):
        '''
        for each data entry in the data set X, this function returns a hypothesis y
        in the form of a vector
        @return an array containing the estimated values
        '''
        return dot(X, self.__weights)
    
    def train(self, iterations, learnrate, X, Y):
        '''
        learns a parameter vector using the specified training set with the input
        values stored in the 2D-array X and the corresponding outputs in the array
        Y
        '''
        m = size(X, 0)
        old_err = self.error(X, Y)
        new_err = self.error(X, Y)
        i = 0
        while i == 0 or (i < iterations and old_err - new_err > 0.00000001):
            H = self.estimate(X)
            self.__weights -= learnrate / m * dot(X.transpose(), (H - Y))
            i+=1
            old_err = new_err
            new_err = self.error(X, Y)
        print 'finished with error %.5f after %d iterations' % (new_err, i)
    
    def error(self, X, Y):
        m = size(X, 0)
        H = self.estimate(X)
        return 0.5/m * sum((H - Y)**2)

if __name__ == '__main__':
    reg = LinearRegression(2)
    X = array([[1., 0.],
               [1., 2.],
               [1., 4.]])
    Y = array([[0.],
               [4.],
               [8.]])
    print reg.estimate(X)
    reg.train(1000, 0.1, X, Y)
    print reg.estimate(X)
    print reg.estimate(array([[1., 3.]]))