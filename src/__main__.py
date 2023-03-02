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
    usrinput = input('> ')
    #CLI.clear()
    match usrinput:
        case '!new':
            puzzle = CommandHandler.newPuzzle(outty)
            print(outty.getField())
            validIn = True
        case '!load':
            puzzle = CommandHandler.loadGame(puzzle)
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
CLI.drawGameBox(puzzle)
usrinput = input('> ')

while True:
    CLI.clear()
    print('{:═<40}'.format(''))
    puzzle = CommandHandler.parse(usrinput, puzzle)
    print('{:═<40}'.format(''))
    CLI.drawGameBox(puzzle)
    if puzzle.getFinishedFlag():
        CommandHandler.finalGame(puzzle)
    usrinput = input('> ')