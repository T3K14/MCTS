import random
import sys
import numpy as np

""""not retaining subtree-information
(should follow after implementation)"""


class Tree:
    """class to save the tree and update it to the next node with its children after succesfull choice"""

    def __init__(self, state):
        self.root = Node(state)

    def update_root(self, state):
        self.root = Node(state)


class Node:

    def __init__(self, state, parent=None):

        self.state = state               # current game state (placed tiles, figures, etc)

        self.wins = 0
        self.visits = 0

        self.parent = parent
        self.children = []

        print("normal Node created")

    #@classmethod
    #def create_root_node(cls, state):
    #    print("root created")
    #    return cls(2)

    def add_child(self, child_node):

        self.children.append(child_node)

    def get_child_with_max_score(self):
        pass

    def calculate_UCT_value(self, c=1.4142):

        ############################################# lieber tauschen?
        if self.visits == 0:
            return sys.maxsize
        else:
            return self.wins / self.visits + c * np.sqrt(np.log(self.parent.visits / self.visits))

    # increment visits

    # increment wins

"""brauche funktion, die für irgendein spiel, den status zurückgibt und dazu ebenfalls die liste aller danach möglichen
zustände ausgeben kann, ausser den zufällig spielen kann"""

class State:
    """schnittstelle zum spiel"""
    def __init__(self):
        pass

    def random_play(self):
        pass

    def get_possible_next_states(self):
        pass



class MCTS:


    def find_next_move(self, tree, player):
        """find the best next move in given settings"""

        # startzeit festlegen
        t = 0
        t_end = 1

        #loop: solange zeit übrig:
        while(t < t_end):
            # selection
            promising_node = self.select_next_node(tree.root)

            # expansion if the choosen note does not represent and and-state of the game
            if promising_node.state == 1:
                self.expand(promising_node)

            # simulation
            # backprob

        # auswertung, rückgabe von bestem child-state
            t += 1

        # tree zu dem endzeitpunkt ausgeben
        pass



    def select_next_node(self, root_node):
        """method to choose the next node from the start at root node until one approaches the end of the tree"""

        # POSSIBLE ERROR: wenn in der while schleife nur die erste node berücksichtigt wird und nicht in jeder iteration die neue (eigentlich ausgeschlossen)

        node = root_node

        # as long as there are known children, choose next child-node with uct
        while len(node.children) != 0:

            node = max(*node.children, key=lambda nod: nod.calculate_UCT_value)

        return node


    def expand(self, node):
        """adds new leaf nodes for all possible game states to the node and initializes them correctly"""
        for state in node.state.get_possible_next_states():
            node.children.append(Node(state, node))


    # randomly select next game state
    def random_select_new_node(self, possible_moves):
        """method for choosing the next node out of all possible next game states at random"""

        move = random.choice(possible_moves)

    def simulate(self):
        """method for random simulating until end state and evaluating"""

        pass

    def backprob(self):
        """method for updating w and n of all included nodes in after one simulation process"""

        pass


#def game():
    # erstelle tree

    #loop: abwechselnd spielen spieler ihre züge, zb über mcts oder echte Spieler
        #

    #pass


if __name__ == '__main__':

    tree = Tree(0)
    mcts = MCTS()

    mcts.find_next_move(tree, 2)
    #print(2*float('inf'))
    #print(12000/sys.maxsize)
    #print(sys.maxsize+1)

    mcts.select_next_node(tree.root)


