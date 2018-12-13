import random

""""not retaining subtree-information
(should follow after implementation)"""


class Tree(object):
    """class to save the tree and update it to the next node with its children after succesfull choice"""
    root = None

    def __init__(self, state):
        Tree.root = Node(state)

    def set_root(self, state):
        Tree.root = Node(state)

    def add_node(self, state, parent):
        pass

    def update_tree(self, new_root_node):
        """method to update the tree to new starting root"""
        Tree.root = new_root_node

    def print_root(self):
        print(Tree.root)

class Node:

    def __init__(self, state, parent=None):

        self.state = state               # current game state (placed tiles, figures, etc)

        self.w = 0
        self.n = 0

        self.parent = parent
        self.children = []

        print("normal created")

    @classmethod
    def create_root_node(cls, state):
        print("root created")
        return cls(2)


class MCTS:

    def create_tree(self, state):
        tree = Tree()

    def find_next_move(self, game_state):
        """find the best next move in given settings"""

        pass

    def select_node(self):
        pass

    def expand_node(self):
        pass

    def select_next_node_random(self, possible_moves):
        """method for choosing the next node out of all possible next game states at random"""

        move = random.choice(possible_moves)

    def select_next_node(self):
        """method to choose the next node out of all possible next game states"""

        pass

    def simulate(self):
        """method for random simulating until end state and evaluating"""

        pass

    def backprob(self):
        """method for updating w and n of all included nodes in after one simulation process"""

        pass

