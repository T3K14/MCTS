choice1 = random.choice(empty)
empty.remove(choice1)
makeMove(state, 'X', choice1)
if isWinner(theBoard, playerLetter):
    drawBoard(theBoard)
    print('Hooray! You have won the game!')
    #gameIsPlaying = False
    break
else:
    if isBoardFull(theBoard):
        drawBoard(theBoard)
        print('The game is a tie!')
        break
    else:
        turn = 'computer'
else:

choice2 = random.choice(empty)
empty.remove(choice2)
makeMove(state, 'O', choice2)

if isWinner(theBoard, playerLetter):
    drawBoard(theBoard)
    print('Computer won!')
    break
    #gameIsPlaying = False
else:
    if isBoardFull(theBoard):
        drawBoard(theBoard)
        print('The game is a tie!')
        break
    else:
        turn = 'player'