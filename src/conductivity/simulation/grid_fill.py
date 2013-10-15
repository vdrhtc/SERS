'''
Created on 09 окт. 2013 г.

@author: gleb
'''

from conductivity.basic_elements.grid import Grid
from conductivity.basic_elements.wire import Wire
from conductivity.basic_elements.node import Node
from conductivity.simulation.equationeer import Equationeer as eq
import sys, sympy 
import random as rnd

    
    
def execute(N, P, verbose=False, silent = False):
    """
    Fills the grid, builds equations to calculate currents and solves them
    returns a grid representation in wires, solution dictionary, keys, sum of currents
    """
    grid = Grid()
    
    currents_gen = sympy.numbered_symbols('I')
    currents = [next(currents_gen) for _ in range(0,2*N**2)]
    currents_iter = iter(currents)

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
                       next(currents_iter))
                       for node_from in grid.nodes
                       for node_to in neighborhood_nodes(node_from)]
     
    if verbose:
        for wire in grid.wires:
            print(wire)
             
    if not silent:    
        print(len(grid.wires))
        if N<15:
            grid.draw()
         
    equations = list(eq().circuit_equations(grid))
    if verbose: print(equations)
       
    equations+= list(eq().node_equations(grid))
    if verbose: print(equations)
         
    solution = sympy.solve(equations)#, grid.wires[7].current)
    if verbose: print(solution)
     
    if not silent:   
        print('The sum of currents is: ', sum(solution.values()))
     
    return [grid.wires, solution, currents, sum(solution.values())]
     
    
    
if __name__ == '__main__':
    
    execute(int(sys.argv[1]), float(sys.argv[2]), True)
