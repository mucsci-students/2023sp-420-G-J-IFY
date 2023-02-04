from src.SpellingBee import CLI
from src.SpellingBee import CommandHandler
import os

CLI.drawTextBox(['Welcome to Spelling Bee! \ Presented by G(J)IFY',
    'To start a new game, type \"!new\". \ To load a previous save, type \"!load\"',
    'For a list of available commands, type \"!help\"'], 40, '^')

while 'True':

    userInput = input('> ').lower()
    CommandHandler.checkCommands(userInput)
    os.system('clear')

    # The following is just a placeholder, mainly just to showcase the idea.
    tier1 = 'Welcome to Spelling Bee! \ Presented by G(J)IFY'
    tier2 = 'Level: \ {lvl} {pBar} \ ({num} more to \'{nxtLvl}\')'.format(lvl = 'Novice', pBar = CLI.drawProgressBar(20, 0.35), num = 8, nxtLvl = 'Okay')
    tier3 = 'Discovered Words: \ {wrds}'.format(wrds = CLI.drawList(['ICING', 'ACING', 'AGING']))
    tier4 = CLI.drawPuzzle(['I', 'O', 'A', 'N', 'G', 'X', 'C'])
    tier5 = 'Enter your guess, or type \'!help\' for a list of commands.'
    CLI.drawTextBox([tier1, tier2, tier3, tier4, tier5], 40, '^')

    print()