'''
Created on 15 окт. 2013 г.

@author: vdrhtc
'''
import sympy, math
from numpy import *


class Equationeer(object):
    '''
    Operates with equations of the model
    '''
    def lsystem_to_matrix_and_ordinate(self, equations, variables):
        B = []
        b = [0 for _ in range(len(variables))]
             
        for i in range(len(equations)):
            b[i] = -equations[i].as_independent(*variables)[0]            
            B.append([])
             
            for j in range(len(variables)):
                B[i].append(equations[i].coeff(variables[j]))
                
        return sympy.Matrix(B), b
    
    
    def create_equation_matrix_and_ordinate(self, variables, grid):

        """A very, very, very ugly (but fast) piece of code based on operations in methods cirquit_ and node_equations"""
       
        B = zeros((len(variables),len(variables)))
        b = zeros(len(variables))
        vardict = dict(zip(variables, range(len(variables))))
        
        i=0
        for node in grid.nodes[:-1]:
            j1 = vardict[grid.get_wires_to_node(node)[0].current]
            B[i][j1] = 1
             
            j2 = vardict[grid.get_wires_to_node(node)[1].current]
            B[i][j2] = 1
             
            j3 = vardict[grid.get_wires_from_node(node)[0].current]
            B[i][j3] = -1
             
            j4 = vardict[grid.get_wires_from_node(node)[1].current]
            B[i][j4] = -1
             
            i+=1
             
            first_wire = grid.get_wires_from_node(node)[1]
            second_node = first_wire.node_to
            second_wire = grid.get_wires_from_node(second_node)[0]
            third_node = second_wire.node_to
            third_wire = grid.get_wires_to_node(third_node)[1]
            fourth_wire = grid.get_wires_from_node(node)[0] 
             
            j1 = vardict[first_wire.current]
            B[i][j1] = 1/first_wire.conductivity
             
            j2 = vardict[second_wire.current]
            B[i][j2] = 1/second_wire.conductivity
             
            j3 = vardict[third_wire.current]
            B[i][j3] = -1/third_wire.conductivity
             
            j4 = vardict[fourth_wire.current]
            B[i][j4] = -1/fourth_wire.conductivity
             
            i+=1
             
        N = int(math.sqrt(len(grid.nodes)))
        node_iter = grid.nodes[0]
        bi = 0
        for _ in range(0, N):
             
            wire_iter = grid.get_wires_from_node(node_iter)[1]
             
            j1 = vardict[wire_iter.current]
            B[i][j1] = 1/wire_iter.conductivity
             
            bi += wire_iter.emf
            node_iter = wire_iter.node_to
             
        b[i] = bi
         
        i+=1
        bi=0
        node_iter = grid.nodes[0]
         
        for _ in range(0, N):
            wire_iter = grid.get_wires_from_node(node_iter)[0]
             
            j1 = vardict[wire_iter.current]
            B[i][j1] = 1/wire_iter.conductivity
             
            bi += wire_iter.emf
            node_iter = wire_iter.node_to
             
        b[i] = bi
        return B, b
       
    def node_equations(self, grid):
        for node in grid.nodes[:-1]:
            yield (grid.get_wires_to_node(node)[0].current
                  +grid.get_wires_to_node(node)[1].current
                  -grid.get_wires_from_node(node)[0].current
                  -grid.get_wires_from_node(node)[1].current)
    
    def circuit_equations(self, grid):
        """Yields circuit equations counter watch"""
        for node in grid.nodes[:-1]:
            first_wire = grid.get_wires_from_node(node)[1]
            second_node = first_wire.node_to
            second_wire = grid.get_wires_from_node(second_node)[0]
            third_node = second_wire.node_to
            third_wire = grid.get_wires_to_node(third_node)[1]
            fourth_wire = grid.get_wires_from_node(node)[0] 
            yield (first_wire.current/first_wire.conductivity
                   + second_wire.current/second_wire.conductivity
                   - third_wire.current/third_wire.conductivity
                   - fourth_wire.current/fourth_wire.conductivity)
        eq_vertical = 0
        N = int(math.sqrt(len(grid.nodes)))
        node_iter = grid.nodes[0]
        for _ in range(0, N):
            wire_iter = grid.get_wires_from_node(node_iter)[1]
            eq_vertical += wire_iter.current/wire_iter.conductivity-wire_iter.emf
            node_iter = wire_iter.node_to
        yield eq_vertical
        
        eq_horizontal = 0
        node_iter = grid.nodes[0]
        for _ in range(0, N):
            wire_iter = grid.get_wires_from_node(node_iter)[0]
            eq_horizontal += wire_iter.current/wire_iter.conductivity-wire_iter.emf
            node_iter = wire_iter.node_to
        yield eq_horizontal 
