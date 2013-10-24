'''
Created on 08 окт. 2013 г.

@author: gleb
'''
import conductivity.basic_elements.grid, math
from conductivity.basic_elements import grid

class Wire(object):
    '''
    Represents wire object with arbitrary conductivity
    '''
    
    def __init__(self, grid, conductivity = 1, emf = 0, node_from = None, node_to = None, current=0):
        '''
        Constructor
        '''
        self.conductivity = conductivity
        self.emf = emf
        self.node_from = node_from
        self.node_to = node_to
        self.current = current
        self.horizontal = True if abs(node_from.id - node_to.id)<math.sqrt(len(grid.nodes)) else False
        
        
    def __repr__(self):
        return "<Class: Wire, conductivity = " + str(self.conductivity)+ ", current = " + str(self.current) + ", (From, To) = " + str(( self.node_from, self.node_to)) + ">"
    
    def draw(self, grid_size):
        if abs(self.node_from.id - self.node_to.id) < grid_size:
            print("---", end = '') if self.conductivity == 1 else print("   ", end = '')
        else:
            print("V", end = '') if self.conductivity == 1 else print(" ", end = '')
            