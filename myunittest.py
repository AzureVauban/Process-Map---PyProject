import unittest
from random import randint
from main import Ingredient,parsecsv,combine_ingredient_tree,createtreefromcsv
def fib(n: int) -> int:
    if n <= 1:
        return 1
    return fib(n-1)+fib(n-2)


class test_setup(unittest.TestCase):

    def test_setup(self):
        fibelements: list = []
        for _ in range(10):
            fibelements.append(_+1)
        self.assertGreaterEqual(len(fibelements),5)


class TestIngredientSearchAndParse(unittest.TestCase):

    def testdict_parsesearch(self):
        dict_of_head_nodes: dict = parsecsv()
        self.assertGreaterEqual(len(dict_of_head_nodes), 5, 'errored')

    def testsearch(self):
        #! add back later recipe : Ingredient = createtreefromcsv(parent_ingredient,False)
        test_list: list = combine_ingredient_tree('')
        self.skipTest('Not implemented')
