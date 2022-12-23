"""
final version of the Process Map (Python)
"""

import random


def fib(nth_term: int) -> int:
    """
    outputs the nth term of the fibonacci sequence
    n        : 01|02|03|04|05|06|07|08|09|10
    nth term : 01|01|02|03|05|08|13|21|34|55
    """
    if nth_term <= 1:
        return 1
    return fib(nth_term-1)+fib(nth_term-2)


def randomly_generate_string(size: int = random.randint(5, 10)) -> str:
    """select random characters and return the string"""
    choice: str = 'ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuvwxyz1234567890-'
    return_str: str = ''
    for _ in range(size):
        return_str += random.choice(choice)
    return return_str

import random

def chat_randomly_generate_string(size: int = None, seed: int = None, 
                             include_lowercase: bool = True, include_uppercase: bool = True, 
                             include_numbers: bool = True, include_special: bool = False) -> str:
    """Generate a random string with the specified character options and length."""
    # Set default size if not provided
    if size is None:
        size = random.randint(5, 10)
        
    # Validate size argument
    if not isinstance(size, int) or size < 1:
        raise ValueError("Size must be a positive integer")
    
    # Set default seed if not provided
    if seed is not None:
        random.seed(seed)
    
    # Build list of valid characters
    choices = []
    if include_lowercase:
        choices += 'abcdefghijklmnopqrstuvwxyz'
    if include_uppercase:
        choices += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if include_numbers:
        choices += '1234567890'
    if include_special:
        choices += '!@#$%^&*()_+-=[]{}|:;<>,.?/~`'
    
    # Generate random string
    return_str = ''
    for _ in range(size):
        return_str += random.choice(choices)
    return return_str

class Dequeue:
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

        def set_index(self, index):
            """set the index of the node instance"""
            self.index = index

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

    def enqueue_front(self, data):
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

    def dequeue_front(self) -> None:
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


if __name__ == '__main__':
    test = Dequeue()
    for _ in range(10):
        test.enqueue_front(chat_randomly_generate_string(
            random.randint(7, 17),
            include_special=True,
            include_lowercase=False,
            include_uppercase=True))
    while not test.is_empty():
        print(test.dequeue_front())
    print('terminating process')
