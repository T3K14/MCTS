def fun(node):
    return node.n

class Node:
    def __init__(self, n):
        self.n = n

l = [Node(1), Node(2), Node(3)]
print(l)

print(max(*l, key=lambda node: node.n))