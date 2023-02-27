################################################################################
# CommandHandler.py
# AUTHOR: Isaak Weidman, Jacob Lovegren
# DATE OF CREATION: -
#
# DESCRIPTION:
#   Routs functionality from user-input into backend of the project, then
#   updates the display to reflect those changes.
#
# FUNCTIONS:
#   parse(userinput : str, game : object) -> object
#
#   newPuzzle() -> object:
#
#   printPuzzle(game : object) -> None
#
#   printWords(game : object) -> None
#
#   showStatus(game : object) -> None
#
#   saveGame(game : object) -> None
#
#   savePuzzle(game : object) -> None 
#
#   loadGame(game : object) -> None
#
#   help() -> None
#
#   exit() -> None
#
#   handleSave(game : object, num : int) -> None
#
#   finalGame(finishedPuzzle : object) -> None
################################################################################
import sys
import os


current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import cview as CLI
from model import MakePuzzle, StateStorage
from os import path

################################################################################
# parse(userinput : str, game : object) -> object:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
# 
# PARAMETERS:
#   usrinput : str
#     - string provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - puzzle object storing current game state
#
# RETURN:
#   object
#     - updated puzzle object
################################################################################
def parse(usrinput : str, game : object) -> object:
    match usrinput:
        case '!new':
            return newPuzzle()
        case '!puzzle':
            printPuzzle(game)
            return game
        case '!found-words':
            printWords(game)
            return game
        case '!status':
            showStatus(game)
            return game
        case '!shuffle':
            game.shuffleChars()
            print('Shuffling letters...')
            return game
        case '!save':
            saveGame(game)
            return game
        case '!savePuzzle':
            savePuzzle(game)
            return game
        case '!load':
            return loadGame(game)
        case '!save-list':
            print ('Implementation Pending...')
        case '!help':
            help()
            return game
        case '!exit':
            exit(game)
            return game
        case _:
            if usrinput.startswith('!'):
                print('Command not recognized. Type \"!help\" for a list of '
                      'valid commands...')
                return game

            elif not usrinput.isalpha():
                print('Input not accepted:\n'
                      '\t~Guesses should only contain alphabetical characters.')
                return game
                
            else:
                MakePuzzle.guess(game, usrinput)
                return game


################################################################################
# newPuzzle() -> None:
#
# DESCRIPTION:
#   prompts for input and directs functionality to create a new puzzle object.
#
# RETURN:
#   object
#     - new puzzle object
################################################################################
def newPuzzle() -> object:
    print('Please enter a base word with exactly 7 unique characters. \n' +
    'For auto-generated base word, press enter.')
    word = input('> ')
    out = MakePuzzle.newPuzzle(word.lower())
    out.shuffleChars()
    return(out)


################################################################################
# printPuzzle(game : object) -> None:
#
# DESCRIPTION:
#   prints puzzle data in a neatly formatted box
#
# PRAMETERS:
#   game : object
#     - puzzle object storing current game state
################################################################################
def printPuzzle(game : object) -> None:
    CLI.drawTextBox([CLI.drawPuzzle(game.getShuffleLetters().upper())], 
                    40, '^')


################################################################################
# printWords(game : object) ->
#
# DESCRIPTION:
#   prints list of discovered words in a neatly formatted text box
#
# PARAMETERS:
#   game : object
#     - puzzle object storing current game state
################################################################################
def printWords(game : object) -> None:
    CLI.drawTextBox(
        ['Discovered Words: \ {wrds}'.format(wrds = game.getFoundWords())], 
        40, '^')


################################################################################
# showStatus(game : object) -> None
#
# DESCRIPTION:
#   prints the current user rank, score, a progress bar and percent progress
#   in a neatly formatted text box.
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state.
################################################################################
def showStatus(game : object) -> None:
    score = game.getScore()
    max = game.getMaxScore()
    prog = score/max
    bar = game.getRank() + ' ' + CLI.drawProgressBar(20, prog)
    stats = 'Score: {} \ Progress: {}%'.format(score, int(prog*100))
    CLI.drawTextBox(['Level: \ ' + bar + ' \ ' + stats], 40, '^')


################################################################################
# saveGame(Game : object) -> None:
#
# DESCRIPTION:
#   creates a new save entry for the overall status of the game.
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state
################################################################################
def saveGame(game : object) -> None:
    handleSave(game, 0)


