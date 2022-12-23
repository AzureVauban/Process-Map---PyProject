"""
final version of the Process Map (Python)
"""


class Queue:
    class Node:
        after = None
        before = None
        data = None
    head: Node = None
    size: int = 0


if __name__ == '__main__':
    print('terminating process')
