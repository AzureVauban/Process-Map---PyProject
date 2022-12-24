"""
final version of the Process Map (Python)
"""


def fib(nth_term: int) -> int:
    """
    outputs the nth term of the fibonacci sequence
    n        : 01|02|03|04|05|06|07|08|09|10
    nth term : 01|01|02|03|05|08|13|21|34|55
    """
    if nth_term <= 1:
        return 1
    return fib(nth_term-1)+fib(nth_term-2)


class Deque:
    """double ended queue"""
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

    def enqueue_front(self, data):
        """add data to the front of the container instance"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = self.Node(None, data, None)
        elif self.is_full():
            raise ValueError("The container is full")
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

    def dequeue_front(self) -> None:
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

    def peak_front(self) -> None:
        """see what is at the front of the container instance without popping the element"""
        if not self.is_empty():
            return self.head.data
        raise ValueError('the container is empty, there are no values to peak')

    def enqueue_back(self, data):
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

    def dequeue_back(self) -> None:
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

    def peak_back(self) -> None:
        """see what is at the front of the container instance without popping the element"""
        if not self.is_empty():
            return self.__get_end().data
        raise ValueError('the container is empty, there are no values to peak')


class Base:
    """base class"""
    ingredient_name: str
    amount_on_hand: int = 0
    amount_made_per_craft: int = 0
    amount_needed_per_craft: int = 0
    amount_resulted: int = 0
    buffer_amount_resulted: dict = {}

    def __init__(self, ingredient_name: str = '',
                 amount_on_hand: int = 0,
                 amount_made_per_craft: int = 0,
                 amount_needed_per_craft: int = 0) -> None:
        self.ingredient_name = ingredient_name
        self.amount_on_hand = amount_on_hand
        self.amount_made_per_craft = amount_made_per_craft
        self.amount_needed_per_craft = amount_needed_per_craft
        self.amount_resulted = 0
        self.buffer_amount_resulted = {}


class Ingredient(Base):
    """ingredient class"""
    parent = None
    children: list = []

    def __init__(self, ingredient_name: str = '',
                 parent=None,
                 amount_on_hand: int = 0,
                 amount_made_per_craft: int = 0,
                 amount_needed_per_craft: int = 0) -> None:
        super().__init__(ingredient_name, amount_on_hand,
                         amount_made_per_craft, amount_needed_per_craft)
        if parent is not None and not isinstance(parent, Ingredient):
            raise TypeError('parent must be an instance', Ingredient)
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.children.append(self)


def head(ingredient: Ingredient) -> Ingredient:
    """traverse upward"""
    while ingredient.parent is not None:
        ingredient = ingredient.parent
    return ingredient


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


def populate(ingredient: Ingredient) -> Ingredient:
    """create an ingredient tree and return the head node ingredient"""
    print('What ingredients do you need to create',
          ingredient.ingredient_name, end=':\n')
    user_inputs: Deque = Deque()
    blacklist_ingredient: list = [ingredient.ingredient_name,
                                  head(ingredient).ingredient_name]
    # output the ingredient trail
    if ingredient.parent is not None:
        trail(ingredient)
    # prompt input ingredients
    while True:
        ingredient_input: str = input('')
        if ingredient_input in blacklist_ingredient:
            print('you cannot type input')
        elif len(ingredient_input) == 0:
            break
        else:
            user_inputs.enqueue_front(ingredient_input)
            blacklist_ingredient.append(ingredient_input)
    # create subnodes
    while not user_inputs.is_empty():
        subpopulate(ingredient, user_inputs.dequeue_front())
    # populate subnodes
    for subnode in ingredient.children:
        populate(subnode)
    return head(ingredient)



def subpopulate(parent: Ingredient, ingredient_name: str) -> Ingredient:
    """add docstring"""
    # todo add search method
    print('search results:',len(search_results),search_results)
    return Ingredient(ingredient_name, parent)


def recursive_count_ingredients(purple: Ingredient) -> int:
    """add docstring"""
    nodescounted = 1
    for subnode in purple.children:
        nodescounted += recursive_count_ingredients(subnode)
    return nodescounted


def count_ingredients(head_ingredient: Ingredient) -> int:
    """add docstring"""
    node_count: int = recursive_count_ingredients(head_ingredient)
    return node_count


if __name__ == '__main__':
    test = populate(Ingredient('DESIRED TEST ITEM', None, 0, 1, 1))
    print('current population:', count_ingredients(test))
    print('terminating process')
