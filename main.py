"""
final version of the python process map
- use python 3.11
"""


class Node:
    """Node class for Queue"""
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


class Queue:
    """dynamic queue class
    #! remove below docstring comment lines later
    - implement in csv -> node creation method
    - implement in populate()
    """
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
# end def


if __name__ == '__main__':
    itemname: str = input('What is the name of the item you want to create')
#!    ingredient_tree: Node = populate(Node(itemname))
    print('terminating process')
