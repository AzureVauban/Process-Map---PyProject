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
    #? instant conversion from dict to list : list(parsecsv().values())[I]
    def testdict_parsesearch(self): #todo finish this
        #! the first head ingredient in the csv file : list(parsecsv().values())[0]
        prime_val = list(createtreefromcsv(list(parsecsv().values())[0]).children_ingredients.values())[2].ingredient_name
        self.assertGreaterEqual(len(prime_val), 5, 'errored')

    def testsearch(self):
        #! add back later recipe : Ingredient = createtreefromcsv(parent_ingredient,False)
        test_list: list = combine_ingredient_tree('')
        self.skipTest('Not implemented')
