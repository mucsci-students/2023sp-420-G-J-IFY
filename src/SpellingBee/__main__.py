import CLI
import CommandHandler
import os

CLI.drawTextBox(['Welcome to Spelling Bee! \ '
                 'Presented by G(J)IFY',
                 'To start a new game, type \"!new\". \ '
                 'To load a previous save, type \"!load\"'], 40, '^')

# TODO, restrict input to JUST !new, !load, and !exit

usrinput = input('> ')
validIn = False

while not validIn:
    match usrinput:
        case '!new':
            puzzle = CommandHandler.newPuzzle()
            validIn = True
        case '!load':
            puzzle = CommandHandler.loadGame()
            validIn = True
        case '!exit':
            quit()
        case _:
            os.system('clear')
            CLI.drawTextBox(['Command Not recognized. Please try again.',
                    'To start a new game, type \"!new\". \ To load a previous '
                    'save, type \"!load\"'], 40, '^')
            usrinput = input('> ')

while True:

    os.system('clear')
    CLI.drawGameBox(puzzle)
    usrinput = input('> ')
    CommandHandler.parse(usrinput, puzzle)
    input("Press enter to continue. . .")
