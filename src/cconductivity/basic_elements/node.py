'''
Created on 09 окт. 2013 г.

@author: gleb
'''

class Node(object):
    '''
    Represents a node in the grid
    '''

    def __init__(self, id_number = 0):
        '''
        Constructor
        '''
        self.id = id_number
        self.wires_from = [None, None]
        self.wires_to = [None, None]
        
    def __repr__(self):
        return str(self.id)
    
    def draw(self): 
        print('+', end="")