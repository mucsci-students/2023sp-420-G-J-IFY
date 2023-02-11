import CLI
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
            return loadGame()
        case '!save-list':
            print ('Implementation Pending...')
        case '!help':
            return help(game)
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


def newPuzzle():
    print('Please enter a base word with exactly 7 unique characters. \n' +
    'For auto-generated base word, press enter.')
    word = input('> ')
    out = MakePuzzle.newPuzzle(word.lower())
    out.shuffleChars()
    return(out)

# params:
#   - game: object, the currently active game
def printPuzzle(game):
    CLI.drawTextBox([CLI.drawPuzzle(game.showShuffleLetters().upper())], 
                    40, '^')

def printWords(game):
    CLI.drawTextBox(
        ['Discovered Words: \ {wrds}'.format(wrds = game.showFoundWords())], 
        40, '^')

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
    fileName = input('Please enter the name of the game you are looking for.'
                     '\n> ')
    return StateStorage.loadPuzzle(fileName)

def help(game):
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
                '!load: \ '
                'Load a previously saved game \ '
                '!help: \ '
                'Show the list of all available commands with a brief '
                "description. (You're here now!) \ "
                '!exit: \ '
                'Exit the game ')
    
    CLI.drawTextBox([descHead, descBody], 40, '<')
    CLI.drawTextBox([commHead, commBody], 40, '<')

    return game

def exit(game):
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

# Params: game - the game object
#       : num -  an integer value to determin if we are saving all the game 
#                progress or just the puzzle 0 for saveCurrent() and 1 for 
#                savePuzzle
# saves the games state and handles input from the user to determine if they 
# want to overwirte a file or not
def handleSave(game, num):
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

def finalGame(finishedPuzzle):
    showStatus(finishedPuzzle)
    print("Congratulations!!!!\nYou have found all of the\nwords for this puzzle!")