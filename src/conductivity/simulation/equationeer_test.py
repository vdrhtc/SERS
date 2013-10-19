'''
Created on 15 окт. 2013 г.

@author: vdrhtc
'''
import unittest, sympy
from sympy import Matrix
from conductivity.simulation.equationeer import Equationeer
from conductivity.simulation.grid_fill_and_solve import execute_fill


class Test(unittest.TestCase):

    def test_create_equation_matrix_and_ordinate(self):
        '''Should make a corresponding matrix from grid'''
        grid, equations, currents, eq_matrix, ordinate = execute_fill(10, 0.8, silent=True, fast=False)
        B, b = Equationeer().create_equation_matrix_and_ordinate(currents, grid)
        
        
        #self.assertEqual(eq_matrix, B)
        self.assertEqual(sum(ordinate), sum(b))
    
    def test_lsystem_to_matrix_and_ordinate(self):
        '''Should make a corresponding matrix from linear equations'''
        A = sympy.Matrix([[1,1,1], [1,0,2], [1,11,3]])
        a = [-2, 0, 0]
        vars_gen = sympy.numbered_symbols('V')
        vars_list= [next(vars_gen) for _ in range(0,3)]
        equations = [vars_list[0]+vars_list[1]+vars_list[2]+2,
                     vars_list[0]+2*vars_list[2],
                     vars_list[0]+11*vars_list[1]+3*vars_list[2]]
        
        B, b = Equationeer().lsystem_to_matrix_and_ordinate(equations, vars_list)
        print(B)
        self.assertEqual(A, B)
        self.assertEqual(a, b)

if __name__ == "__main__":
    unittest.main()