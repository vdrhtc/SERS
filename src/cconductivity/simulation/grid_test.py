'''
Created on 24 окт. 2013 г.

@author: gleb
'''
import unittest, conductivity.simulation.grid_fill_and_solve, conductivity.basic_elements.grid
from conductivity.simulation import grid_fill_and_solve


class Test(unittest.TestCase):


    def test_nodes_from_and_to_2(self):
        grid, equations, currents, eq_matrix, ordinate = grid_fill_and_solve.create_equations(10, 0.5, False, True, True)
#         print(tuple(grid.get_wires_to_node(grid.nodes[2])), 
#                          (tuple(grid.get_wires_to_node2(grid.nodes[2]))))
       
        self.assertEqual(tuple(grid.get_wires_to_node(grid.nodes[9])), 
                         (tuple(grid.get_wires_to_node2(grid.nodes[9]))))
        self.assertEqual(tuple(grid.get_wires_from_node(grid.nodes[9])),
                         tuple(grid.get_wires_from_node2(grid.nodes[9])))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_nodes_from_and_to_2']
    unittest.main()