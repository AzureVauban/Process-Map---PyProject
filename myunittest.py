import unittest
from random import randint
from main import Ingredient, parsecsv, combine_ingredient_tree, createtreefromcsv


class TestIngredientSearchAndParse(unittest.TestCase):
    # ? instant conversion from dict to list : list(parsecsv().values())[I]
    def testdict_parsesearch(self):  # todo finish this
        #! the first head ingredient in the csv file : list(parsecsv().values())[0]
        prime_val = list(createtreefromcsv(list(parsecsv().values())[0]).children_ingredients.values())[2].ingredient_name
        self.assertEqual(prime_val, 'quantum processor')

    def testsearch(self):
        #! add back later recipe : Ingredient = createtreefromcsv(parent_ingredient,False)
        test_ingredient_name: str = list(createtreefromcsv(list(parsecsv().values())[0]).children_ingredients.values())[2].ingredient_name
        test_ingredient_parent: Ingredient = list(createtreefromcsv(
            list(parsecsv().values())[0]).children_ingredients.values())[2].parent_ingredient
        test_list: list = combine_ingredient_tree(
            test_ingredient_name, test_ingredient_parent)
        self.assertGreaterEqual(2, len(test_list))
        # self.assertEqual(test_ingredient_parent.ingredient_name,'industrial battery')

    def test_createsubtree(self):  # todo finish later
        test_ingredient: Ingredient = create_subtree()
        self.skipTest('test not implemented yet')
    def test_parsesearch_anylevel(self):
        # test the function that will search for any parent ingredient and then search for its children, returns as a list
        parsecsv_anything()
        self.skipTest('test not implemented yet')