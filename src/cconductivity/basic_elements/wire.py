'''
Created on 08 окт. 2013 г.

@author: gleb
'''

import math

class Wire(object):
    '''
    Represents wire object with arbitrary conductivity
    '''
    
    def __init__(self, grid, conductivity = 1, conductor=True, emf = 0, node_from = None, node_to = None, current=0):
        '''
        Constructor
        '''
        self.conductivity = conductivity
        self.emf = emf
        self.node_from = node_from
        self.node_to = node_to
        self.current = current
        self.horizontal = True if abs(node_from.id - node_to.id)< math.sqrt(len(grid.nodes)) else False
        self.conductor = conductor
        
        
    def __repr__(self):
        return "<Class: Wire, conductivity = " + str(self.conductivity)+ ", conductor = " + str(self.conductor) + ", current = " + str(self.current) + ", (From, To) = " + str(( self.node_from, self.node_to)) + ">"
    
    def draw(self):
        if self.horizontal:
            if self.emf == 0:
                print("---", end = '') if self.conductor else print("   ", end = '')
            elif self.emf > 0:
                print("->-", end = '') if self.conductor else print("   ", end = '')
            else:
                print("-<-", end = '') if self.conductor else print("   ", end = '')
            
        else:
            if self.emf == 0:
                print("|", end = '') if self.conductor else print(" ", end = '')
            elif self.emf > 0:
                print("V", end = '') if self.conductor else print(" ", end = '')
            else:
                print("^", end = '') if self.conductor else print(" ", end = '')


            