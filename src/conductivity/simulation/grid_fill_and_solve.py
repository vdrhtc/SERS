'''
Created on 09 окт. 2013 г.

@author: gleb
'''

from conductivity.basic_elements.grid import Grid
from conductivity.basic_elements.wire import Wire
from conductivity.basic_elements.node import Node
from conductivity.simulation.equationeer import Equationeer as eq
import sys, sympy, numpy, time, scipy.sparse.linalg as ssl
import random as rnd


def solve(equations, variables, eq_matrix, ordinate, symbolic=False):
    """
    Solves symbolically or numerically given equations
    """
    if not symbolic:
        solution = ssl.spsolve(eq_matrix, ordinate) 
        solution = dict(zip(variables, solution))
        return [solution, variables, sum(solution.values())]
    else:
        solution = sympy.solve(equations)
        return [solution, variables, sum(solution.values())]
    
def execute_fill(matrix_dimension, P, verbose=False, silent = False, fast = True, sm = 9, sd = 1):
    """
    Fills the grid, builds equations to calculate currents and 
    returns the grid, symbolic equations, variables and the numerical representation of the equations
    """
    grid = Grid()
    
    currents_gen = sympy.numbered_symbols('I')
    currents = [next(currents_gen) for _ in range(0,2*matrix_dimension**2)]
    currents_iter = iter(currents)

    def choose_conductivity(sm, sd):
        """Uses given probability to simulate different concentrations of metallic particles"""
        return sm if rnd.random() < P else sd
    
    def choose_emf(node_from, node_to):
        """Places a battery only in vertical wires"""
        return 0 if abs(node_from.id - node_to.id) < matrix_dimension else 1
    
   
    grid.nodes = [Node(number_id) for number_id in range(0, matrix_dimension ** 2)]
    
    i=0
    for node_from in grid.nodes:
        for node_to_id in grid.neighborhood_nodes2(node_from):
            wire = Wire(grid, choose_conductivity(sm, sd),
                       choose_emf(node_from, grid.nodes[node_to_id]), 
                       node_from, 
                       grid.nodes[node_to_id],
                       next(currents_iter))
            grid.wires.append(wire)
            if wire.horizontal: 
                grid.nodes[i].wires_from[0] = wire
                grid.nodes[node_to_id].wires_to[0] = wire
            else: 
                grid.nodes[i].wires_from[1] = wire           
                grid.nodes[node_to_id].wires_to[1] = wire
        i+=1
            
     
    if verbose:
        for wire in grid.wires:
            print(wire)
             
    if not silent:    
        print(len(grid.wires))
        if matrix_dimension<15:
            grid.draw()
     
    if not fast:    
        equations1 = list(eq().circuit_equations(grid))
        if verbose: print(equations1)
        
        equations2 = list(eq().node_equations(grid))
        if verbose: print(equations2)
        
        equations = equations1+equations2
    
        eq_matrix, ordinate = eq().lsystem_to_matrix_and_ordinate(equations, currents)
    else:
        eq_matrix, ordinate = eq().create_equation_matrix_and_ordinate(currents, grid)
        equations = None
    return grid, equations, currents, eq_matrix, ordinate
        
    
if __name__ == '__main__':
    grid, equations, currents, eq_matrix, ordinate = execute_fill(int(sys.argv[1]), float(sys.argv[2]), False, fast=True)
    print("The sum of currents is: ", (solve(equations, currents, eq_matrix, ordinate, False))[-1])