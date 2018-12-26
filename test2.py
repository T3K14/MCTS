import random
#from mcts2 import Tree, Node, State, MCTS

class State:

    def __init__(self, board, liste):
        self.board = board
        self.infolist = liste

def playrandom(state):      # letter ist der, von dem der global den besten nächsten zug auswählen
    """bekommt eine liste und setzt darin alle freien einträge zufällig nach und nach mit abwechselnden X oder O und schaut, wer gewinnt und evaluiert"""

    board = state.board[:]
    computer_letter = state.infolist[0]     # letter von dem der dran ist  # letter von dem der dran ist, ist nicht immer auch der letter vom gegner
    turn = state.infolist[1]                # wer dran ist

    if computer_letter == 'O':

        player_letter = 'X'
    else:
        player_letter = 'O'

    empty = []
    out = []

    for i, x in enumerate(board[1:]):

        if x == ' ':
            empty.append(i+1)

    for i in range(len(empty[:])):

        if turn == 'computer':
            choice1 = random.choice(empty)
            empty.remove(choice1)
            makeMove(board, computer_letter, choice1)
            out.append((computer_letter, choice1))
            if isWinner(board, computer_letter):
                drawBoard(board)

                print(out)
                return computer_letter
            else:
                if isBoardFull(board):
                    drawBoard(board)

                    print(out)
                    return 0
                else:
                    turn = 'player'
        else:
            choice2 = random.choice(empty)
            empty.remove(choice2)
            makeMove(board, player_letter, choice2)
            out.append((player_letter, choice2))
            if isWinner(board, player_letter):
                drawBoard(board)

                print(out)
                return player_letter
            else:
                if isBoardFull(board):
                    drawBoard(board)

                    print(out)
                    return 0
                else:
                    turn = 'computer'


def get_possible_next_states(state):

    let = state.infolist[0]

    empty = []
    lis = []

    for i, x in enumerate(state.board[1:]):
        if x == ' ':
            empty.append(i+1)

    for i in empty:
        board = state.board[:]
        #state = state.board[:]
        #state1 = State(state.board, let, state.infolist[1])
        makeMove(board, let, i)
        lis.append(State(board, state.infolist[0], state.infolist[1]))

    return lis


def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')


def inputPlayerLetter():
    # Let's the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

    # 0, player 0 with O, 1 player 1 with X
    #return random.randint(0, 1)


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal


def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '


def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)


def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


# ai to replace
def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def is_normal_state(state):

    if get_possible_next_states(state):
        state.status = True
    else:
        state.status = False








if __name__ == '__main__':

    print('Welcome to MCTS-Tic Tac Toe!')

    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()

    theBoard = [' '] * 10
    #theBoard[2] = "X"


    playrandom(State(theBoard, []))