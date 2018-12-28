import random
import sys
import numpy as np


class Player:

    def __init__(self, nr, id=None):
        self.id = id
        self.nr = nr


class Node:

    def __init__(self, state, player=None, parent=None):

        self.state = state  # current game state (placed tiles, figures, etc)
        self.player = player

        self.wins = 0
        self.visits = 0

        self.parent = parent
        self.children = []

    def add_child(self, child_node):

        self.children.append(child_node)

    def get_best_child(self):
        return max(self.children, key=lambda nod: nod.visits)

    def calculate_UCT_value(self, c=1.4142):

        if self.visits == 0:
            return sys.maxsize
        else:
            result = self.wins / self.visits + c * np.sqrt(np.log(self.parent.visits / self.visits))
            return result


class State:
    """connection to the game (eg knows the board etc)"""

    def __init__(self, status, board, *args):
        self.board = board
        self.infolist = [i for i in args]

        self.status = status


class MCTS:
    """MCTS-class with essential update functions and the core algorithm functions"""

    def __init__(self, player_number, random_play, get_possible_next_states):

        self.root = None
        self.next_player = {}
        self.player_list = [Player(i) for i in range(player_number)]

        for i in range(player_number):
            if i+1 < player_number:
                self.next_player.update({self.player_list[i]: self.player_list[i+1]})
            else:
                self.next_player.update({self.player_list[i]: self.player_list[0]})

        self.random_play = random_play
        self.get_possible_next_states = get_possible_next_states

    def update_root(self, new_state):
        """method to update the root, if another player made a move"""
        if self.root.children:
            for child in self.root.children:

                if child.state.board == new_state.board:
                    self.root = child
        else:
            # another player made the first move of the game
            self.root = Node(new_state, self.next_player[self.root.player])

    # not used but can be for better understanding
    def get_next_player(self, player):
        return self.next_player[player]

    def find_next_move(self):
        """find the best next move in given settings"""

        # start time replacement
        t = 0
        t_end = 3000

        # loop as long as time is left:
        while t < t_end:

            # selection
            promising_node = self.select_next_node()

            # expansion if the choosen note does not represent an and-state of the game
            if promising_node.state.status:
                self.expand(promising_node)

            # simulation

            # if there has been an expansion select next node at random, else evaluate instant
            choosen_node = promising_node
            if len(promising_node.children) > 0:
                choosen_node = random.choice(promising_node.children)
            result = self.random_play(choosen_node)

            # backprob

            self.backprop(choosen_node, result)

            t += 1
        # return the most visited child node with the "best next move"
        return self.root.get_best_child()

    def select_next_node(self):
        """method to choose the next node from the start at root node until one approaches the end of the tree"""

        node = self.root

        # as long as there are known children, choose next child-node with uct
        while len(node.children) != 0:
            node = max(node.children, key=lambda nod: nod.calculate_UCT_value())

        return node

    def expand(self, node):
        """adds new leaf nodes for all possible game states to the node and initializes them correctly"""

        # player of all child nodes is not player of parent node
        player = self.next_player[node.player]

        for state in self.get_possible_next_states(node):
            node.children.append(Node(state, player, node))

    def backprop(self, node, result):
        """method for updating wins and visits of all included nodes after one simulation

        takes the node from where the simulation started and the result of the simulation (0 for tie or player-instance
        for winning player"""

        # if simulated game ended with a draw
        if result == 0:
            while node.parent != None:
                node.visits += 1
                node.wins += 0.5
                node = node.parent

            # for the root node:
            node.visits += 1
            node.wins += 0.5

        else:
            while node.parent != None:
                node.visits += 1

                if node.player.id != result:           # if the player for that node did not win
                    node.wins += 1
                node = node.parent

            # for the root node:
            node.visits += 1
            if node.player.id != result:
                node.wins += 1


if __name__ == '__main__':
    print("In MCTS.py script")