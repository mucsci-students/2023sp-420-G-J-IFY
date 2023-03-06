import cview.CLI as CLI
import model.puzzle as puzzle
import controller.cController as CommandHandler
import model.output as output
import os


#Start of game declarations for needed objects and fields
outty = output.Output()
usrinput = ' '
validIn = False
puzzle = puzzle.Puzzle('', '')

# inital game loop, loop until valid start is reached
while not validIn:
    if outty.getField() != '':
        print(outty.getField())
    CLI.drawTextBox(['Welcome to Spelling Bee! \ '
                     'Presented by G(J)IFY',
                     'To start a new game, type "!new". To load a previous '
                     'save, type "!load"'], 40, '^')
    usrinput = input('> ')
    match usrinput:
        #new game
        case '!new':
            puzzle = CommandHandler.newPuzzle(outty)
            validIn = True
        #load game
        case '!load':
            puzzle = CommandHandler.loadGame(puzzle, outty)
            #check and see if valid game was loaded
            if puzzle.maxScore == 0:
                validIn = False
            else:
                validIn = True
        #exit
        case '!exit':
            print('Goodbye!')
            quit()
        #invalid command
        case _:
            print(usrinput + " is not a valid command")
    #check and see if bad puzzle object was returned somewhere
    if puzzle == None:
        validIn = False

#after start of game loop, draw new game for first time
CLI.clear()
CLI.drawGameBox(puzzle, outty)
usrinput = input('> ')

#game loop
while True:
    CLI.clear()
    #parse user input
    retPuzzle = CommandHandler.parse(usrinput, puzzle, outty)
    #check to see if return puzzle was None (error occuered)
    if retPuzzle != None:
        puzzle = retPuzzle
    #draw game box
    CLI.drawGameBox(puzzle, outty)
    #reset outty
    outty.setField('')
    #check for end of game flag
    if puzzle.getFinishedFlag():
        CommandHandler.finalGame(puzzle, outty)
    #wait for user's next input
    usrinput = input('> ')