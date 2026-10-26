import unittest
from tsp_python import tsp_dynamic_programming

class TspTests(unittest.TestCase):
    def test_optimal_cost_and_complete_closed_route(self):
        matrix = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
        cost, path = tsp_dynamic_programming(matrix)
        self.assertEqual(cost, 80)
        self.assertEqual(path[0], path[-1])
        self.assertEqual(len(path), 5)
        self.assertEqual(set(path[:-1]), set(range(4)))
        self.assertEqual(sum(matrix[a][b] for a,b in zip(path,path[1:])), cost)

if __name__ == '__main__':
    unittest.main()
