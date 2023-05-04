###############################################################################
# CAdapter.py
# AUTHOR: Yah'hymbey Baruti Ali-BEy
# DATE OF CREATION: - 3/28/2023
#
# DESCRIPTION:
#   Multi-line descripiton pending
#
# FUNCTIONS:
#
###############################################################################

from controller import cmd
import sys
import os
import puzzle
from cview import CLI
from model.output import Output
from os import path, name, system
import highScore
import __main__ as main
current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

outty = Output.getInstance()


class CLI_A():
    def __init__(self, puzzle: puzzle.Puzzle):
        self.puzzle = puzzle

    ###########################################################################
    # parse(userinput : str, game : object, outty : object) -> object:
    #
    # DESCRIPTION:
    #   Directs game functionality based on string input, game object
    #
    # PARAMETERS:
    #   usrinput : str
    #     - string provided by user containing either a guess, a command, or
    #       bad input.
    #   game : object
    #     - puzzle object storing current game state
    #   outty : object
    #     - output object storing output strings
    #
    # RETURN:
    #   object
    #     - updated puzzle object
    ###########################################################################
    def parse(self, usrinput: str) -> object:
        match usrinput:
            case 'newGame':
                self.newPuzzle()
                return self.puzzle
            case 'showFoundWords':
                self.printWords()
                return self.puzzle
            case 'shuffleLetters':
                self.puzzle.shuffleChars()
                outty.setField('Shuffling letters...')
                return self.puzzle
            case 'saveGame':
                self.saveGame()
                return self.puzzle
            case 'saveBlankGame':
                self.savePuzzle()
                return self.puzzle
            case 'loadGame':
                self.loadGame()
                return self.puzzle
            case 'showLeaderboard':
                self.leaderboard()
                input("Press enter to return to game")
                CLI.clear()
                return self.puzzle
            case 'showHelp':
                self.help()
                return self.puzzle
            case 'showHints':
                self.hints()
                return self.puzzle
            case 'quitToDesktop':
                self.exit()
                return None
            case 'endGame':
                self.endQuit()
                return None
            case _:
                if not usrinput.isalpha():
                    outty.setField(
                        'Input not accepted:\n\t~Guesses '
                        'should only contain alphabetical '
                        'characters.'
                    )
                    return self.puzzle
                else:
                    guess = cmd.Guess(self.puzzle, usrinput)
                    guess.execute()
                    if self.puzzle.finishedFlag is True:
                        pass
                    return self.puzzle

    ###########################################################################
    # newPuzzle() -> None:
    #
    # DESCRIPTION:
    #   prompts for input and directs functionality to create a new puzzle
    #   object.
    #
    #  PARAMETERS:
    #   outty : object
    #     - output object storing output strings
    #
    # RETURN:
    #   object
    #     - new puzzle object
    ###########################################################################
    def newPuzzle(self) -> object:
        print('Please enter a base word with exactly 7 unique '
              'characters.\nFor auto-generated base word, press enter.')
        word = input('> ')
        keyLetter = ''
        if word != '':
            keyLetter = input("Enter a letter from your word "
                              "to use as the key letter\n> ")
        out = cmd.NewGame(word.lower(), keyLetter.lower())
        self.puzzle = out.execute()
        if outty.getField().startswith("ERROR"):
            print(outty.getField())
            outty.setField('')

    ###########################################################################
    # printWords(game : object) ->
    #
    # DESCRIPTION:
    #   prints list of discovered words in a neatly formatted text box
    #
    # PARAMETERS:
    #   game : object
    #     - puzzle object storing current game state
    ###########################################################################
    def printWords(self) -> None:
        CLI.drawTextBox(
            ['Discovered Words: \ {wrds}'.format
             (wrds=self.puzzle.concatFound())], 40, '^')

    ###########################################################################
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
    ###########################################################################
    def saveGame(self) -> None:
        self.handleSave(False)

    ###########################################################################
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
    ###########################################################################
    def savePuzzle(self) -> None:
        self.handleSave(1)

    ###########################################################################
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
    ###########################################################################
    def loadGame(self) -> None:
        fileName = input('Please enter the name of the game you are '
                         'looking for.\n> ')
        if not fileName.endswith('.json'):
            fileName += '.json'

        currentPath = os.getcwd() + "/" + fileName

        newGame = cmd.LoadGame(currentPath)
        newGame = newGame.execute()
        if newGame is not None:
            self.puzzle = newGame
        else:
            self.puzzle = None

    ###########################################################################
    # help() -> None
    #
    # DESCRIPTION:
    #   provides a brief description of game rules and generally how to play as
    #   well as a list of all available commands.
    ###########################################################################
    def help(self) -> None:
        f = open('spellingbee/controller/cController/helpOut.txt', 'r')
        fileContents = f.read()
        print(fileContents)
        f.close()
        input("Press enter to return to the game: ")
        CLI.clear()

    ###########################################################################
    # hints(puzzle: object, outty: object) -> None
    #
    # DESCRIPTION:
    #   Prints the hints, including the hints gird, number of words,
    #   2 letter list, etc
    # PARAMETERS:
    #   puzzle : object
    #     - puzzle object for the currently active game.
    #   outty : object
    #     - output object storing output strings
    ###########################################################################
    def hints(self) -> None:
        hints = cmd.Hint(self.puzzle)
        hintsDict = hints.execute()

        hintHeader = 'Spelling Bee Hint Grid \n\n\n'
        hintHeader += 'Center letter is underlined. \n\n '
        hintHeader += f'{hintsDict["letters"]} \n\n\n'
        hintHeader += 'WORDS: ' + f'{hintsDict["numWords"]}, POINTS: '
        hintHeader += str(hintsDict["points"]) + ', PANGRAMS: '
        hintHeader += str(hintsDict["numPan"]) + ' ('
        hintHeader += str(hintsDict["numPerf"]) + ' Perfect) BINGO: '
        hintHeader += str(hintsDict["bingo"]) + '\n'

        lst = hintsDict["matrix"]
        letters = self.getLettersFromGrid(lst)
        hintGrid = self.formatHintGrid(lst, letters)

        grid = (f'{hintGrid}')

        twoLetterList = ('Two letter list:\n\n'
                         f'{self.formatTwoLetterList(hintsDict)}')

        finalView = hintHeader + '\n\n\n' + grid + '\n' + twoLetterList
        finalView += '\n\n'
        print(finalView)
        input("Press enter to return to game")
        CLI.clear()

    ###########################################################################
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
    ###########################################################################
    def formatHintGrid(self, lst, letters: str) -> str:
        fStr = '     '
        # remove all columns whos sigma is zero
        self.removeZeroColumns(lst)

        # print lengths
        for i in range((len(lst[0]))):
            fStr += f'{lst[0][i]:<4}'

        fStr += '\n\n'
        for i in range(1, 9):
            fStr += f'{letters[i-1]}:'
            for y in range(len(lst[0])):
                fStr += f' {lst[i][y]:>3}'

            fStr += '\n\n'
        return fStr

    ###########################################################################
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
    ###########################################################################
    def getLettersFromGrid(self, lst) -> str:
        letters = ''
        for i in range(9):
            letters += str(lst[i][0]).upper()
            lst[i].pop(0)
        return letters

    ###########################################################################
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
    ###########################################################################
    def formatTwoLetterList(self, hint: dict) -> str:
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

    ###########################################################################
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
    ###########################################################################
    def removeColumn(self, col, lst) -> list[list[int]]:
        for i in lst:
            del i[col]
        return lst

    ###########################################################################
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
    ###########################################################################
    def removeZeroColumns(self, lst):
        count = len(lst[8]) - 1

        for i in reversed(lst[8]):
            if i == 0:
                self.removeColumn(count, lst)
            count += -1
        return lst

    ###########################################################################
    # exit() -> None:
    #
    # DESCRIPTION:
    #   prompts user for confirmation, then quits the game.
    ###########################################################################
    def exit(self) -> None:
        print('Are you sure you want to exit? [Y/N]')
        usrinput = input('> ').upper()
        match usrinput:
            case 'Y':
                print("Thank you for playing!")
                quit()
            case 'N':
                return None
            case _:
                print('Input Invalid')
                return None

    ###########################################################################
    # leaderboard(puzzle: object, outty: object) -> None
    #
    # DESCRIPTION:
    #   Prints the  current leaderboard to the user
    #
    # PARAMETERS:
    #   puzzle : object
    #     - puzzle object for the currently active game.
    #   outty : object
    #     - output object storing output strings
    #
    # RETURNS:
    #   None
    ###########################################################################
    def leaderboard(self):
        leaderboard = highScore.getHighScore(self.puzzle.getUniqueLetters(),
                                             self.puzzle.getKeyLetter())
        fstr = 'Leaderboard:\n\n'
        fstr += 'Place   Name       Rank        Score\n'

        count = 0
        for i in leaderboard:
            fstr += (
                f'{count+1:<7} {leaderboard[count][1]:<11}'
                f'{leaderboard[count][2]:<14} {leaderboard[count][3]}\n'
            )
            count += 1

        print(fstr)

    ###########################################################################
    # handleSave(game : object, num : int, outty : object) -> None:
    #                                                 # comment this out better
    # DESCRIPTION:
    #   saves the games state and handles input from the user to determin if
    #   they want to overwrite a file or not
    #
    # PARAMETERS:
    #   game : object
    #     - puzzle object storing current game state
    #   num : int
    #     - an integer value to determin if we are saving all the game progress
    #       or just the pzzle. 0 for saveCurrent() and 1 for savePuzzle().
    #   outty : object
    #     - output object storing output strings
    ###########################################################################
    def handleSave(self, num: bool) -> None:
        saveStatus = False
        fileName = input(('Please enter the name of the file you would like '
                          'to save for example "Game1"\n> '))
        if not fileName.endswith('.json'):
            fileName += '.json'
        filePath = str(os.getcwd()) + '/' + fileName
        encrypt = self.checkEncrypt()

        if (path.isfile(filePath)):
            yesOrNo = input('Would you like to overwrite the file '
                            + fileName + '?' +
                            ' [Y/N]\n> ')
            print(filePath)
            if (yesOrNo == 'Y'):
                save = cmd.SaveGame(self.puzzle, filePath, num, encrypt)
                save.execute()
                saveStatus = True
        else:
            save = cmd.SaveGame(self.puzzle, filePath, num, encrypt)
            save.execute()
            saveStatus = True

        if saveStatus:
            print('Save Complete!')
        else:
            print(f'Game could not be saved. Path: {filePath}')

    ###########################################################################
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
    ###########################################################################
    def finalGame(self) -> None:
        outty.setField((
            "Congratulations!!!! You "
            "have found all of the words for this puzzle!"
        ))

    ###########################################################################
    # checkEncrypt() -> None:
    #
    # DESCRIPTION:
    #   Prompts user for confirmation to encrypt the word list, then
    #   encrypts the list if yes, otherwise nothing is done.
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def checkEncrypt(self) -> bool:
        flag = False
        print('Would you like to encrypt the word list? [Y/N]')
        encryptYorN = input('> ').upper()
        match encryptYorN:
            case 'Y':
                flag = True
                return flag
            case 'N':
                return flag
            case _:
                # Recursively calls until valid input provided.
                self.checkEncrypt()

    ###########################################################################
    # checkHighScore() -> None:
    #
    # DESCRIPTION:
    #   Prompts user to submit their score to the leaderboard if their score
    #   is a top 10 score.
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def checkHighScore(self) -> None:
        # Check if it qualifies first
        leaderboard = highScore.getHighScore(self.puzzle.getUniqueLetters(),
                                             self.puzzle.getKeyLetter())
        # If leaderboard is empty
        if len(leaderboard) == 0:
            pass
        # If there are less than 10 scores
        elif len(leaderboard) < 10:
            pass
        # If the last element is less than the current score
        elif leaderboard[-1][3] < self.puzzle.getScore():
            pass
        else:
            return
        # Then ask if they want to enter
        print('Your score is a top 10 score! Would you like to be on the '
              + 'leaderboard? [Y/N]')
        leaderboardCheck = input('> ').upper()
        if leaderboardCheck.startswith('Y'):
            # Enter score in the database
            name = self.validateName()
            highScore.qualify(name, self.puzzle.getRank(),
                                self.puzzle.getScore(),
                                self.puzzle.getUniqueLetters(),
                                self.puzzle.getKeyLetter())
        else:
            return

    ###########################################################################
    # validateName() -> str:
    #
    # DESCRIPTION:
    #   Helper function to validate name input.
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   Name : str
    #       Returns validated name
    ###########################################################################
    def validateName(self) -> str:
        print()
        name = input("What is the name that you'd like to enter?\n> ")
        if len(name) >= 10:
            print("\nName must be 10 characters\n")
            name = self.validateName()
        elif not name.isalpha():
            print("\nName must not contain non-alphabetical characters\n")
            name = self.validateName()
        print()
        return name

    ###########################################################################
    # saveAndQuit(self) -> None:
    #
    # DESCRIPTION:
    #   asks the user if they want to quit and save their progress. this will
    #   also prompt the user to save their progress if they wish and display
    #   the leaderboard for the current fame and prompt the user if they are
    #   elegible to join the leaderboad
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def endQuit(self) -> None:
        # display leaderboard for current game
        self.checkHighScore()

        # prompt user to join leaderboard if they are elegible to join
        # the leaderboard
        self.leaderboard()

        input ("Press enter to continue...")

        # bring user back to the start page
        self.clear()
        main.main(self.puzzle)

    def clear(self):

        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def endGame(self):
        input('Congratulations you made it to Queen Bee. ' +
              'Press enter to continue.\n')
        print()
        self.saveAndQuit()

    ###########################################################################
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
    ###########################################################################
    def commandsList(self) -> list:
        commands = [
            'newGame',
            'loadGame',
            'saveGame',
            'saveBlankGame',
            'showHelp',
            'showHints',
            'showLeaderboard',
            'showFoundWords',
            'shuffleLetters',
            'quitToDesktop',
            'endGame'
        ]
        return commands
