"""
final version of the python process map
- use python 3.11
"""


class QueueNode:
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
    head: QueueNode = None
    size: int = 0

    # functions
    def __get_end(self) -> QueueNode:
        """get the endpoint node of the data structure"""
        current: QueueNode = self.head
        while current.after is not None:
            current = current.after
        return current

    def __set_index(self):
        """set the index of all the nodes"""
        if not self.is_empty():
            current: QueueNode = self.head
            new_index: int = 0
            while current.after is not None:
                current.set_index(new_index)
                current = current.after

    @classmethod
    def __check_data_typing(cls, old_node: QueueNode, new_data):
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
            self.head = QueueNode(None, data, None)
        else:
            # append a new node to the end of the queue
            old_endpoint: QueueNode = self.__get_end()
            self.__check_data_typing(old_endpoint, data)
            # link Node pointers of old and new endpoint
            new_endpoint: QueueNode = QueueNode(old_endpoint, data, None)
            old_endpoint.after = new_endpoint
        # set the new indicies
        self.__set_index()
        # change the size of the queue
        self.size += 1

    def dequeue(self) -> None:
        """dequeue data from the queue instance"""
        if not self.is_empty():
            old_head_node: QueueNode = self.head
            return_data = old_head_node.data
            new_head_node: QueueNode = None
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


class Base:
    """add docstring"""
    ingredient: str = ''
    amount_on_hand: int = 0
    amount_made_per_craft: int = 0
    amount_needed_per_craft: int = 0
    amount_resulted: int = 0

    def __init__(self, ingredient: str = '',
                 amount_on_hand: int = 0,
                 amount_made_per_craft: int = 0,
                 amount_needed_per_craft: int = 0) -> None:
        self.ingredient = ingredient
        self.amount_on_hand = amount_on_hand
        self.amount_made_per_craft = amount_made_per_craft
        self.amount_needed_per_craft = amount_needed_per_craft
        self.amount_resulted = 0


class NodeBase(Base):
    """add docstring"""
    parent = None
    children: list = []
    instances: int = 0
    generation: int = 0

    def __init__(self, ingredient: str = '',
                 parent=None,
                 amount_on_hand: int = 0,
                 amount_made_per_craft: int = 0,
                 amount_needed_per_craft: int = 0) -> None:
        super().__init__(ingredient, amount_on_hand,
                         amount_made_per_craft,
                         amount_needed_per_craft)
        self.parent = parent
        if self.parent is not None and not isinstance(self.parent, NodeBase):
            raise TypeError('must be an instance of',NodeBase,'or None')
        self.generation = 0
        if self.parent is not None:
            self.parent.children.append(self)
            self.generation = self.parent.generation+1
        NodeBase.instances += 1

def head(node : NodeBase)-> NodeBase:
    """add docstring"""
    while node.parent is not None:
        node = node.parent
    return node
def subpopulate(parent_node: NodeBase, ingredient: str) -> NodeBase:
    """add docstring"""
    return NodeBase(ingredient, parent_node)


def populate(parent_node: NodeBase) -> NodeBase: #todo finish this functon
    """add docstring"""
    # prompt userinput
    print('what do you need to create',parent_node.ingredient,end=':\n')
    user_inputs : Queue = Queue()
    while True:
        ingredient_name : str = input('')
        if len(ingredient_name) == 0:
            break
        user_inputs.enqueue(ingredient_name)
    # create subnodes 
    for _ in range(user_inputs.size):
        subpopulate(parent_node,user_inputs.dequeue())
    # recursively populate the ingredient tree
    for sub_node in parent_node.children:
        populate(sub_node)
    return parent_node

if __name__ == '__main__':
    itemname: str = input('What is the name of the item you want to create: ')
    ingredient_tree: NodeBase = populate(NodeBase(itemname))
    print('terminating process')
