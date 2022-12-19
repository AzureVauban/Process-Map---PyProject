"""
final version of the python process map
- use python 3.11
"""

from enum import Enum
from math import floor, ceil
from sys import maxsize


class ProgramState(Enum):
    """Enum for which mode the user selected during runtime"""
    MODE_A = 0  # recursive arithmetic (amountresulted)
    MODE_B = 1  # inverse recursive arithmetic (amountonhand)


program_mode_enum: ProgramState = ProgramState.MODE_A


def fib(nth_term: int) -> int:  # ! remove this later
    """output the nth term of the fibonacci sequence"""
    if nth_term <= 1:
        return 1
    return fib(nth_term-1) + fib(nth_term-2)


def promptint() -> int:
    """
    prompts the user for an postive integer and returns it
    Returns:
        int: postive integer from user input
    """
    while True:
        myinput = input('').strip()
        if not myinput.isdigit():
            print('you can only type in a positive integer')
        elif int(myinput) < 0:
            print('please type in a postive integer')
        else:
            return int(myinput)


class Pillar:
    """
    dynamically-size data structure, allows insert/remove operations
    from both ends (no middle access)
    - when empty, is typeless
    - allows for 'First-In,First-Out' & 'Last-In,First-Out' usage
    """
    class Node:
        """Node class for pillar data structure"""
        index: int
        data = None
        after = None
        before = None

        def __init__(self, before, data, after) -> None:
            self.before = before
            self.data = data
            self.after = after
            self.index = 0

        def set_index(self, index):
            """set the index of the node instance"""
            self.index = index

        def help(self):
            """print debug data for the Node instance"""
            print('index: '+str(self.index))
            print('data: '+str(self.data))
            print('after: '+str(self.after))
            print('before: '+str(self.before))

    head: Node = None
    size: int = 0

    def __init__(self) -> None:
        self.head = None
        self.size = 0

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
                current.set_index(new_index)
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

    def peak_front(self) -> None:
        """see what is at the front of the container instance without popping the element"""
        if not self.is_empty():
            return self.head.data
        raise ValueError('the container is empty, there are no values to peak')

    def insert_front(self, data):  # ! should be called push front/prepend
        """add data to the front of the container instance"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = self.Node(None, data, None)
        else:
            # prepend a new node to the front of the container instance
            old_head: self.Node = self.head
            self.__check_data_typing(old_head, data)
            new_head: self.Node = self.Node(None, data, old_head)
            old_head.before = new_head
            self.head = new_head
        # set the new indicies
        self.__set_index()
        # change the size of the container instance
        self.size += 1

    def remove_front(self) -> None:  # ! should be called pop front/remove front
        """remove data from the back of the container instance"""
        if self.is_empty():
            raise ValueError('cannot pop any values from an empty container')
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

    def peak_back(self) -> None:
        """see what is at the front of the container instance without popping the element"""
        if not self.is_empty():
            return self.__get_end().data
        raise ValueError('the container is empty, there are no values to peak')

    def insert_back(self, data):  # ! should be called push back/append
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

    def remove_back(self) -> None:  # ! should be called pop back/remove back
        """remove data from the front of the container instance"""
        if self.is_empty():
            raise ValueError('cannot pop any values from an empty container')
        return_value = self.head.data
        if self.size == 1:
            self.head = None
        else:
            old_endpoint: self.Node = self.__get_end()
            return_value = old_endpoint.data
            new_endpoint: self.Node = None
            if old_endpoint.before is not None:
                # ? destroy the link the the endpoint and the node before it (if its not NULL)
                new_endpoint = old_endpoint.before
                new_endpoint.after = None
                old_endpoint.before = None
                old_endpoint = None
                del old_endpoint
        self.size -= 1
        return return_value


class Base:
    """add docstring"""
    ingredient_name: str = ''
    amount_on_hand: int = 0  # ! original name : amount_on_hand
    amount_made_per_craft: int = 0  # ! original name : amount_made_per_craft
    amount_needed_per_craft: int = 0  # ! original name : amount_needed_per_craft
    amount_resulted: int = 0  # ! original name : amount_resulted
    buffer_amount_resulted: dict = {}  # ! original name : buffer_amount_resulted
    # todo make a method that make this unique for all duplicates in the tree
    ingredient_name_alias: str = ''

    def __init__(self, ingredient_name: str = '',
                 amount_on_hand: int = 0,
                 amount_made_per_craft: int = 0,
                 amount_needed_per_craft: int = 0) -> None:
        self.ingredient_name = ingredient_name
        self.amount_on_hand = amount_on_hand
        self.amount_made_per_craft = amount_made_per_craft
        self.amount_needed_per_craft = amount_needed_per_craft
        self.ingredient_name_alias = self.ingredient_name
        self.amount_resulted = 0

    def clear_buffer(self):
        """clear the amount resulted buffer"""
        self.buffer_amount_resulted.clear()

    def prompt_amount_on_hand(self):
        """add docstring"""
        self.amount_on_hand = promptint()

    def prompt_amount_made_per_craft(self):
        """add docstring"""
        self.amount_made_per_craft = promptint()

    def prompt_amount_needed_per_craft(self):
        """add docstring"""
        self.amount_needed_per_craft = promptint()


class Ingredient(Base):
    """add docstring"""
    parent = None
    children: list = []
    instances: int = 0
    generation: int = 0
    prompt_amount_made_per_craft_bool: bool = False
    prompt_amounts_to_user: bool = False

    def __init__(self, ingredient_name: str = '',
                 parent=None,
                 amount_on_hand: int = 0,
                 amount_made_per_craft: int = 1,
                 amount_needed_per_craft: int = 1,
                 prompt_amount_made_per_craft_bool: bool = False) -> None:
        super().__init__(ingredient_name,
                         amount_on_hand,
                         amount_made_per_craft,
                         amount_needed_per_craft)
        self.parent = parent
        self.children = []
        self.prompt_amounts_to_user = False
        if self.parent is not None and not isinstance(self.parent, Ingredient):
            raise TypeError('must be an instance of', Ingredient, 'or None')
        self.generation = 0
        self.prompt_amount_made_per_craft_bool = prompt_amount_made_per_craft_bool
        if self.parent is not None:
            self.parent.children.append(self)
            self.generation = self.parent.generation+1
            self.prompt_amounts_to_user = self.parent.prompt_amounts_to_user
            self.prompt_amount_made_per_craft_bool = self.parent.prompt_amount_made_per_craft_bool
        # prompt user amounts
        if self.parent is not None and self.prompt_amounts_to_user:
            self.__prompt_amounts()
        Ingredient.instances += 1

    def recursivearithmetic(self) -> int:  # ! upward recursion
        """
        tentative docstring description
        """
        # check and set minimum resulted if queue is not empty
        tentative_integer: int = maxsize  # ? sys.maxsize
        if len(self.buffer_amount_resulted) == 0:
            tentative_integer = 0
        else:
            for myinteger in self.buffer_amount_resulted.items():
                if myinteger[1] < tentative_integer:
                    tentative_integer = myinteger[1]
        red = (self.amount_made_per_craft / self.amount_needed_per_craft)
        blue = (red*self.amount_on_hand) + (red*tentative_integer)
        blue = round(floor(blue))  # ? math.floor()
        self.amount_resulted = blue
        # recursively call the method
        if self.parent is not None:
            self.parent.buffer_amount_resulted.update(
                {self.ingredient_name: self.amount_resulted})
            self.parent.recursivearithmetic()
        return self.amount_resulted

    def reversearithmetic(self, desiredamount: int = 0) -> int:  # ! downward recursion
        """
        tentative docstring description
        """
        self.amount_resulted = desiredamount
        red: float = ((self.amount_made_per_craft/self.amount_needed_per_craft)
                      ** -1)*self.amount_resulted
        green: float = round(ceil(red))  # ? math.ceil()
        self.amount_on_hand = int(max(red, green))
        traceback: bool = green > red
        if traceback:  # traverse upward and increase the amount on hand by 1
            temp: Ingredient = self
            while temp.parent is not None:
                temp = temp.parent
                temp.amount_on_hand += 1
        # continue method recursively
        if len(self.children) > 0:
            for child in self.children:
                if not isinstance(child, Ingredient):
                    raise TypeError('object is not an instance of', Ingredient)
                child.reversearithmetic(self.amount_on_hand)
        return self.amount_on_hand

    def __prompt_amounts(self):
        """
        - only in mode A: prompt amount_on_hand
        - if not head node(regardless of enum state):
            - prompt amount_made_per_craft
            - prompt amount_needed_per_craft (only for eldest sibiling node)
        """
        if not isinstance(self.parent, Ingredient) and self.parent is not None:
            raise TypeError('parent object is not an instance of', Ingredient)
        if program_mode_enum == ProgramState.MODE_A:
            print('How much', self.ingredient_name, 'do you have on hand?')
            self.prompt_amount_on_hand()
        if self.parent is not None and self.prompt_amount_made_per_craft_bool:
            print('How much', self.parent.ingredient_name,
                  'do you make each time you craft it?')
            self.prompt_amount_made_per_craft()
        if self.parent is not None:
            print('How much', self.ingredient_name,
                  'do you need to craft', self.parent.ingredient_name, 'once?')
            self.prompt_amount_needed_per_craft()


def find_ingredients_with_same_name(ingredient_name: str,
                                    ingredient_node: Ingredient,
                                    pillar_of_ingredients2: Pillar = Pillar()) -> Pillar:
    """find other ingredient nodes with the same ingredient name"""
    if ingredient_node.ingredient_name == ingredient_name:
        pillar_of_ingredients2.insert_back(ingredient_node)
    for subingredient in ingredient_node.children:
        find_ingredients_with_same_name(ingredient_name,
                                        subingredient,
                                        pillar_of_ingredients2)
    return pillar_of_ingredients2


def make_all_names_unique(sub_node: Ingredient):  # todo test method out
    """makes all subnode ingredient alias unique"""
    if sub_node.parent is not None:
        nodes_with_same_name: Pillar = find_ingredients_with_same_name(sub_node.ingredient_name,
                                                                       head(
                                                                           sub_node),
                                                                       Pillar())
        if len(nodes_with_same_name) > 1:
            nodes_with_same_name.remove_front()
            variant_num: int = 1
            for _ in range(nodes_with_same_name.size):
                ingredient_node: Ingredient = nodes_with_same_name.remove_back()
                ingredient_node.ingredient_name_alias += variant_num
                variant_num += 1
    for sub_node in sub_node.children:
        make_all_names_unique(sub_node)


def subpopulate(parent_node: Ingredient,
                ingredient_name: str,
                amount_made_per_craft: int,
                prompt_amount_made_per_craft: bool) -> Ingredient:
    """
    creates a new sub-node, prompt user if they want to clone it if
    ingredient name as already been typed
    """
    return Ingredient(ingredient_name,
                      parent_node,
                      amount_made_per_craft=amount_made_per_craft,
                      prompt_amount_made_per_craft_bool=prompt_amount_made_per_craft)


def trail(current: Ingredient):
    """
    print the ingredient trail leading up to the parent most Node
    Args:
        node (Node): starting Node
    """
    print('TRAIL: ', end='')
    while True:
        if current.parent is not None:
            print(current.ingredient_name, '-> ', end='')
            current = current.parent
        else:
            print(current.ingredient_name)
            break


def head(node: Ingredient) -> Ingredient:
    """add docstring"""
    while node.parent is not None:
        node = node.parent
    return node


def populate(parent_node: Ingredient) -> Ingredient:
    """
    creates an ingredient tree by prompting the user to type in the name of the sub-ingredients
    """
    # prompt user inputs & output current ingredient trail
    print('what do you need to create', parent_node.ingredient_name, end=':\n')
    user_inputs: Pillar = Pillar()
    ingredient_blacklist: list = [parent_node.ingredient_name,
                                  head(parent_node).ingredient_name]
    for sub_node in parent_node.children:
        ingredient_blacklist.append(sub_node.ingredient_name)
    # output ingredient trail
    if parent_node.parent is not None:
        trail(parent_node)
    while True:
        ingredient_name: str = input('')
        if ingredient_name in ingredient_blacklist:
            print('you cannot repeat your input')
        elif len(ingredient_name) == 0:
            break
        else:
            user_inputs.insert_front(ingredient_name)
            ingredient_blacklist.append(ingredient_name)
    # create subnodes
    # todo implement eldest sibling amount_made_per_craft auto-input
    eldest_sibling: Ingredient = None
    for _ in range(user_inputs.size):
        if eldest_sibling is None:
            eldest_sibling = subpopulate(
                parent_node,
                user_inputs.remove_front(),
                1, True)
        else:
            subpopulate(parent_node,
                        user_inputs.remove_front(),
                        eldest_sibling.amount_made_per_craft,
                        False)
    del user_inputs
    # recursively populate the ingredient tree
    for sub_node in parent_node.children:
        populate(sub_node)
    # if on mode A, call recursive upward math method
    if program_mode_enum == ProgramState.MODE_A and len(parent_node.children) == 0:
        parent_node.recursivearithmetic()
    return head(parent_node)


def population_count(head_node: Ingredient) -> int:  # ! rework later
    """
    creates a pillar instance of all ingredient names from each node then returns the size of that
    container instance which is equal to the population of the ingredient tree
    """
    node_count: int = 0
    if head_node is not None:
        node_pillar: Pillar = find_all(head_node, Pillar())
        node_count = node_pillar.size
        while not node_pillar.is_empty():
            node_pillar.remove_back()
    return node_count


def find_all(head_node: Ingredient, container_nodes: Pillar) -> Pillar:  # ! remove later
    """debug function - see how many ingredients are in the container instance"""
    container_nodes.insert_back(head_node)
    for sub_node in head_node.children:
        find_all(sub_node, container_nodes)
    return container_nodes


def superpopulate() -> Ingredient:
    """main process for creating ingredient tree"""
    # prompt the user for the name of the item they want to create
    while True:
        itemname: str = input(
            'What is the name of the item you want to create: ')
        if len(itemname) != 0:
            break
        print('your input cannot be empty')
    # create ingredient tree
    tree: Ingredient = Ingredient(itemname)
    tree.prompt_amounts_to_user = False
    tree = populate(tree)
    return tree


def pillar_test():  # ! remove later
    """a function for testing the operations of the pillar data structure"""
    nani: Pillar = Pillar()
    nth_term_i: int = 0
    for __ in range(0, 10):
        nth_term_i += fib(__+2)
        if __ % 2 == 0:
            nani.insert_back(nth_term_i)
            nth_term_i *= -3
        else:
            nani.insert_front(nth_term_i)
    del nth_term_i  # ? remove variable from debug view pass this line
    for __ in range(nani.size):
        print(nani.remove_back())


def find_endpoints(ingredient_object: Ingredient, pillar_of_nodes: Pillar = Pillar()) -> Pillar:
    """find all endpoint instances in the ingredient tree"""
    for sub_node in ingredient_object.children:
        find_endpoints(sub_node, pillar_of_nodes)
    if len(ingredient_object.children) == 0:
        pillar_of_nodes.insert_back(ingredient_object)
    return pillar_of_nodes  # ! use return value as a stack


if __name__ == '__main__':
    # create ingredient tree
    ingredient_tree: Ingredient = superpopulate()
    population_count_str: str = str(population_count(ingredient_tree))
    print('current population: ', end=population_count_str+'\n\n')
    # output data
    pillar_of_ingredients: Pillar = find_all(ingredient_tree, Pillar())
    ingredient_tree.reversearithmetic(100)
    pillar_of_endpoints: Pillar = Pillar()
    pillar_of_endpoints: Pillar = find_endpoints(ingredient_tree, pillar_of_endpoints)
    for _ in range(pillar_of_endpoints.size):
        print(pillar_of_endpoints.peak_front().ingredient_name, str(pillar_of_endpoints.peak_front().amount_on_hand)+'x')
        pillar_of_endpoints.remove_front()
    make_all_names_unique(ingredient_tree)
    foo:Pillar = find_all(ingredient_tree,Pillar())
    
    print('terminating process')
