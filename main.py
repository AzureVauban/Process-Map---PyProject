"""
final version of the Process Map (Python)
"""


def fib(n: int) -> int:
    if n <= 1:
        return 1
    return fib(n-1)+fib(n-2)


if __name__ == '__main__':
    for _ in range(10):
        print(fib(_))
    print('terminating process')
