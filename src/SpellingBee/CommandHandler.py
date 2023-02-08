import CLI
import saveState
import MakePuzzle
import StateStorage
import os.path 
from os import path

# params:
#   - input: string, user input. Check if input matches anythin in commands list
#   - game: object, the currently active game
def parse(input, game):
    match input:
        case '!new':
            return newPuzzle()
        case '!puzzle':
            return printPuzzle()
        case '!found-words':
            return printWords()
        case '!status':
            return showStatus()
        case '!shuffle':
            game.shuffle()
        case '!save':
            saveGame(game)
        case '!savePuzzle':
            savePuzzle(game)
        case '!load':
            return loadGame()
        case '!help':
            print('!new: Generates a new puzzle from a base word with exactly 7 unique characters','\n',
                '!puzzle: Prints the current puzzle to the screen','\n',
                '!found-words: prints the list of all discovered words','\n',
                '!status: prints the users level for current game (novice, beginner, pro, etc)','\n',
                '!shuffle: shuffles puzzle','\n',
                '!save: save the game','\n',
                '!load: load a previously saved game','\n',
                '!help: show list of commands with brief description','\n',
                '!exit: exit the game')

        case ['!exit']:
            print('Are you sure? all unsaved progress will be lost. [Y/N]')
            input = input().upper()
            match input:
                case 'Y':
                    quit()
                case 'N':
                    return
                case _:
                    print('Input Invalid')
                    parse('!exit', game) # recursively calls until valid input provided.

        case _:
            if input.startswith('!'):
                print('Command not recognized. Type \"!help\" for a list of valid commands...')
            else:
                MakePuzzle.guess(input)


def newPuzzle():
    print('Please enter a base word with exactly 7 unique characters. \n For auto-generated base word, press enter.')
    word = input()
    return MakePuzzle.newPuzzle()

# params:
#   - game: object, the currently active game
def printPuzzle(game):
    CLI.drawTextBox([CLI.drawPuzzle(game.showUniqueLetters())], 40, '^')

def printWords(game):
    CLI.drawTextBox(['Found Words: \ ' + game.showFoundWords()], 40, '^')

def showStatus(game):
    score = game.showScore()
    max = game.showMaxScore()
    prog = score/max
    CLI.drawTextBox(['Level: \ ' + game.showRank() + ' ' + CLI.drawProgressBar(20, prog)], 40, '^')

# saves overall game progress
def saveGame(game):
    handleSave(game, 0)
    print('Implementation Pending')

# save puzzle (unique letters and words) only
def savePuzzle(game):
    handleSave(game, 1)

def loadGame():
    print("Implementation Pending")

def exit():
    print("Thank you for playing!")
    quit()

# Params: game - the game object
#       : num -  an integer value to determin if we are saving all the game progress or just the puzzle 0 for saveCurrent() and 1 for savePuzzle
# saves the games state and handles input from the user to determine if they want to overwirte a file or not
def handleSave(game, num):
    fileName = input('Please enter the name of the file you would like to save for example "Game1": ')
    if(path.isfile(fileName +'.json')):
        yesOrNo = input('Would you like to overwrite the file ' + fileName + '?' '\n Enter Y for yes or N for no: ')
        if(yesOrNo == 'Y'):
            if(num == 0):
                StateStorage.saveCurrent(game, fileName)
            elif(num == 1):
                StateStorage.savePuzzle(game, fileName)
    else: 
        if(num == 0):
            StateStorage.saveCurrent(game, fileName)
        elif(num == 1):
            StateStorage.savePuzzle(game, fileName)
    print('Save Complete')