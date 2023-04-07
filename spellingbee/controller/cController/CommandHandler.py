###############################################################################
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
###############################################################################
from cview import CLI
from model import MakePuzzle, StateStorage
from model import hint
from os import path
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

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


###############################################################################
# parse(userinput : str, game : object, outty : object) -> object:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
#
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - Puzzle object storing current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - Updated puzzle object
###############################################################################
def parse(usrinput: str, game: object, outty) -> object:
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
                outty.setField('Command not recognized. Type \"!help\" '
                               'for a list of valid commands...')
                return game
            elif not usrinput.isalpha():
                outty.setField('Input not accepted:\n'
                               '\t~Guesses should only contain '
                               'alphabetical characters.')
                return game
            else:
                MakePuzzle.guess(game, usrinput, False, outty)
                return game


###############################################################################
# newPuzzle() -> None:
#
# DESCRIPTION:
#   Prompts for input and directs functionality to create a new puzzle object.
#
#  PARAMETERS:
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - New puzzle object
###############################################################################
def newPuzzle(outty) -> object:
    print('Please enter a base word with exactly 7 unique characters. \n'
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
        return (out)


###############################################################################
# printPuzzle(game : object) -> None:
#
# DESCRIPTION:
#   Prints puzzle data in a neatly formatted box
#
# PRAMETERS:
#   game : object
#     - Puzzle object storing current game state
#
# RETURNS:
#   None
###############################################################################
def printPuzzle(game: object) -> None:
    CLI.drawTextBox([CLI.drawPuzzle(game.getShuffleLetters().upper())],
                    40, '^')


###############################################################################
# printWords(game : object) -> None
#
# DESCRIPTION:
#   Prints list of discovered words in a neatly formatted text box
#
# PARAMETERS:
#   game : object
#     - Puzzle object storing current game state
#
# RETURNS:
#   None
###############################################################################
def printWords(game: object) -> None:
    CLI.drawTextBox(
        ['Discovered Words: \ {wrds}'.format(wrds=game.getFoundWords())],
        40, '^')


###############################################################################
# showStatus(game : object) -> None
#
# DESCRIPTION:
#   Prints the current user rank, score, a progress bar and percent progress
#   in a neatly formatted text box.
#
# PARAMETERS:
#   game : object
#     - Puzzle object storing the current game state.
#
# RETURNS:
#   None
###############################################################################
def showStatus(game: object) -> None:
    score = game.getScore()
    max = game.getMaxScore()
    prog = score / max
    bar = game.getRank() + ' ' + CLI.drawProgressBar(20, prog)
    stats = 'Score: {} \ Progress: {}%'.format(score, int(prog * 100))
    CLI.drawTextBox(['Level: \ ' + bar + ' \ ' + stats], 40, '^')


###############################################################################
# saveGame(Game : object) -> None:
#
# DESCRIPTION:
#   creates a new save entry for the overall status of the game.
#
# PARAMETERS:
#   game : object
#     - Puzzle object storing the current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   None
###############################################################################
def saveGame(game: object, outty: object) -> None:
    handleSave(game, 0, outty)


###############################################################################
# savePuzzle(game : object) -> None:
#
# DESCRIPTION:
#   Creates a new save entry for JUST the puzzle data of the game.
#
# PARAMETERS:
#   game : object
#     - Puzzle object storing the current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   None
###############################################################################
def savePuzzle(game: object, outty) -> None:
    handleSave(game, 1, outty)


###############################################################################
# loadGame(game : object) -> None:
#
# DESCRIPTION:
#   Load an existing save entry into memory
#
# PARAMETERS:
#   game : object
#     - Puzzle object storing the current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   None
###############################################################################
def loadGame(game: object, outty) -> None:
    fileName = input('Please enter the name of the game you are looking for.'
                     '\n> ')
    newGame = StateStorage.loadPuzzle(fileName, outty)
    if newGame is not None:
        game = newGame
    return (game)


###############################################################################
# help() -> None
#
# DESCRIPTION:
#   Provides a brief description of game rules and generally how to play as
#   well as a list of all available commands.
#
# PARAMETERS:
#   None
#
# RETURNS:
#   None
###############################################################################
def help() -> None:
    f = open('spellingbee/controller/cController/helpOut.txt', 'r')
    fileContents = f.read()
    print(fileContents)
    f.close()
    input("Press enter to return to the game: ")


###############################################################################
# exit() -> None:
#
# DESCRIPTION:
#   Prompts user for confirmation, then quits the game.
#
# PARAMETERS:
#   None
#
# RETURNS:
#   None
###############################################################################
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
            # recursively calls until valid input provided.
            parse('!exit', game, outty)


###############################################################################
# handleSave(game : object, num : int, outty : object) -> None:
#
# DESCRIPTION:
#   Saves the games state and handles input from the user to determin if they
#   want to overwrite a file or not
#
# PARAMETERS:
#   game : object
#     - Puzzle object storing current game state
#   num : int
#     - An integer value to determin if we are saving all the game progress
#       or just the pzzle. 0 for saveCurrent() and 1 for savePuzzle().
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   None
###############################################################################
def handleSave(game: object, num: int, outty: object) -> None:
    saveStatus = False
    fileName = input('Please enter the name of the file you would like to save'
                     ' for example "Game1"\n> ')
    if len(fileName) < 1:
        print('Must enter a file name with a length greater then 0\n')
        handleSave(game, num, outty)
    else:
        os.chdir('./saves')
        if (path.isfile(fileName + '.json')):
            print('Would you like to overwrite the file ' + fileName + '?')
            yesOrNo = input('Enter Y for yes or N for no\n> ')
            if (yesOrNo == 'Y'):
                if (num == 0):
                    StateStorage.saveCurrent(game, fileName)
                    saveStatus = True
                elif (num == 1):
                    StateStorage.savePuzzle(game, fileName)
                    saveStatus = True
        else:
            if (num == 0):
                StateStorage.saveCurrent(game, fileName)
                saveStatus = True
            elif (num == 1):
                StateStorage.savePuzzle(game, fileName)
                saveStatus = True
        if saveStatus:
            print('Save Complete!')
        else:
            print('Game could not be saved.')
        os.chdir('..')


###############################################################################
# finalGame(finishedPuzzle : object, outty : object) -> None
#
# DESCRIPTION:
#   Notifies the user that they have found all the words for the currently
#   active game.
#
# PARAMETERS:
#   finishedPuzzle : object
#     - Puzzle object for the currently active (and finished) game.
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   None
###############################################################################
def finalGame(finishedPuzzle: object, outty) -> None:
    showStatus(finishedPuzzle)
    outty.setField("Congratulations!!!!"
                   " You have found all of the words for this puzzle!")


###############################################################################
# hints(puzzle: object, outty: object) -> None
#
# DESCRIPTION:
#   Prints the hints, including the hints gird, number of words, 2 letter list,
#   etc
# PARAMETERS:
#   puzzle : object
#     - Puzzle object for the currently active game.
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   None
###############################################################################
def hints(game: object, outty: object) -> None:
    gameLetters = formatGameLetts(game)
    hints = hint.hint(game)
    hints.makeHintGrid(game)
    hintHeader = ('Spelling Bee Hint Grid \n\n\n' + 'Center letter is underlined. \n\n ' + f'{gameLetters} \n -\n\n' + 'WORDS: ' + (f'{hints.countWords(game)}, POINTS: ' + str(game.maxScore) + ', PANGRAMS: ' + str(hints.numPangrams(game)) + ' (' + str(hints.numPerfectPangram(game)) + ' Perfect) BINGO: ' + str(game.checkBingo()) + '\n'))
    lst = hints.hint
    letters = getLettersFromGrid(lst)
    hintGrid = formatHintGrid(lst, letters)

    grid = (f'{hintGrid}')

    twoLetterList = ('Two letter list:\n\n'
                     f'{formatTwoLetterList(hints, game)}')

    finalView = hintHeader + '\n\n\n' + grid + '\n' + twoLetterList + '\n\n'
    print(finalView)
    input("Press enter to return to game")


###############################################################################
# formatGameLetts(game:object) -> str
#
# DESCRIPTION:
#   Formats the letters of the Game to be printed
#
# PARAMETERS:
#   puzzle : object
#     - Puzzle object for the currently active game.
# RETURNS:
#   fStr: str
#     - A format string of the game letters
###############################################################################
def formatGameLetts(game: object) -> str:
    fStr = ''
    uniqueLetters = game.getShuffleLetters()

    counter = 0
    for i in uniqueLetters:
        fStr += i.capitalize() + ' '
        counter += 1
    return fStr


###############################################################################
# formatHintGrid(game:object) -> str
#
# DESCRIPTION:
#   Formats the the hints grid of the Game to be printed
# PARAMETERS:
#   puzzle : object
#     - Puzzle object for the currently active game.
#
# RETURNS:
#   fStr: str
#     - A format string of the hint grid
###############################################################################
def formatHintGrid(lst, letters: str) -> str:
    fStr = '     '
    # Remove all columns whos sigma is zero
    removeZeroColumns(lst)

    # Print lengths
    for i in range((len(lst[0]))):
        fStr += f'{lst[0][i]:<4}'

    fStr += '\n\n'
    for i in range(1, 9):
        fStr += f'{letters[i - 1]}:'
        for y in range(len(lst[0])):
            fStr += f' {lst[i][y]:>3}'
        fStr += '\n\n'
    return fStr


###############################################################################
# formatTwoLetterList(hint : object) -> str:
#
# DESCRIPTION:
#   Gets the letters from the list and removes that column
#
# PARAMETERS:
#   lst : object
#     - List representation of the hints grid
#
# RETURNS:
#   letters : str
#     - A string that contains the letters of the puzzle
###############################################################################
def getLettersFromGrid(lst) -> str:
    letters = ''
    for i in range(9):
        letters += str(lst[i][0]).capitalize()
        lst[i].pop(0)
        return letters


###############################################################################
# formatTwoLetterList(hint : object) -> str:
#
# DESCRIPTION:
#   Formats the two letter list for th hints dialog
#
# PARAMETERS:
#   hint : object
#     - A hint object
#
# RETURNS:
#   fStr : str
#     - A string that contains the formated string
###############################################################################
def formatTwoLetterList(hint: object, game) -> str:
    hint.twoLetterList(game)
    lst = hint.getTwoLetterList()
    count = 0
    fStr = ''
    for i in lst:
        letters = str(i[0]).capitalize()
        num = i[1]
        if count > 0:
            prevLetters = str(lst[count - 1][0]).capitalize()
            if letters[0] == prevLetters[0]:
                if count == len(lst) - 1:
                    fStr += f'{letters}: {num}'
                else:
                    fStr += f'{letters}: {num}, '
            else:
                fStr += f'\n{letters}: {num}, '
        else:
            fStr += f'{letters}: {num}, '
        count += 1

    return fStr


###############################################################################
# removeColumn(self, col, lst) -> list[list[int]]:
#
# DESCRIPTION:
#   Removes empty column from the grid
#
# PARAMETERS:
#   self
#      - Gcontroller object
#
#   lst : List[List[int]]
#      - List representation of the hints grid
#
# RETURNS:
#   lst: list[list[int]]
###############################################################################
def removeColumn(col, lst) -> list[list[int]]:
    for i in lst:
        del i[col]
    return lst


###############################################################################
# removeColumn(self, col, lst) -> list[list[int]]:
#
# DESCRIPTION:
#   Removes all columns from the grid whos sumation is Zero
#
# PARAMETERS:
#   self
#     - Gcontroller object
#
#   lst : List[List[int]]
#     -List representaion of the hints grid
#
# RETURNS:
#   None
###############################################################################
def removeZeroColumns(lst):
    count = len(lst[8]) - 1

    for i in reversed(lst[8]):
        if i == 0:
            removeColumn(count, lst)
        count += -1
    return lst
