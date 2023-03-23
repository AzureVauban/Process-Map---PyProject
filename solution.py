"""
Reworked Process Map with needed changes:
Improved Recursive math method
- calculation with floats

Reworked csv parsing and writing
- parsing works at any level from any node
- ability to organize recipes into groups with their own unique string key
- commands
- - view (render the recipe tree into the console)
- - rename (any ingredient in the recipe)
- - edit (have the user select which node they want to edit)

# FORMAT TO PEP8 STANDARDS
"""

from time import sleep
from random import randint, choice
valid_commands_list: list = ['--help',  # outputs a list of commands
                                        # for the user*
                             '--view',  # renders the local branch of the
                                        # recipe tree*
                             '--edit',  # output a list of Nodes in the
                                        # recipe tree and prompts the user to
                                        # choose one to modify*
                             '--preview'  # outputs a list of Nodes in the
                                          # recipe tree and prompts the
                                          # user to choose one to preview
                                          # the resulting amount*
                             ]  # commands with * in the desc should be used during the populate method


def generate_settings_file() -> None:
    return None


class Queue:
    class Node:
        index: int
        data = None
        after = None
        before = None

        def __init__(self, before, data, after) -> None:
            self.before = before
            self.data = data
            self.after = after
            self.index = 0

    head: Node = None
    size: int = 0
    max_size: int = 0

    def __init__(self, max_size=None) -> None:
        self.head = None
        self.size = 0
        self.max_size = max_size

    def __get_end(self) -> Node:
        """get the endpoint node of the container instance"""
        current: self.Node = self.head
        while current.after is not None:
            current = current.after
        return current

    def __set_index(self):
        """set the index of all the nodes"""
        if not self.is_empty():
            current: self.Node = self.head
            new_index: int = 0
            while current.after is not None:
                current.index = new_index
                current = current.after
                new_index += 1

    @classmethod
    def __check_data_typing(cls, old_node: Node, new_data):
        """make sure that the data being added is the same type"""
        if not isinstance(old_node.data, type(new_data)):
            raise TypeError('data is not an instance of', type(old_node.data))

    def is_empty(self) -> bool:
        """checks if there is any data in the container instance"""
        return self.head is None

    def is_full(self) -> bool:
        """checks if the max amount of values are present in the container"""
        if self.max_size is not None:
            return self.size > self.max_size
        return False

    def enqueue(self, data):
        """add data to the back of the container instance"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = self.Node(None, data, None)
        else:
            # append a new node to the end of the container instance
            old_endpoint: self.Node = self.__get_end()
            self.__check_data_typing(old_endpoint, data)
            # link Node pointers of old and new endpoint
            new_endpoint: self.Node = self.Node(old_endpoint, data, None)
            old_endpoint.after = new_endpoint
        # set the new indicies
        self.__set_index()
        # change the size of the container instance
        self.size += 1

    def dequeue(self) -> None:
        """remove data from the back of the container instance"""
        if self.is_empty():
            raise ValueError('cannot pop any values from an empty container')
        if self.is_full():
            raise ValueError("The container is full")
        old_head_node: self.Node = self.head
        return_data = old_head_node.data
        new_head_node: self.Node = None
        if old_head_node.after is not None:
            new_head_node = old_head_node.after
            new_head_node.before = None
        self.head = new_head_node
        del old_head_node
        self.size -= 1
        # set the new indicies
        self.__set_index()
        return return_data


class Base:
    # TODO ADD/IMPORT
    name: str = 'None'
    on_hand: float = 0
    needed_per_craft: float = 0  # quantity of item it takes to craft resultant once
    # todo determine if resultant_made_per_craft type should be a float/int
    resultant_made_per_craft: int = 0  # quantity of resultant made per craft
    resultant_resulted: float = 0  # quantity of resultant made

    def __init__(self, name: str = '',
                 on_hand: float = 0,
                 needed_per_craft: float = 1,
                 parent_made_per_craft: float = 0) -> None:
        self.name = name
        self.on_hand = on_hand
        self.needed_per_craft = needed_per_craft
        self.resultant_made_per_craft = parent_made_per_craft
        self.resultant_resulted = 0


class Ingredient(Base):
    # TODO ADD/IMPORT
    parent = None  # todo rename to parent
    children: list = []

    def __init__(self, name: str = '',
                 parent=None,
                 on_hand: float = 0,
                 needed_per_craft: float = 1,
                 parent_made_per_craft: float = 0) -> None:
        super().__init__(name, on_hand, needed_per_craft, parent_made_per_craft)
        if parent is not None and not isinstance(parent, Ingredient):
            raise TypeError('Parent must be', None,
                            'or and instance of', Ingredient)
        self.parent = parent
        self.children = []


class Recipe:
    # TODO ADD/IMPORT
    resultant_item: Ingredient = None
    group_identifer_key: str = 'N/A'
    population: int = 0

    def __init__(self, ingredient: Ingredient) -> None:
        if not isinstance(ingredient, Ingredient):
            raise TypeError(
                'input ingredient node must be an instance of', Ingredient)
        self.resultant_item = head(ingredient)


def promptint(default_input_to_one: bool = False) -> int:
    """
    prompts the user for an postive integer and returns it
    Returns:
        int: postive integer from user input
    """
    while True:
        myinput = input('').strip()
        if len(myinput) == 0 and default_input_to_one:  # todo check this
            return 1
        elif len(myinput) == 0 and not default_input_to_one:  # todo check this
            return 0
        elif not myinput.isdigit():
            print('you can only type in a positive integer')
        elif int(myinput) < 0:
            print('please type in a postive integer')
        else:
            return int(myinput)


def head(current: Ingredient) -> Ingredient:
    """
    traverse to the parent-most Ingredient
    Args:
        current (Ingredient): starting Ingredient
    Returns:
        Ingredient: parent most Ingredient of the starting Ingredient
    """
    while current.parent is not None:
        current = current.parent
    return current


def trail(ingredient: Ingredient):
    """
    print the ingredient trail leading up to the parent most Ingredient
    Args:
        ingredient (Ingredient): starting Ingredient
    """
    print('TRAIL: ', end='')
    while True:
        if ingredient.parent is not None:
            print(ingredient.name, '-> ', end='')
            ingredient = ingredient.parent
        else:
            print(ingredient.name)
            break


def RAND_STR_GEN(maxlength: int = randint(10, 20)) -> str:
    """
    generate a unique tree key of random alphumeric characters
    """
    treekey = ''
    for _ in range(0, maxlength):
        treekey += choice(
            '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return treekey


def command_prompt(command_string_input: str,  # command string
                   ingredient: Ingredient,  # ingredient Node
                   preview : Ingredient # preview recipe Node
                   ):
    if command_string_input == '--help':
        help_recipe()
    elif command_string_input == '--view':
        view_recipe()
    elif command_string_input == '--edit':
        # parse through the recipe tree and prompt the user if they want to edit a node
        edit_recipe(head(preview))  # TODO finish (disable for now, 0-print)
    elif command_string_input == '--preview':
        preview_recipe(head(preview_recipe))
    else:
        print('not a valid command')


def help_recipe():
    pass


def view_recipe():
    pass


def parse_and_enqueue(ingredient: Ingredient,
                      enqueued_recipe: list) -> list:
    parse_and_enqueue.append(enqueued_recipe)
    for child in ingredient.children:
        parse_and_enqueue(child, enqueued_recipe)
    
    return enqueued_recipe


def edit_recipe(ingredient: Ingredient) -> Ingredient:
    # have a parse through method, parse through the entire recipe tree
    # enqueue all ingredients in the recipe, then have the user select
    # which node they want to change the details of, return selected node
    ingredients: list = parse_and_enqueue(ingredient, [])
    for index, ingredient in enumerate(ingredients):
        # todo finish later
        print(index, ':', ingredient.name)
        print('Which ingredient do you want to edit (choose between 0 and',
              len(ingredients), ')')
    return ingredients[promptint(False)-1]


def preview_recipe():
    pass


def populate(current: Ingredient, preview: Ingredient) -> Ingredient:
    # preview is an mock recipe tree that can be rendered,update concurrently with I/O
    new_ingredients: Queue = Queue()
    # todo add ingredient blacklist later
    ingredient_blacklist: list = [head(current).name]
    if current.parent is not None:
        ingredient_blacklist.append(current.parent.name)
    # prompt user for additional ingredients in the recipe
    trail(current)
    print('What do you need to create', current.name, end=':\n')
    while True:
        ingredient_str: str = input().strip()
        if len(ingredient_str) == 0:
            break
        elif ingredient_str == '--r':
            # randomly generate a random amount of ingredient names
            random_generated_names: list = []
            for _ in range(randint(0, 10)):
                generated_str: str = RAND_STR_GEN(randint(4, 20))
                ingredient_blacklist.append(generated_str)
                new_ingredients.enqueue(generated_str)
                preview.children.append(Ingredient(generated_str,preview))
                print('ADDED STRING:', end=generated_str+'\n')
            continue
        elif ingredient_str in ingredient_blacklist:
            print('YOU CANNOT REPEAT INPUTS')
        elif ingredient_str in valid_commands_list:
            command_prompt(ingredient_str, current,preview)
            continue
        else:
            new_ingredients.enqueue(ingredient_str)
            ingredient_blacklist.append(ingredient_str)
            Ingredient(ingredient_str,preview)
    # create add ingredients to the recipe
    while not new_ingredients.is_empty():
        current.children.append(Ingredient(new_ingredients.dequeue(), current))
    # link ingredients to the recipe recursively
    for index,child in enumerate(current.children):
        populate(child,preview.children[index])
    return head(current)


def superpopulate() -> Ingredient:
    print('What is the name of the item you want to create:', end='\n')
    while True:
        recipe_title: str = input().strip()
        if len(recipe_title) > 0:
            break
    # todo add functionality for numeric input
    preview_tree : Ingredient = Ingredient(recipe_title,None)
    return populate(Ingredient(recipe_title, None),preview_tree)


if __name__ == '__main__':
    # check for settings file
    print('Hello World from the devel 3.0!')
    recipe_tree: Ingredient = superpopulate()
    # close program in 10 seconds
    print('the program will close in 10 seconds')
    del recipe_tree
    NANI: int = 10
    while NANI > 0:
        sleep(1)
        NANI -= 1
    print('terminating program')
