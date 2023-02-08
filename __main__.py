from src.SpellingBee import CLI
from src.SpellingBee import CommandHandler
import os

CLI.drawTextBox(['Welcome to Spelling Bee! \ Presented by G(J)IFY',
    'To start a new game, type \"!new\". \ To load a previous save, type \"!load\"'], 40, '^')

# TODO, restrict input to JUST !new, !load, and !exit

input = input('> ')
validIn = False

while not validIn:
    match input:
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
                    'To start a new game, type \"!new\". \ To load a previous save, type \"!load\"'], 40, '^')
            input = input('> ')

while True:

    os.system('clear')
    CLI.drawGameBox(puzzle)
    CommandHandler.parse(input('> '), puzzle)