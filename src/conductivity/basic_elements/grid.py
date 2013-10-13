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
    
    def node_equations(self):
        for node in self.nodes[:-1]:
            yield (self.get_wires_to_node(node)[0].current
                  +self.get_wires_to_node(node)[1].current
                  -self.get_wires_from_node(node)[0].current
                  -self.get_wires_from_node(node)[1].current)
    
    def circuit_equations(self):
        """Yeilds circuit equations counter watch"""
        for node in self.nodes[:-1]:
            first_wire = self.get_wires_from_node(node)[1]
            second_node = first_wire.node_to
            second_wire = self.get_wires_from_node(second_node)[0]
            third_node = second_wire.node_to
            third_wire = self.get_wires_to_node(third_node)[1]
            fourth_wire = self.get_wires_from_node(node)[0] 
            yield (first_wire.current/first_wire.conductivity
                   + second_wire.current/second_wire.conductivity
                   - third_wire.current/third_wire.conductivity
                   - fourth_wire.current/fourth_wire.conductivity)
        eq_vertical = 0
        N = int(math.sqrt(len(self.nodes)))
        node_iter = self.nodes[0]
        for _ in range(0, N):
            wire_iter = self.get_wires_from_node(node_iter)[1]
            eq_vertical += wire_iter.current/wire_iter.conductivity-wire_iter.emf
            node_iter = wire_iter.node_to
        yield eq_vertical
        
        eq_horizontal = 0
        node_iter = self.nodes[0]
        for _ in range(0, N):
            wire_iter = self.get_wires_from_node(node_iter)[0]
            eq_horizontal += wire_iter.current/wire_iter.conductivity-wire_iter.emf
            node_iter = wire_iter.node_to
        yield eq_horizontal
