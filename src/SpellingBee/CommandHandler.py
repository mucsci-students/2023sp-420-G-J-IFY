#import MakePuzzle
#import StateStorage
import CLI
import saveState
import MakePuzzle


# params:
#   - input: string, user input. Check if input matches anythin in commands list
#   - game: object, the currently active game
def parse(input, game):
    match input:
        case ['!new']:
            return newPuzzle()
        case ['!puzzle']:
            return printPuzzle()
        case ['!found-words']:
            return printWords()
        case ['!status']:
            return showStatus()
        case ['!shuffle']:
            game.shuffle()
        case ['!save']:
            return saveGame()
        case ['!savePuzzle']:
            return savePuzzle()
        case ['!load']:
            return loadGame()
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
        case _:
            print('Implentation Pending')


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
def saveGame():
    print('Implementation Pending')

# save puzzle (unique letters and words) only
def savePuzzle():
    print('Implementation Pending')

def loadGame():
    print("Implementation Pending")

def exit():
    print("Thank you for playing!")
    quit()