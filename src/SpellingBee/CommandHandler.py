import MakePuzzle
import StateStorage.py


def checkCommands(input):
    match input:
        case ['!new']:
            newPuzzle()
        case ['!puzzle']:
            printPuzzle()
        case ['!found-words']:
            printWords()
        case ['!status']:
            showStatus()
        case ['!shuffle']:
            shuffle()
        case ['!save']:
            saveGame()
        case ['!load']:
            loadGame()
        case ['!help']:
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
            exit()

def newPuzzle():
    print('Please enter a base word with exactly 7 unique characters. \n For auto-generated base word, press enter.')
    word = input()
    MakePuzzle.newPuzzle(word)

def printPuzzle():
    print("Implementation Pending")

def printWords():
    print("Implementation Pending")

def showStatus():
    print("Implementation Pending")

def shuffle():
    print("Implementation Pending")

def saveGame():
    print("Would you like to save only the generated puzzle?")
    input = input().upper()
    match input:
        case ['Y']:
            print("Saving game (generated puzzle only)...")
            StateStorage.saveGame(dict, filename)
        case ['N']:
            StateStorage.saveGame(dict, filename)

def loadGame():
    print("Implementation Pending")