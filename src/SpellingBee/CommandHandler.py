import CLI
import saveState
import MakePuzzle
import StateStorage
from os import path

# params:
#   - input: string, user input. Check if input matches anythin in commands list
#   - game: object, the currently active game
def parse(usrinput, game):
    match usrinput:
        case '!new':
            return newPuzzle()
        case '!puzzle':
            return printPuzzle(game)
        case '!found-words':
            return printWords(game)
        case '!status':
            return showStatus(game)
        case '!shuffle':
            game.shuffleChars()
        case '!save':
            saveGame(game)
        case '!savePuzzle':
            savePuzzle(game)
        case '!load':
            return loadGame()
        case '!save-list':
            showSaves()
        case '!help':
            print('!new: Generates a new puzzle from a base word with exactly 7 unique characters\n' + 
                '!puzzle: Prints the current puzzle to the screen\n' +
                '!found-words: prints the list of all discovered words\n' +
                '!status: prints the users level for current game (novice, beginner, pro, etc)\n' +
                '!shuffle: shuffles puzzle\n' +
                '!save: save the game\n' +
                '!load: load a previously saved game\n' +
                '!save-list: shows a list of all available game saves\n' +
                '!help: show list of commands with brief description\n' +
                '!exit: exit the game')
            input('press enter to continute')

        case '!exit':
            print('Are you sure? all unsaved progress will be lost. [Y/N]')
            usrinput = input('> ').upper()
            match usrinput:
                case 'Y':
                    exit()
                case 'N':
                    return
                case _:
                    print('Input Invalid')
                    parse('!exit', game) # recursively calls until valid input provided.

        case _:
            if usrinput.startswith('!'):
                print('Command not recognized. Type \"!help\" for a list of valid commands...')
            else:
                MakePuzzle.guess(game, usrinput)


def newPuzzle():
    print('Please enter a base word with exactly 7 unique characters. \n' +
    'For auto-generated base word, press enter.')
    word = input('> ')
    out = MakePuzzle.newPuzzle(word.lower())
    out.shuffleChars()
    return out

# params:
#   - game: object, the currently active game
def printPuzzle(game):
    CLI.drawTextBox([CLI.drawPuzzle(game.showUniqueLetters())], 40, '^')

def printWords(game):
    CLI.drawTextBox(['Discovered Words: \ {wrds}'.format(wrds = game.showFoundWords())], 40, '^')

def showStatus(game):
    score = game.showScore()
    max = game.showMaxScore()
    prog = score/max
    bar = game.showRank() + ' ' + CLI.drawProgressBar(20, prog)
    stats = 'Score: {} \ Progress: {}%'.format(score, int(prog*100))
    CLI.drawTextBox(['Level: \ ' + bar + ' \ ' + stats], 40, '^')

# saves overall game progress
def saveGame(game):
    handleSave(game, 0)

# save puzzle (unique letters and words) only
def savePuzzle(game):
    handleSave(game, 1)

def loadGame():
    fileName = input('Please enter the name of the game you are looking for.\n> ')
    return StateStorage.loadPuzzle(fileName)

def showSaves():
    print("Implementation Pending")

def exit():
    print("Thank you for playing!")
    quit()

# Params: game - the game object
#       : num -  an integer value to determin if we are saving all the game progress or just the puzzle 0 for saveCurrent() and 1 for savePuzzle
# saves the games state and handles input from the user to determine if they want to overwirte a file or not
def handleSave(game, num):
    saveStatus = False
    fileName = input('Please enter the name of the file you would like to save for example "Game1"\n> ')
    if(path.isfile(fileName +'.json')):
        yesOrNo = input('Would you like to overwrite the file ' + fileName + '?' '\n Enter Y for yes or N for no\n> ')
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