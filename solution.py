"""
Reworked Main Process Map with needed changes
Reworked csv parsing and writing
- parsing works at any level from any node
- ability to organize recipes into groups with their own unique string key
Caculation with floats
- commands
- - view (render the recipe tree into the console)
- - rename (any ingredient in the recipe)
- - edit (have the user select which node they want to edit)

# FORMAT TO PEP8 STANDARDS
"""


class Queue:
    # TODO ADD/IMPORT
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
    pass


class Ingredient(Base):
    # TODO ADD/IMPORT
    pass


class Recipe:
    # TODO ADD/IMPORT
    tentative: Ingredient = None


def head(current: Ingredient = None) -> Ingredient:
    # TODO ADD/IMPORT
    return current