################################################################################
# savePuzzle(game : object) -> None:
#
# DESCRIPTION:
#   creates a new save entry for JUST the puzzle data of the game.
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state
################################################################################
def savePuzzle(game : object) -> None:
    handleSave(game, 1)


################################################################################
# loadGame(game : object) -> None:
#
# DESCRIPTION:
#   load an existing save entry into memory
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state
################################################################################
def loadGame(game : object) -> None:
    fileName = input('Please enter the name of the game you are looking for.'
                     '\n> ')
    newGame =  StateStorage.loadPuzzle(fileName)
    if newGame != None:
        game = newGame
    return(game)


################################################################################
# help() -> None
#
# DESCRIPTION:
#   provides a brief description of game rules and generally how to play as well
#   as a list of all available commands.
################################################################################
def help() -> None:
    descHead = ('How to play: \ ')
    descBody = ("Simply type a word after the '> ' prompt and press enter "
                "to submit a guess. \ \ "
                "To enter a command, simply type '!' followed by the command "
                "you wish to use.")

    commHead = ('Available Commands: \ ')
    commBody = ('!new: \ '
                'Generates a new puzzle from a base word with exactly 7 '
                'unique characters, or an auto-generated base word. \ '
                '!puzzle: \ '
                'Prints the current puzzle to the screen \ '
                '!found-words: \ '
                'Displays the list of all discovered words \ '
                '!status: \ '
                'Prints your achieved level for the active game \ '
                '!shuffle: \ '
                'Shuffle the order of the active puzzle for a fresh view \ '
                '!save: \ '
                'Create a new save for the current game \ '
                '!savePuzzle: \ '
                'Create a new save for a blank version of the current game '
                '(not including any progress from current session)'
                '!load: \ '
                'Load a previously saved game \ '
                '!help: \ '
                'Show the list of all available commands with a brief '
                "description. (You're here now!) \ "
                '!exit: \ '
                'Exit the game ')
    
    CLI.drawTextBox([descHead, descBody], 40, '<')
    CLI.drawTextBox([commHead, commBody], 40, '<')


################################################################################
# exit() -> None:
#
# DESCRIPTION:
#   prompts user for confirmation, then quits the game.
################################################################################
def exit(game) -> None:
    print('Are you sure? all unsaved progress will be lost. [Y/N]')
    usrinput = input('> ').upper()
    match usrinput:
        case 'Y':
            print("Thank you for playing!")
            quit()
        case 'N':
            return
        case _:
            print('Input Invalid')
            parse('!exit', game) # recursively calls until valid input provided.


################################################################################
# handleSave(game : object, num) -> None:
#
# DESCRIPTION:
#   saves the games state and handles input from the user to determin if they
#   want to overwrite a file or not
# 
# PARAMETERS:
#   game : object
#     - puzzle object storing current game state
#   num : int
#     - an integer value to determin if we are saving all the game progress
#       or just the pzzle. 0 for saveCurrent() and 1 for savePuzzle().
################################################################################
def handleSave(game : object, num : int) -> None:
    saveStatus = False
    fileName = input('Please enter the name of the file you would like to save '
                     'for example "Game1"\n> ')
    if(path.isfile(fileName +'.json')):
        yesOrNo = input('Would you like to overwrite the file ' + fileName + '?'
                        '\n Enter Y for yes or N for no\n> ')
        if(yesOrNo == 'Y'):
            if(num == 0):
                StateStorage.saveCurrent(game, fileName)
                saveStatus = True
            elif(num == 1):
                StateStorage.savePuzzle(game, fileName)
                saveStatus = True
    else: 
        if(num == 0):
            StateStorage.saveCurrent(game, fileName)
            saveStatus = True
        elif(num == 1):
            StateStorage.savePuzzle(game, fileName)
            saveStatus = True
    
    if saveStatus:
        print('Save Complete!')
    else:
        print('Game could not be saved.')

################################################################################
# finalGame(finishedPuzzle : object) -> None
#
# DESCRIPTION:
#   Notifies the user that they have found all the words for the currently
#   active game.
#
# PARAMETERS:
#   finishedPuzzle : object
#     - puzzle object for the currently active (and finished) game.
################################################################################
def finalGame(finishedPuzzle : object) -> None:
    showStatus(finishedPuzzle)
    print("Congratulations!!!!\nYou have found all of the\nwords for this puzzle!")  