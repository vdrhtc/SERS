'''
Created on 09 окт. 2013 г.

@author: gleb
'''


from cconductivity.basic_elements.grid import Grid
from cconductivity.basic_elements.node import Node
from cconductivity.basic_elements.wire import Wire
from cconductivity.simulation.equationeer import Equationeer as eq
import random as rnd
import scipy
import scipy.sparse as ss
import scipy.sparse.linalg as ssl
import sympy
import sys

def solve(equations, variables, eq_matrix, ordinate, symbolic=False):
    """
    Solves symbolically or numerically given equations
    """
    if not symbolic:
        solution = ssl.spsolve(ss.csr_matrix(eq_matrix), ordinate) 
        solution = dict(zip(variables, solution))
        return [solution, sum(solution.values())]
    else:
        solution = sympy.solve(equations)
        return [solution, variables, sum(solution.values())]
    

def calculate_em(frequency):
    J = 1J
    e_b = 5
    omega_p = 9.1
    omega_tau = 0.02
    return e_b - (omega_p / frequency) ** 2 / (1 + (omega_tau / frequency) * J)

def calculate_sm(frequency):
    j = 1j 
    return -j * frequency * calculate_em(frequency) / 4 / scipy.pi

   

def change_emfs(old_grid, new_emfs):
    """
    Takes an old grid and replaces old emfs with ones from the new_emfs array (2n^2 x 1) 
    """
    for new_emf in new_emfs:
        next(iter(grid.wires)).emf = new_emf
    

    
def change_frequency(old_grid, frequency):
    em = calculate_em(frequency)
    for wire in old_grid.wires:
        if wire.conductivity != 1:
            wire.conductivity = em
    
    
def generate_grid(matrix_dimension, P,  frequency=1.02, ed=1):    
    
    grid = Grid()
    
    def choose_conductivity(em, ed):
        """Uses given probability to simulate different concentrations of metallic particles"""
        return (em, True) if rnd.random() < P else (ed, False)
    
    def choose_emf(node_from, node_to):
        """Places a battery only in vertical wires"""
        return 0 if abs(node_from.id - node_to.id) < matrix_dimension else 1
    
    
    em = calculate_em(frequency)
    print(em)

   

    currents_gen = sympy.numbered_symbols('I')
    currents = [next(currents_gen) for _ in range(0, 2 * matrix_dimension ** 2)]
    currents_iter = iter(currents) 
    
    
    
    grid.nodes = [Node(number_id) for number_id in range(0, matrix_dimension ** 2)]
    
    
    i = 0
    for node_from in grid.nodes:
        for node_to_id in grid.neighborhood_nodes2(node_from):
            conductivity, conductor = choose_conductivity(em, ed)
            wire = Wire(grid, conductivity, conductor,
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
        i += 1
    
    grid.dimension = matrix_dimension
    return grid, currents

    
def create_equations(matrix_dimension, P, verbose=False, silent=False, fast=True, frequency=1.02, ed=1):
    """
    Fills the grid, builds equations to calculate currents and 
    returns the grid, symbolic equations, variables and the numerical representation of the equations
    """
    grid, currents = generate_grid(matrix_dimension, P, frequency, ed)
     
    print_grid_info(verbose, silent, grid)
     
    if not fast:    
        equations1 = list(eq().circuit_equations(grid))
        if verbose: print(repr(equations1))
        
        equations2 = list(eq().node_equations(grid))
        if verbose: print(equations2)
        
        equations = equations1 + equations2
    
        eq_matrix, ordinate = eq().lsystem_to_matrix_and_ordinate(equations, currents)
    else:
        eq_matrix, ordinate = eq().create_equation_matrix_and_ordinate_low_memory(currents, grid)
        equations = None

    return grid, equations, currents, eq_matrix, ordinate
        
        
def print_grid_info(verbose, silent, grid):
    if verbose:
        for wire in grid.wires:
            print(wire)
             
    if not silent:    
        print(len(grid.wires))
        if grid.dimension < 15:
            grid.draw()
    
if __name__ == '__main__':
    grid, equations, currents, eq_matrix, ordinate = create_equations(int(sys.argv[1]), float(sys.argv[2]), False, fast=True)
    print("The conductivity is: ", (solve(equations, currents, eq_matrix, ordinate, False))[-1] / len(currents) * 2)
