import CLI
import CommandHandler
import os

os.system('clear')
CLI.drawTextBox(['Welcome to Spelling Bee! \ Presented by G(J)IFY',
    'To start a new game, type \"!new\". \ To load a previous save, type \"!load\"'], 40, '^')

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
                    'To start a new game, type "!new". \ To load a previous save, type "!load"'], 40, '^')
            usrinput = input('> ')

os.system('clear')
CLI.drawGameBox(puzzle)
print('{:═<40}'.format(''))
usrinput = input('> ')

while True:
    os.system('clear')
    print('{:═<40}'.format(''))
    CommandHandler.parse(usrinput, puzzle)
    print('{:═<40}'.format(''))
    CLI.drawGameBox(puzzle)
    usrinput = input('> ')
