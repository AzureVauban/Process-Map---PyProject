"""
final version of the python process map
- use python 3.11
"""

from enum import Enum


class ProgramState(Enum):
    """Enum for which mode the user selected during runtime"""
    MODE_A = 0  # recursive arithmetic (amountresulted)
    MODE_B = 1  # inverse recursive arithmetic (amountonhand)


program_mode_enum: ProgramState = ProgramState.MODE_A


class Node:
    """Node class for Queue and Stack"""
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
# end def


def fib(nth_term: int) -> int:  # ! remove this later
    """output the nth term of the fibonacci sequence"""
    if nth_term <= 1:
        return 1
    return fib(nth_term-1) + fib(nth_term-2)


class Queue:
    """dynamic queue class ("First-In, First-Out")"""
    head: Node = None
    size: int = 0

    # functions
    def __get_end(self) -> Node:
        """get the endpoint node of the data structure"""
        current: Node = self.head
        while current.after is not None:
            current = current.after
        return current

    def __set_index(self):
        """set the index of all the nodes"""
        if not self.is_empty():
            current: Node = self.head
            new_index: int = 0
            while current.after is not None:
                current.set_index(new_index)
                current = current.after
                new_index += 1

    @classmethod
    def __check_data_typing(cls, old_node: Node, new_data):
        """make sure that the data enqueued is the same type"""
        if not isinstance(old_node.data, type(new_data)):
            raise TypeError('data is not an instance of', type(old_node.data))

    def is_empty(self) -> bool:
        """checks if there is any data in the queue"""
        return self.head is None

    def peak(self) -> None:
        """see who is at the front of the queue without dequeueing the element"""
        if not self.is_empty():
            return self.head.data
        return None

    def enqueue(self, data):
        """enqueue data into the queue instance"""
        if self.is_empty():
            self.head = Node(None, data, None)
        else:
            # append a new node to the end of the queue
            old_endpoint: Node = self.__get_end()
            self.__check_data_typing(old_endpoint, data)
            # link Node pointers of old and new endpoint
            new_endpoint: Node = Node(old_endpoint, data, None)
            old_endpoint.after = new_endpoint
        # set the new indicies
        self.__set_index()
        # change the size of the queue
        self.size += 1

    def dequeue(self) -> None:
        """dequeue data from the queue instance"""
        if not self.is_empty():
            old_head_node: Node = self.head
            return_data = old_head_node.data
            new_head_node: Node = None
            if old_head_node.after is not None:
                new_head_node = old_head_node.after
                new_head_node.before = None
            self.head = new_head_node
            del old_head_node
            self.size -= 1
            # set the new indicies
            self.__set_index()
            return return_data
        return None

    def __init__(self) -> None:
        self.head = None
        self.size = 0

    def __help__printborder(self):
        """helper method for public help()"""
        border: str = ''
        for _ in range(15+len(str(self))):
            border += '_'
        print(border)

    def help(self, output_node_help: bool = False):
        """print debug data for the Queue instance"""
        queue_data_type: str = 'None'
        if not self.is_empty():
            queue_data_type = str(type(self.head.data))
        print('stored data type: '+queue_data_type)
        print('size: '+str(self.size))
        print('stored at: '+str(self))
        self.__help__printborder()
        if output_node_help and not self.is_empty():
            current: Node = self.head
            while current.after is not None:
                current.help()
                current = current.after
                self.__help__printborder()
# end def


