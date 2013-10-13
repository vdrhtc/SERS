'''
Created on 09 окт. 2013 г.

@author: gleb
'''

from conductivity.basic_elements.grid import Grid
from conductivity.basic_elements.wire import Wire
from conductivity.basic_elements.node import Node
import sys, sympy 
import random as rnd

    
    
def execute(N, P, verbose=False, silent = False):
    """Fills the grid and builds equations to calculate currents"""
    grid = Grid()
    
    currents_gen = sympy.numbered_symbols('I')
    
    
    def choose_conductivity():
        """Uses given probability to simulate different concentrations of metallic particles"""
        return 1 if rnd.random() < P else 1e-5
    
    def choose_emf(node_from, node_to):
        """Places a battery only in vertical wires"""
        return 0 if abs(node_from.id - node_to.id) < N else 1
    
    def neighborhood_nodes(node):
        """
        Ugly generator that decides whether we should go round the thor 
        to reach the neighborhood node
        """
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
        
        
    grid.nodes = [Node(number_id) for number_id in range(0, N ** 2)]
    
    grid.wires = [Wire(choose_conductivity(),
                       choose_emf(node_from, node_to), 
                       node_from, 
                       node_to,
                       next(currents_gen))
                       for node_from in grid.nodes
                       for node_to in neighborhood_nodes(node_from)]
#     for wire in grid.wires:
#         print(wire)
    if not silent:    
        print(len(grid.wires))
        if N<15:
            grid.draw()
        
    equations = list(grid.circuit_equations())
    equations+= list(grid.node_equations())
    if verbose == True:
        print(list(grid.node_equations()))
        print(list(grid.circuit_equations()))
        
    solution = sympy.solve(equations)#, grid.wires[7].current)
    if verbose == True: print(solution)
    
    if not silent:   
        print('The sum of currents is: ', sum(solution.values()))
    
    return [grid.wires, solution, sum(solution.values())]
    
    
    
if __name__ == '__main__':
    
    execute(int(sys.argv[1]), float(sys.argv[2]), True)
