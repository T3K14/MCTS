import random
from MCTS import Node, State, MCTS


def playrandom(node):
    """bekommt eine node spielt ab dem dazugehörigen state random zu ende, returned wer gewonnen hat"""

    board = node.state.board[:]
    first_letter = node.player.id
    opponent_letter = 'X' if first_letter == 'O' else 'O'

    # if state schon endstate
    if isWinner(board, first_letter):
        return first_letter
    elif isWinner(board, opponent_letter):
        return opponent_letter

    if isBoardFull(board):
        return 0

    dic = {first_letter: opponent_letter, opponent_letter: first_letter}
    empty = []

    for i, x in enumerate(board[1:]):
        if x == ' ':
            empty.append(i+1)

    let = first_letter
    for i in range(len(empty[:])):

        choice1 = random.choice(empty)
        empty.remove(choice1)
        makeMove(board, let, choice1)

        if isWinner(board, let):
            return let
        else:
            if isBoardFull(board):
                return 0
            else:
                let = dic[let]


def get_possible_next_states(node):
    """function that returnes list with all possible next states"""

    # sollte hier ueberflüssig sein
    if isWinner(node.state.board, 'X') or isWinner(node.state.board, 'O'):
        print("Error, you should never get here!")
        return []

    else:
        let = node.player.id

        empty = []
        next_states = []

        for i, x in enumerate(node.state.board[1:]):
            if x == ' ':
                empty.append(i+1)

        for i in empty:
            board = node.state.board[:]
            makeMove(board, let, i)

            # if the new state is an end-state
            if isWinner(board, let):
                status = False
            else:
                status = True

            next_states.append(State(status, board))

        return next_states


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

def normal_game():
    print("\nWelcome to MonteCarlo-TicTacToe")
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    theBoard = [' '] * 10

    mcts = MCTS(2, playrandom, get_possible_next_states)

    first_letter = playerLetter if turn == 'player' else computerLetter

    for player in mcts.player_list:
        if player.nr == 0:
            player.id = first_letter
        else:
            player.id = playerLetter if first_letter == computerLetter else computerLetter

    mcts.root = Node(State(True, theBoard), mcts.player_list[0])

    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            print('\n')
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            status = True       # da falls das nicht der fall ist in der folgenden Auswertung sowieso das Spiel endet

            next_state = State(status, theBoard)
            mcts.update_root(next_state)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'

        else:
            print('\n')
            print('\n')
            drawBoard(theBoard)

            mcts.root = mcts.find_next_move()
            #choosen_next_state = mcts.find_next_move(tree, tree.root.state.infolist[0])

            # make the move that was choosen by the mcts-algorithm
            for i, entry in enumerate(theBoard):
                if entry != mcts.root.state.board[i]:
                    makeMove(theBoard, computerLetter, i)
                    break

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'


def AI_vs_AI():
    flag = True
    while flag:
        playerLetter = random.choice(('X', 'O'))
        computerLetter = 'O' if playerLetter == 'X' else 'X'
        turn = whoGoesFirst()
        theBoard = [' '] * 10

        mcts = MCTS(2, playrandom, get_possible_next_states)

        first_letter = playerLetter if turn == 'player' else computerLetter

        for player in mcts.player_list:
            if player.nr == 0:
                player.id = first_letter
            else:
                player.id = playerLetter if first_letter == computerLetter else computerLetter

        mcts.root = Node(State(True, theBoard), mcts.player_list[0])

        gameIsPlaying = True

        while gameIsPlaying:
            if turn == 'player':
                print('\n')

                drawBoard(theBoard)
                print('\n')
                mcts.root = mcts.find_next_move()
                # choosen_next_state = mcts.find_next_move(tree, tree.root.state.infolist[0])

                # make the move that was choosen by the mcts-algorithm
                for i, entry in enumerate(theBoard):
                    if entry != mcts.root.state.board[i]:
                        makeMove(theBoard, playerLetter, i)
                        break

                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    print(playerLetter, ' won the game!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'computer'
                        input()

            else:
                print('\n')
                #print('\n')
                drawBoard(theBoard)
                print('\n')

                mcts.root = mcts.find_next_move()
                # choosen_next_state = mcts.find_next_move(tree, tree.root.state.infolist[0])

                # make the move that was choosen by the mcts-algorithm
                for i, entry in enumerate(theBoard):
                    if entry != mcts.root.state.board[i]:
                        makeMove(theBoard, computerLetter, i)
                        break

                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    print(computerLetter, ' won the game!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player'
                        input()

        cont = input('another game?\n')
        if cont not in ['y', 'yes', 'ye']:
            flag = False

normal_game()
# AI_vs_AI()
