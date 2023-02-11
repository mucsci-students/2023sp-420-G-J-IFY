import CLI
import saveState
import CommandHandler
import os

CLI.drawTextBox(['Welcome to Spelling Bee! \ '
                 'Presented by G(J)IFY',
                 'To start a new game, type \"!new\". \ '
                 'To load a previous save, type \"!load\"'], 40, '^')

# TODO, restrict input to JUST !new, !load, and !exit

usrinput = input('> ')
validIn = False
puzzle = saveState.Puzzle('', '')

while not validIn:
    match usrinput:
        case '!new':
            puzzle = CommandHandler.newPuzzle()
            validIn = True
        case '!load':
            puzzle = CommandHandler.loadGame()
            validIn = True
        case '!exit':
            print('Goodbye!')
            quit()
        case _:
            os.system('clear')
            CLI.drawTextBox(['Command Not recognized. Please try again.',
                    'To start a new game, type \"!new\". \ To load a previous '
                    'save, type \"!load\"'], 40, '^')
            usrinput = input('> ')

CLI.clear()
CLI.drawGameBox(puzzle)
usrinput = input('> ')

while True:
    CLI.clear()
    print('{:═<40}'.format(''))
    puzzle = CommandHandler.parse(usrinput, puzzle)
    print('{:═<40}'.format(''))
    CLI.drawGameBox(puzzle)
    usrinput = input('> ')