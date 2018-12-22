import random
import sys
import numpy as np

#from tictactoe2 import get_possible_next_states, playrandom

class Tree:
    """class to save the tree and update it to the next node with its children after succesfull choice"""

    def __init__(self, state):
        self.root = Node(state)

    def update_root(self, state):
        self.root = Node(state)


class Node:

    def __init__(self, state, player=0, parent=None):

        self.state = state          # current game state (placed tiles, figures, etc)
        self.player = player        # bool, True 1, False 0

        self.wins = 0
        self.visits = 0

        self.parent = parent
        self.children = []

        #print("normal Node created")

    #@classmethod
    #def create_root_node(cls, state):
    #    print("root created")
    #    return cls(2)

    def add_child(self, child_node):

        self.children.append(child_node)

    def get_best_child(self):
        return max(self.children, key=lambda nod: nod.visits)

    def calculate_UCT_value(self, c=1.4142):

        ############################################# lieber tauschen?
        if self.parent.visits == 0:
            if self.visits == 0:
                return sys.maxsize
            else:
                return self.wins/self.visits

        if self.visits == 0:
            return sys.maxsize
        else:
            result = self.wins / self.visits + c * np.sqrt(np.log(self.parent.visits / self.visits))
            return result
    # increment visits

    # increment wins

"""brauche funktion, die für irgendein spiel, den status zurückgibt und dazu ebenfalls die liste aller danach möglichen
zustände ausgeben kann, ausserdem zufällig spielen kann"""


class State:
    """schnittstelle zum spiel, weiß wer dran ist, wer welche Frabe hat, kennt Spielbrett, etc"""
    def __init__(self, board, *args):
        self.board = board
        self.infolist = [i for i in args]

        self.status = True



    def is_normal_state(self, extern_get_next_states):

        states = extern_get_next_states(self)

        if states:
            return True
        else:
            return False

    # to update the state after another player made a move (go the tree one step down to the node that represents
    # the played move)
    def update_state(self, tree, state):

        """ wenn die rootnode keine kinder hat, wird der jetzige stand als neuer root-state festgelegt
           ansonsten wird das kind, welches den gespielten state repräsentiert zum root gemacht, von wo aus dann
           weiter gespielt wird"""

        if tree.root.children:
            for child in tree.root.children:

                if child.state == state:
                    tree.root = child
                    break
        else:
            tree.root.state = state

    def random_play(self):
        from tictactoe2 import playrandom
        return playrandom(self)

    def get_possible_next_states(self):

        from tictactoe2 import get_possible_next_states
        return get_possible_next_states(self)

        #states = extern_get_next_states(self)
        #if states:
        #    return True, states
        #else:
        #    return False, states


class MCTS:

    def __init__(self, number_players):

        self.players = number_players

    def set_starting_player(self, tree, player):
        tree.root.player = player

    def find_next_move(self, tree):
        """find the best next move in given settings"""

        # startzeit festlegen
        t = 0
        t_end = 100

        # loop: solange zeit übrig:
        while t < t_end:

            # selection
            promising_node = self.select_next_node(tree.root)

            # expansion if the choosen note does not represent an and-state of the game
            if promising_node.state.status:
                self.expand(promising_node)

            # simulation

            # if there has been an expansion select next node at random, else evaluate instant
            choosen_node = promising_node
            if len(promising_node.children) > 0:
                choosen_node = random.choice(promising_node.children)
            result = self.simulate(choosen_node)        # result ist wert(1 für win, 0 for loss, 0.5 for tie

            # backprob

            player = tree.root.player

            self.backprob(promising_node, player, result)

            t += 1
        # auswertung, rückgabe von bestem child-state
        best_node = tree.root.get_best_child()

        tree.root = best_node

        return best_node.state

        # tree zu dem endzeitpunkt ausgeben


    def select_next_node(self, root_node):
        """method to choose the next node from the start at root node until one approaches the end of the tree"""

        # POSSIBLE ERROR: wenn in der while schleife nur die erste node berücksichtigt wird und nicht in jeder iteration die neue (eigentlich ausgeschlossen)

        node = root_node

        # as long as there are known children, choose next child-node with uct
        while len(node.children) != 0:

            node = max(*node.children, key=lambda nod: nod.calculate_UCT_value())

        return node


    def expand(self, node):
        """adds new leaf nodes for all possible game states to the node and initializes them correctly"""

        # player of all child nodes is not player of parent node
        player = not node.player

        if node.state.infolist[0] == 'X':
            let = 'O'
        else:
            let = 'X'

        if node.state.infolist[1] == 'player':
            turn = 'computer'
        else:
            turn = 'player'

        #for state in node.get_best_child():

        for state in node.state.get_possible_next_states():
            node.children.append(Node(State(state.board, let, turn), player, node))


    # randomly select next game state #UNNÖTIG
    def random_select_new_node(self, possible_moves):
        """method for choosing the next node out of all possible next game states at random"""

        move = random.choice(possible_moves)


    def simulate(self, node):
        """method for random simulating until end state and evaluating

        needs a function that can play the wanted game random from any state till the end only given the game state
        of the starting node

        this play_random-function has to return the result of the played game in  a format that can be evaluated
        by MCTS"""

        #choice = random.choice(start_node.children)
        return node.state.random_play()        #0 loss, 1 victory, 0.5 tie


    def backprob(self, node, player, result):
        """method for updating weights and visits of all included nodes in after one simulation process"""

        while node.parent != None:
            node.visits += 1

            # if node corresponds to the same player
            if node.player == player:
                node.wins += result

            node = node.parent


if __name__ == '__main__':
    print("In MCTS.py script")