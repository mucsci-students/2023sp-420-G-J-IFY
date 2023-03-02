import cview.CLI as CLI
import model.puzzle as puzzle
import controller.cController as CommandHandler
import model.output as output
import os


# TODO, restrict input to JUST !new, !load, and !exit
outty = output.Output()
usrinput = ' '
validIn = False
puzzle = puzzle.Puzzle('', '')

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
CLI.drawGameBox(puzzle, outty)
usrinput = input('> ')

while True:
    CLI.clear()
    print('{:═<40}'.format(''))
    puzzle = CommandHandler.parse(usrinput, puzzle, outty)
    print('{:═<40}'.format(''))
    CLI.drawGameBox(puzzle, outty)
    if puzzle.getFinishedFlag():
        CommandHandler.finalGame(puzzle)
    usrinput = input('> ')