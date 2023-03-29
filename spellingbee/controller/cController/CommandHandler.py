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
#   parse(userinput : str, game : object, outty : object) -> object
#
#   newPuzzle() -> object:
#
#   printPuzzle(game : object) -> None
#
#   printWords(game : object) -> None
#
#   showStatus(game : object) -> None
#
#   saveGame(game : object, outty : object) -> None
#
#   savePuzzle(game : object, outty : object) -> None 
#
#   loadGame(game : object, outty : object) -> None
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
#import model.output as output



current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

from View.CLI import CLI
from model import MakePuzzle, StateStorage
from model import hint
from os import path


commands = [
    '!new',
    '!puzzle',
    '!found-words',
    '!status',
    '!shuffle',
    '!save',
    '!savePuzzle',
    '!load',
    '!help',
    '!exit',
    '!hint'
]

################################################################################
# parse(userinput : str, game : object, outty : object) -> object:
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
#   outty : object
#     - output object storing output strings
#
# RETURN:
#   object
#     - updated puzzle object
################################################################################
def parse(usrinput : str, game : object, outty) -> object:
    match usrinput:
        case '!new':
            return newPuzzle(outty)
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
            outty.setField('Shuffling letters...')
            return game
        case '!save':
            saveGame(game, outty)
            return game
        case '!savePuzzle':
            savePuzzle(game, outty)
            return game
        case '!load':
            return loadGame(game, outty)
        case '!save-list':
            outty.setField('Implementation Pending...')
        case '!help':
            help()
            return game
        case '!exit':
            exit(game, outty)
            return game
        case '!hint':
            hints(game, outty)
        case _:
            if usrinput.startswith('!'):
                outty.setField('Command not recognized. Type \"!help\" for a list of '
                      'valid commands...')
                return game

            elif not usrinput.isalpha():
                outty.setField('Input not accepted:\n'
                      '\t~Guesses should only contain alphabetical characters.')
                return game
                
            else:
                MakePuzzle.guess(game, usrinput, False, outty)
                return game


################################################################################
# newPuzzle() -> None:
#
# DESCRIPTION:
#   prompts for input and directs functionality to create a new puzzle object.
#
#  PARAMETERS:
#   outty : object
#     - output object storing output strings
#
# RETURN:
#   object
#     - new puzzle object
################################################################################
def newPuzzle(outty) -> object:
    print('Please enter a base word with exactly 7 unique characters. \n' +
    'For auto-generated base word, press enter.')
    word = input('> ')
    keyLetter = ''
    if word != '':
        keyLetter = input("Enter a letter from your word "
                      "to use as the key letter\n> ")
    out = MakePuzzle.newPuzzle(word.lower(), keyLetter.lower(), outty, False)
    if outty.getField().startswith("ERROR"):
        print(outty.getField())
        outty.setField('')
    else:
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
#   outty : object
#     - output object storing output strings
################################################################################
def saveGame(game : object, outty : object) -> None:
    handleSave(game, 0, outty)


################################################################################
# savePuzzle(game : object) -> None:
#
# DESCRIPTION:
#   creates a new save entry for JUST the puzzle data of the game.
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state
#   outty : object
#     - output object storing output strings
################################################################################
def savePuzzle(game : object, outty) -> None:
    handleSave(game, 1, outty)


################################################################################
# loadGame(game : object) -> None:
#
# DESCRIPTION:
#   load an existing save entry into memory
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state
#   outty : object
#     - output object storing output strings
################################################################################
def loadGame(game : object, outty) -> None:
    fileName = input('Please enter the name of the game you are looking for.'
                     '\n> ')
    newGame =  StateStorage.loadPuzzle(fileName, outty)
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
                '(not including any progress from current session) \ '
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
def exit(game, outty) -> None:
    print('Are you sure? all unsaved progress will be lost. [Y/N]')
    usrinput = input('> ').upper()
    match usrinput:
        case 'Y':
            outty.setField("Thank you for playing!")
    
            quit()
        case 'N':
            return
        case _:
            outty.setField('Input Invalid')
            parse('!exit', game, outty) # recursively calls until valid input provided.


################################################################################
# handleSave(game : object, num : int, outty : object) -> None:
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
#   outty : object
#     - output object storing output strings
################################################################################
def handleSave(game : object, num : int, outty : object) -> None:
    saveStatus = False
    fileName = input('Please enter the name of the file you would like to save '
                     'for example "Game1"\n> ')
    os.chdir('./saves')
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
        
    os.chdir('..')

################################################################################
# finalGame(finishedPuzzle : object, outty : object) -> None
#
# DESCRIPTION:
#   Notifies the user that they have found all the words for the currently
#   active game.
#
# PARAMETERS:
#   finishedPuzzle : object
#     - puzzle object for the currently active (and finished) game.
#   outty : object
#     - output object storing output strings
################################################################################
def finalGame(finishedPuzzle : object, outty) -> None:
    showStatus(finishedPuzzle)
    outty.setField("Congratulations!!!! You have found all of the words for this puzzle!")  

################################################################################
# hints(puzzle: object, outty: object) -> None
#
# DESCRIPTION:
#   Prints the hints, including the hints gird, number of words, 2 letter list, etc
# PARAMETERS:
#   puzzle : object
#     - puzzle object for the currently active game.
#   outty : object
#     - output object storing output strings

################################################################################
def hints(game: object, outty: object) -> None:
    gameLetters = formatGameLetts(game)
    hintHeader = ('Spelling Bee Hint Grid \ '
                  ' \ '
                  'Center letter is capitalized. \ '
                  ' \ '
                  f'{gameLetters}'
                  
                )
    
    lengthHeaderStr = lengthHeader()
    hintGrid = formatHintGrid(game)

    grid = (f'{lengthHeaderStr} \ '
            f'{hintGrid}')
    
    CLI.drawTextBox([hintHeader, grid], 60, '<')

################################################################################
# formatGameLetts(game:object) -> str
#
# DESCRIPTION:
#   Formats the letters of the Game to be printed
# PARAMETERS:
#   puzzle : object
#     - puzzle object for the currently active game.
# Returns:
#   fStr: str
#       a format string of the game letters

################################################################################
def formatGameLetts(game:object) -> str:
    fStr = ''
    uniqueLetters = game.getShuffleLetters()

    counter = 0
    for i in uniqueLetters:
        if counter == 0:
            fStr += i.capitalize() + ' '
        else:
            fStr += i + ' '
        counter += 1
    return fStr

################################################################################
# formatHintGrid(game:object) -> str
#
# DESCRIPTION:
#   Formats the the hints grid of the Game to be printed
# PARAMETERS:
#   puzzle : object
#     - puzzle object for the currently active game.
# Returns:
#   fStr: str
#       a format string of the hint grid

################################################################################
def formatHintGrid(game:object) -> str:
    hintGrid = hint.hint(game)
    hintGrid.makeHintGrid(game)
    lst = hintGrid.hint
    fStr = ''
    for i in lst:
        fStr += f'{i} \ '
    return fStr

################################################################################
# lengthHeader() -> str
#
# DESCRIPTION:
#   Formats the word lengths of the Game to be printed
# PARAMETERS:
#   puzzle : object
#     - puzzle object for the currently active game.
# Returns:
#   fStr: str
#       a format string of the lengths of the words including sigma

################################################################################
def lengthHeader() -> str:
    fStr =''
    sigma = "Σ"
    for i in range(4,17):
        if i == 16:
            fStr += f'{sigma:>5}'
        else:
            fStr += f'{i:10}'

    return fStr