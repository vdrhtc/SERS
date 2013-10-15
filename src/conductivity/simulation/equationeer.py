'''
Created on 15 окт. 2013 г.

@author: vdrhtc
'''
import sympy, math


class Equationeer(object):
    '''
    Operates with equations of the model
    '''
    def lsystem_to_matrix_and_ordinate(self, equations, vars_list):
        B = []
        b = [0 for _ in range(len(vars_list))]
             
        for i in range(len(equations)):
            b[i] = -equations[i].as_independent(*vars_list)[0]            
            B.append([])
             
            for j in range(len(vars_list)):
                B[i].append(equations[i].coeff(vars_list[j]))
                
        return sympy.Matrix(B), b
    
    def node_equations(self, grid):
        for node in grid.nodes[:-1]:
            yield (grid.get_wires_to_node(node)[0].current
                  +grid.get_wires_to_node(node)[1].current
                  -grid.get_wires_from_node(node)[0].current
                  -grid.get_wires_from_node(node)[1].current)
    
    def circuit_equations(self, grid):
        """Yeilds circuit equations counter watch"""
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