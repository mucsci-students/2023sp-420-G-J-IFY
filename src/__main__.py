import cview.CLI as CLI
import model.puzzle as puzzle
import controller.CommandHandler as CommandHandler
import os
import model.output as output


# TODO, restrict input to JUST !new, !load, and !exit

usrinput = ' '
validIn = False
puzzle = puzzle.Puzzle('', '')
outty = output.Output()

# inital user initialization of game
while not validIn:
    CLI.drawTextBox(['Welcome to Spelling Bee! \ '
                     'Presented by G(J)IFY',
                     'To start a new game, type "!new". To load a previous '
                     'save, type "!load"'], 40, '^')
    if outty.getField != '':
        print(outty.getField())
    usrinput = input('> ')
    #CLI.clear()
    match usrinput:
        case '!new':
            puzzle = CommandHandler.newPuzzle(outty) 
            validIn = True
        case '!load':
            puzzle = CommandHandler.loadGame(puzzle, outty) 
            if puzzle.maxScore == 0:
                validIn = False
            else:
                validIn = True
        case '!exit':
            print('Goodbye!')
            quit()
        case _:
            print(usrinput + " is not a valid command")


CLI.clear()
CLI.drawGameBox(puzzle, outty)
usrinput = input('> ')

while True:
    CLI.clear()
    print('{:═<40}'.format(''))
    puzzle = CommandHandler.parse(usrinput, puzzle, outty)   
    print('{:═<40}'.format(''))
    #check to see if game is over
    if puzzle.getFinishedFlag():
        CommandHandler.finalGame(puzzle, outty)
    #redraw game box
    CLI.drawGameBox(puzzle, outty)
    #prompt for user input                           
    usrinput = input('> ')
    #at the end of loop, reset the output field
    outty.setField('')