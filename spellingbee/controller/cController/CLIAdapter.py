################################################################################
# CAdapter.py
# AUTHOR: Yah'hymbey Baruti Ali-BEy
# DATE OF CREATION: - 3/28/2023
# 
# DESCRIPTION:
#   Multi-line descripiton pending
#
# FUNCTIONS:
#   
################################################################################

from controller import cmd
import sys
import os
import puzzle

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

from cview import CLI
from model import MakePuzzle, StateStorage, hint, output
from os import path
  

class CLI_A():
    def __init__(self, puzzle: puzzle.Puzzle, outty: object):
        self.puzzle = puzzle
        self.outty = outty

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
    def parse(self, usrinput : str) -> object:
        match usrinput:
            case '!new':
                self.newPuzzle()
                return self.puzzle
            case '!puzzle':
                self.printPuzzle()
                return self.puzzle
            case '!found-words':
                self.printWords()
                return self.puzzle
            case '!status':
                self.showStatus()
                return self.puzzle
            case '!shuffle':
                self.puzzle.shuffleChars()
                self.outty.setField('Shuffling letters...')
                return self.puzzle
            case '!save':
                self.saveGame()
                return self.puzzle
            case '!savePuzzle':
                self.savePuzzle()
                return self.puzzle
            case '!load':
                self.loadGame()
                return self.puzzle
            case '!save-list':
                self.outty.setField('Implementation Pending...')
            case '!help':
                self.help()
                return self.puzzle
            case '!hint':
                self.hints()
                return self.puzzle
            case '!exit':
                self.exit()
                return self.puzzle
            case _:
                if usrinput.startswith('!'):
                    self.outty.setField('Command not recognized. Type \"!help\" for a list of '
                        'valid commands...')
                    return self.puzzle

                elif not usrinput.isalpha():
                    self.outty.setField('Input not accepted:\n'
                        '\t~Guesses should only contain alphabetical characters.')
                    return self.puzzle
                    
                else:
                    guess = cmd.Guess(self.puzzle, usrinput, self.outty)
                    guess.execute()
                    return self.puzzle


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
    def newPuzzle(self) -> object:
        print('Please enter a base word with exactly 7 unique characters. \n' +
        'For auto-generated base word, press enter.')
        word = input('> ')
        keyLetter = ''
        if word != '':
            keyLetter = input("Enter a letter from your word "
                        "to use as the key letter\n> ")
        out = cmd.NewGame( self.outty, word.lower(), keyLetter.lower())
        self.puzzle = out.execute()
        if self.outty.getField().startswith("ERROR"):
            print(self.outty.getField())
            self.outty.setField('')


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
    def printPuzzle(self) -> None:
        CLI.drawTextBox([CLI.drawPuzzle(self.puzzle.getShuffleLetters().upper())], 
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
    def printWords(self) -> None:
        CLI.drawTextBox(
            ['Discovered Words: \ {wrds}'.format(wrds = self.puzzle.getFoundWords())], 
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
    def showStatus(self) -> None:
        score = self.puzzle.getScore()
        max = self.puzzle.getMaxScore()
        prog = score/max
        bar = self.puzzle.getRank() + ' ' + CLI.drawProgressBar(20, prog)
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
    def saveGame(self) -> None:
        self.handleSave(0)


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
    def savePuzzle(self) -> None:
        self.handleSave(1)


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
    def loadGame(self) -> None:
        fileName = input('Please enter the name of the game you are looking for.'
                        '\n> ')
        os.chdir('./saves')
        currentPath = os.getcwd() + "\\"+ fileName

        newGame =  cmd.LoadGame(currentPath, fileName, self.outty)
        newGame = newGame.executeCLI()
        if newGame != None:
            self.puzzle = newGame


    ################################################################################
    # help() -> None
    #
    # DESCRIPTION:
    #   provides a brief description of game rules and generally how to play as well
    #   as a list of all available commands.
    ################################################################################
    def help(self) -> None:
        f = open('spellingbee/controller/cController/helpOut.txt', 'r')
        fileContents = f.read()
        print (fileContents)
        f.close()
        input("Press enter to return to the game: ")

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
    def hints(self) -> None:
        hints = cmd.Hint(self.puzzle)
        hintsDict = hints.execute()
        hintHeader = ('Spelling Bee Hint Grid \n\n\n'
                    'Center letter is underlined. \n\n '
                    f'{hintsDict["letters"]} \n -\n\n'
                    'WORDS: ' + (f'{hintsDict["numWords"]}, POINTS: ' + str(hintsDict["points"]) + ', PANGRAMS: ' +  str(hintsDict["numPan"]) + 
                    ' ('  + str(hintsDict["numPerf"]) + ' Perfect) BINGO: '+ str(hintsDict["bingo"])+ '\n')
                    )
        lst = hintsDict["matrix"]
        letters = self.getLettersFromGrid(lst)
        hintGrid = self.formatHintGrid(lst, letters)

        grid =(f'{hintGrid}')
        
        twoLetterList = ('Two letter list:\n\n'
                        f'{self.formatTwoLetterList(hintsDict)}')
        
        finalView = hintHeader + '\n\n\n' + grid + '\n' + twoLetterList + '\n\n'
        print(finalView)
        input("Press enter to return to game")
    
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
    def formatHintGrid(self, lst, letters: str) -> str:
        fStr ='     '
        #remove all columns whos sigma is zero
        self.removeZeroColumns(lst)

        #print lengths
        for i in range((len(lst[0]))):
            fStr += f'{lst[0][i]:<4}'

        fStr += '\n\n'
        for i in range(1,9):
            fStr += f'{letters[i-1]}:'
            for y in range(len(lst[0])):
                fStr += f' {lst[i][y]:>3}'
                    
            fStr += '\n\n'
        return fStr 
            

    ################################################################################
    # formatTwoLetterList(hint : object) -> str:
    #
    # DESCRIPTION:
    #   gets the letters from the list and removes that column
    #
    # PARAMETERS:
    #   lst : object
    #       list representation of the hints grid
    #
    # RETURN:
    #   letters : str
    #       A string that contains the letters of the puzzle
        ################################################################################
    def getLettersFromGrid(self, lst) -> str:
        letters = ''
        for i in range(9):
            letters += str(lst[i][0]).upper()
            lst[i].pop(0)
        return letters

    ################################################################################
    # formatTwoLetterList(hint : object) -> str:
    #
    # DESCRIPTION:
    #   formats the two letter list for th hints dialog
    #
    # PARAMETERS:
    #   hint : object
    #       is a hint object
    #
    # RETURN:
    #   fStr : str
    #       A string that contains the formated string
    ################################################################################
    def formatTwoLetterList(self, hint : dict) -> str:
        lst = hint['twoLetLst']
        count = 0
        fStr = ''
        for i in lst:
            letters = str(i[0]).upper()
            num = i[1]
            if count >= 0:
                prevLetters = str(lst[count - 1][0]).capitalize()
                if letters[0] == prevLetters[0]:
                    if count == len(lst) - 1:
                        fStr += f'{letters}: {num}'
                    else:
                        fStr += f'{letters}: {num}  '
                else:
                    fStr += f'\n{letters}: {num}  '
            else:
                fStr += f'{letters}: {num} '
            count += 1

        return fStr

    ################################################################################
    # removeColumn(self, col, lst) -> list[list[int]]:
    #
    # DESCRIPTION:
    #   removes empty column from the grid
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #
    #   lst : List[List[int]]
    #       list representation of the hints grid
    ################################################################################
    def removeColumn(self, col, lst) -> list[list[int]]:
        for i in lst:
            del i[col]
        return lst

    ################################################################################
    # removeColumn(self, col, lst) -> list[list[int]]:
    #
    # DESCRIPTION:
    #   removes all columns from the grid whos sumation is Zero
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #   
    #   lst : List[List[int]]
    #       list representaion of the hints grid
    ################################################################################
    def removeZeroColumns(self, lst):
        count = len(lst[8]) - 1

        for i in reversed(lst[8]) :
            if i == 0:
                self.removeColumn(count, lst)
            count += -1
        return lst
    
    ################################################################################
    # exit() -> None:
    #
    # DESCRIPTION:
    #   prompts user for confirmation, then quits the game.
    ################################################################################
    def exit(self) -> None:
        print('Are you sure? all unsaved progress will be lost. [Y/N]')
        usrinput = input('> ').upper()
        match usrinput:
            case 'Y':
                self.outty.setField("Thank you for playing!")
        
                quit()
            case 'N':
                return
            case _:
                self.outty.setField('Input Invalid')
                self.parse('!exit') # recursively calls until valid input provided.


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
    def handleSave(self, num : int) -> None:
        saveStatus = False
        fileName = input('Please enter the name of the file you would like to save '
                        'for example "Game1"\n> ')
        os.chdir('./saves')
        currentPath = os.getcwd()
        fFileName = fileName + '.json'
        print(currentPath)
        if(path.isfile(fFileName)):
            yesOrNo = input('Would you like to overwrite the file ' + fileName + '?'
                            '\n Enter Y for yes or N for no\n> ')
            if(yesOrNo == 'Y'):
                if(num == 0):
                    save = cmd.SaveGame(self.puzzle, fileName, currentPath, 0)
                    save.executeCLI()
                    saveStatus = True
                elif(num == 1):
                    save = cmd.SaveGame(self.puzzle, fileName, currentPath, 1)
                    save.executeCLI()
                    saveStatus = True
        else: 
            if(num == 0):
                save = cmd.SaveGame(self.puzzle, fileName, currentPath, 0)
                save.executeCLI()
                saveStatus = True
            elif(num == 1):
                save = cmd.SaveGame(self.puzzle, fileName, currentPath, 1)
                save.executeCLI()
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
    def finalGame(self) -> None:
        self.showStatus()
        self.outty.setField("Congratulations!!!! You have found all of the words for this puzzle!")
        
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
    def commandsList(self) -> list:
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
        return commands
