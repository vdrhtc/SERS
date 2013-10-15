'''
Created on 08 окт. 2013 г.

@author: gleb
'''
import math

class Grid(object):
    '''
    Represents the system of nodes, conductors and batteries
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        
        
    nodes = []
    wires = []
    
    def draw(self):
        N = int(math.sqrt(len(self.nodes)))
        for row in [self.nodes[i:(i + N)] for i in range(0, N ** 2, N)]:
            for node in row:
                node.draw()
                self.get_wires_from_node(node)[0].draw(N)
            print("")
            for node in row:
                self.get_wires_from_node(node)[1].draw(N)
                print("   ", end='')
            print('')
                 
        
    def get_wires_from_node(self, node): 
        # Array is organized in such a way that horizontal goes first
        wires = ()
        for wire in self.wires:
            if wire.node_from.id == node.id:
                wires += (wire,)
        return wires
    
    def get_wires_to_node(self, node): 
        # Fucntion is organized in such a way that horizontal goes first
        wires = ()
        grid_size = math.sqrt(len(self.nodes))
        for wire in self.wires:
            if wire.node_to.id == node.id:
                wires += (wire,)
        if abs(wires[0].node_from.id - wires[0].node_to.id) < grid_size:
            return wires
        else:
            return wires[1], wires[0]
    
    
