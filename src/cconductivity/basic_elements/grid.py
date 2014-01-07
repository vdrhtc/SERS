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
        self.nodes = []
        self.wires = []
        self.dimension = 0
        
        
    
    def draw(self):
        N = int(math.sqrt(len(self.nodes)))
        for row in [self.nodes[i:(i + N)] for i in range(0, N ** 2, N)]:
            for node in row:
                node.draw()
                self.get_wires_from_node(node)[0].draw()
            print("")
            for node in row:
                self.get_wires_from_node(node)[1].draw()
                print("   ", end='')
            print('')
                 
        
    def get_wires_from_node2(self, node): 
        # Array is organized in such a way that horizontal goes first
        wires = ()
        for wire in self.wires:
            if wire.node_from.id == node.id:
                wires += (wire,)
        return wires
    
    def get_wires_from_node(self, node): 
        # Array is organized in such a way that horizontal goes first
        return node.wires_from
    
    def get_wires_to_node2(self, node): 
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
        
    def get_wires_to_node(self, node): 
        # Fucntion is organized in such a way that horizontal goes first
        return node.wires_to
    
    def neighborhood_nodes(self, node):
        """
        Ugly generator that decides whether we should go round the thor 
        to reach the neighborhood node
        """
        grid = self
        N = int(math.sqrt(len(self.nodes)))
        if (node.id+1) % N == 0:
            # Checking if the node is on the right edge
            yield grid.nodes[node.id+1-N] 
            try:
                yield grid.nodes[node.id + N]
            except IndexError:
                #Index error appears only when we go from the bottom to top
                yield grid.nodes[node.id - N**2 + N]
        else:      
            yield grid.nodes[node.id + 1]
            try:
                yield grid.nodes[node.id + N]
            except IndexError:
                #Index error appears only when we go from the bottom to top
                yield grid.nodes[node.id - N**2 + N]
         
    def neighborhood_nodes2(self, node):
        """
        Ugly generator that decides whether we should go round the thor 
        to reach the neighborhood node
        """
        grid = self
        N = int(math.sqrt(len(self.nodes)))
        if (node.id+1) % N == 0:
            # Checking if the node is on the right edge
            yield node.id+1-N
            try:
                grid.nodes[node.id + N]
                yield node.id + N
            except IndexError:
                #Index error appears only when we go from the bottom to top
                yield node.id - N**2 + N
        else:      
            yield node.id + 1
            try:
                grid.nodes[node.id + N]
                yield node.id + N
            except IndexError:
                #Index error appears only when we go from the bottom to top
                yield node.id - N**2 + N
         
