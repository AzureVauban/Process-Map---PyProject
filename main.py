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
    """dynamic queue class"""
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
    """
    class for storing simple data about an item such as its name and how much
    is needed to create its parent
    """
    ingredient: str = ''
    aliasingredient: str = ''
    #! if the ingredient name has been repeated somewhere else in the
    #! tree, make the aliasingredient a unique name and output into the csv file
    amountonhand: int = 0
    amountneeded: int = 0
    amountofparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '',
                 amountonhand: int = -1,
                 amountofparentmadepercraft: int = -1,
                 amountneeded: int = -1) -> None:  # noqa: E501 pylint: disable=line-too-long
        """
        Args:
            name (str, optional): name of the item. Defaults to ''.
            red (int, optional): amount of the item you have on hand. Defaults to 0.
            blue (int, optional): amount of the parent item you create each time you craft it.
            Defaults to 1.
            yellow (int, optional): amount of item needed to craft the parent item one time.
            Defaults to 1.
        """
        self.amountonhand = amountonhand
        self.amountofparentmadepercraft = amountofparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.aliasingredient = self.ingredient
        self.amountresulted = 0

class BaseNode(Base):
    """
    stores identifiable features of an item, such as the parent and children instances
    Args:
        NobeB (class): parent class of item
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    askmadepercraftquestion: bool = False
    # this is unique identifer for an ingredient tree when its outputted into a csv file
    treekey: str = ''
    ismain_promptinputbool: bool = True

    def __init__(self, ingredient: str = '', parent=None, amountonhand: int = 0, amountofparentmadepercraft: int = 1, amountneeded: int = 1, green: bool = False, orange: bool = __name__ == '__main__', treekey: str = 'NanKey') -> None:  # pylint:disable=C0301
        """
        default constructor for Node instance, stores identifying features of an item's
        information
        Args:
            name (str, optional): name of the item. Defaults to ''.
            pare (class, optional): parent instance of declared Node. Defaults to None
            red (int, optional): amount of the item you have on hand. Defaults to 0.
            blue (int, optional): amount of the parent item you create each time you craft it.
            Defaults to 1.
            yellow (int, optional): amount of item needed to craft the parent item one time.
            Defaults to 1.
            green (bool,optional): boolean variable, checks if one of the Node's sibiling instances was prompted to input the amount made per craft (blue)
        """
        super().__init__(ingredient, amountonhand, amountofparentmadepercraft, amountneeded)
        self.instancekey = BaseNode.instances
        self.children = {}
        self.ismain_promptinputbool = orange
        self.parent = parent
        if self.parent is not None and isinstance(self.parent, BaseNode):
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
            self.treekey = self.parent.treekey
            self.ismain_promptinputbool = self.parent.ismain_promptinputbool
            self.treekey = self.parent.treekey
        else:
            self.generation = 0
            self.treekey = self.generate_treekey()  # generate a unique tree key
        if not __name__ == '__main__' and parent is None:
            self.treekey = treekey
        # set tree key of this instance

        if not self.checkaliasuniqueness(self.aliasingredient):
            self.aliasingredient = self.aliasingredient + '__' + generatename()
        self.askmadepercraftquestion = green
        BaseNode.instances += 1
        if self.ismain_promptinputbool:
            self.__inputnumerics()

    def __inputnumerics(self):
        """
        prompt input of the numeric data for the instance from the user
        """
        # prompt amount on hand
        while True and PROGRAMMODETYPE == 0:
            print('How much', self.ingredient, 'do you have on hand: ')
            self.amountonhand = promptint()
            if self.amountonhand < 0:
                print('That number is not valid')
            else:
                break
            # prompt amount needed
        if self.parent is not None:
            # prompt amount made per craft
            while True and self.askmadepercraftquestion:
                print('How much', self.parent.ingredient,
                      'do you create each time you craft it: ')
                self.amountofparentmadepercraft = promptint()
                if self.amountofparentmadepercraft < 1:
                    print('That number is not valid')
                else:
                    self.askmadepercraftquestion = False
                    break
            while True:
                print('How much', self.ingredient, 'do you need to craft',
                      self.parent.ingredient, '1 time: ')
                self.amountneeded = promptint()
                if self.amountneeded < 1:
                    print('That number is not valid')
                else:
                    break


def populate()


if __name__ == '__main__':
    print('hello world')
    print('terminating process')
