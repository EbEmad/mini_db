import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from index import BPlusTree

class TestBPlusTree(unittest.TestCase):
    def test_insert_and_find(self):
        tree = BPlusTree(order=3)
        
        
        inserts = [(5, "row_0"), (10, "row_1"), (1, "row_2"), (7, "row_3"), (12, "row_4"), (9, "row_5")]
        for key, val in inserts:
            tree.insert(key, val)
            
        
        self.assertEqual(tree.find(5), "row_0")
        self.assertEqual(tree.find(10), "row_1")
        self.assertEqual(tree.find(1), "row_2")
        self.assertEqual(tree.find(7), "row_3")
        self.assertEqual(tree.find(12), "row_4")
        self.assertEqual(tree.find(9), "row_5")
        
        
        self.assertIsNone(tree.find(99))

if __name__ == "__main__":
    unittest.main()