class Stack:
    """
    dynamic stack class ("Last-In, First-Out")
    - implement in csv -> node creation method
    - implement in node -> csv writing method
    """
    head: Node = None
    size: int

    def is_empty(self) -> bool:
        """checks if there is any data in the queue"""
        return self.head is None

    def __get_end(self) -> Node:
        """get the endpoint node of the data structure"""
        current: Node = self.head
        while current.after is not None:
            current = current.after
        return current

    def __set_index(self):
        """set the index of all the nodes"""
        if not self.is_empty():
            current: Node = self.head
            new_index: int = 0
            while current.after is not None:
                current.set_index(new_index)
                current = current.after
                new_index += 1

    def push(self, data):
        """adds a node onto the top of the stack"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = Node(None, data, None)
        else:
            # ? get the endpoint node and append a new node after that
            old_endpoint: Node = self.__get_end()
            new_endpoint: Node = Node(old_endpoint, data, None)
            old_endpoint.after = new_endpoint
            self.__set_index()
        self.size += 1

    def peak(self) -> None:
        """get the data stored at the top of the stack without destroying the node"""
        if not self.is_empty():
            return self.__get_end().data
        return None

    def pop(self) -> None:
        """pop the node last inserted into the stack instance"""
        if not self.is_empty() and self.size != 1:
            old_endpoint: Node = self.__get_end()
            return_value = old_endpoint.data
            new_endpoint: Node = None
            if old_endpoint.before is not None:
                # ? destroy the link the the endpoint and the node before it (if its not NULL)
                new_endpoint = old_endpoint.before
                new_endpoint.after = None
                old_endpoint.before = None
                old_endpoint = None
                del old_endpoint
            self.size -= 1
            return return_value
        if not self.is_empty() and self.size == 1:
            return_value = self.head.data
            self.head = None
            self.size -= 1
            return return_value
        return None

    def __init__(self) -> None:
        self.head = None
        self.size = 0


class DeQueue:  # todo make a DS that combines the functionality of a stack and a queue
    """
    double ended Queue,
    allows for 'FIFO' and 'LIFO'"""
    head: Node = None
    size: int = 0

    def __init__(self) -> None:
        self.head = None
        self.size = 0

    def __get_end(self) -> Node:
        """get the endpoint node of the data structure"""
        current: Node = self.head
        while current.after is not None:
            current = current.after
        return current

    def __set_index(self):
        """set the index of all the nodes"""
        if not self.is_empty():
            current: Node = self.head
            new_index: int = 0
            while current.after is not None:
                current.set_index(new_index)
                current = current.after
                new_index += 1

    @classmethod
    def __check_data_typing(cls, old_node: Node, new_data):
        """make sure that the data enqueued is the same type"""
        if not isinstance(old_node.data, type(new_data)):
            raise TypeError('data is not an instance of', type(old_node.data))

    def is_empty(self) -> bool:
        """checks if there is any data in the queue"""
        return self.head is None

    def peak(self) -> None:
        """see who is at the front of the queue without dequeueing the element"""
        if not self.is_empty():
            return self.head.data
        # ! raise an error (peaking from head when it is null)
        raise ValueError('the container is empty, there are no values to peak')

    def push_back(self, data):  # ! makes a new endpoint node
        """add data to the back of the data structure"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = Node(None, data, None)
        else:
            # append a new node to the end of the queue
            old_endpoint: Node = self.__get_end()
            self.__check_data_typing(old_endpoint, data)
            # link Node pointers of old and new endpoint
            new_endpoint: Node = Node(old_endpoint, data, None)
            old_endpoint.after = new_endpoint
        # set the new indicies
        self.__set_index()
        # change the size of the queue
        self.size += 1

    def push_front(self, data):  # ! makes a new head node
        """add data to the front of the data structure"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = Node(None, data, None)
        else:
            # prepend a new node to the front of the queue
            old_head: Node = self.head
            self.__check_data_typing(old_head, data)
            new_head: Node = Node(None, data, old_head)
            old_head.before = new_head
            self.head = new_head
        # set the new indicies
        self.__set_index()
        # change the size of the queue
        self.size += 1

    def pop_back(self) -> None:
        """remove data from the back of the data structure"""
        if self.is_empty():
            raise ValueError('cannot pop any values from an empty container')
        old_head_node: Node = self.head
        return_data = old_head_node.data
        new_head_node: Node = None
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
    """add docstring"""
    ingredient_name: str = ''
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


class Ingredient(Base):
    """add docstring"""
    parent = None
    children: list = []
    instances: int = 0
    generation: int = 0

    prompt_amounts_to_user: bool = False

    def __init__(self, ingredient_name: str = '',
                 parent=None,
                 amount_on_hand: int = 0,
                 amount_made_per_craft: int = 1,
                 amount_needed_per_craft: int = 1) -> None:
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
        if self.parent is not None:
            self.parent.children.append(self)
            self.generation = self.parent.generation+1
            self.prompt_amounts_to_user = self.parent.prompt_amounts_to_user
        # prompt user amounts
        if self.parent is not None and self.prompt_amounts_to_user:
            self.__prompt_amounts()
        Ingredient.instances += 1

    def __prompt_amounts(self):
        """
        - only in mode A: prompt amount_on_hand
        - if not head node(regardless of enum state):
            - prompt amount_made_per_craft
            - prompt amount_needed_per_craft (only for eldest sibiling node)
        """


def subpopulate(parent_node: Ingredient, ingredient_name: str) -> Ingredient:
    """
    creates a new sub-node, prompt user if they want to clone it if
    ingredient name as already been typed
    """
    return Ingredient(ingredient_name, parent_node)


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
    user_inputs: Queue = Queue()
    ingredient_blacklist: list = [parent_node.ingredient_name]
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
            user_inputs.enqueue(ingredient_name)
            ingredient_blacklist.append(ingredient_name)
    # create subnodes
    for _ in range(user_inputs.size):
        subpopulate(parent_node, user_inputs.dequeue())
    del user_inputs
    # recursively populate the ingredient tree
    for sub_node in parent_node.children:
        populate(sub_node)
    return parent_node


def population_count(head_node: Ingredient) -> int:  # ! rework later
    """
    creates a queue of all ingredient names from each node then returns the size of that
    queue which is equal to the population of the ingredient tree
    """
    node_count: int = 0
    if head_node is not None:
        node_queue: Queue = find_all(head_node, Queue())
        node_count = node_queue.size
        while not node_queue.is_empty():
            node_queue.dequeue()
    return node_count


def find_all(head_node: Ingredient, queue_nodes: Queue) -> Queue:  # ! remove later
    """debug function - see how many ingredients are in the queue"""
    queue_nodes.enqueue(head_node)
    for sub_node in head_node.children:
        find_all(sub_node, queue_nodes)
    return queue_nodes


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
    tree: Ingredient = populate(Ingredient(itemname))
    return tree


if __name__ == '__main__':
    # create ingredient tree
    #!!ingredient_tree: Ingredient = superpopulate()
    #!!population_count_str: str = str(population_count(ingredient_tree))
    #!!print('current population: ', end=population_count_str+'\n')
    # output data
    #!!queue_of_ingredients: Queue = find_all(ingredient_tree, Queue())
    #!!for _ in range(queue_of_ingredients.size):
    #!!    print(queue_of_ingredients.dequeue().ingredient_name)
    nani: DeQueue = DeQueue()
  #  print(test_dequeue.peak())
    for __ in range(0, 10):
        nth_term: int = fib(__+2)
        if __ % 2 == 0:
            nani.push_back(nth_term)
        else:
            nani.push_front(nth_term*-1)

   # print(test_dequeue.size)
    for __ in range(nani.size):
        print('popped value', nani.pop_back())
    #!print('popped value', test_dequeue.pop_back())
    print('terminating process')
