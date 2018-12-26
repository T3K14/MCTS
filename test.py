class Node:
    def __init__(self):
        self.children = []
        self.visits = 2

a = Node()
print(*a.children)
a.children.append(Node())
print(a.children)

m = max(a.children, key=lambda nod: nod.visits)

#list = []
#for nod in a.children:
#    list.append((nod, nod.visits))

#m = max(list, key=)