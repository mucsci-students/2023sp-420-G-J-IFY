###############################################################################
# GController.py
# AUTHOR: Isaak Weidman, Yah'hymbey Baruti Ali-Bey, Francesco Spagnolo
# DATE OF CREATION: 2/25/2023
#
# DESCRIPTION:
#   Routes functionality from user-input into backend of the project, then
#   updates the display to reflect those changes.
#
# CLASSES:
#   GUIController
#
# FUNCTIONS:
#   connectSignals(keySymbol: str, button)
###############################################################################

import sys
import os
from os import name, system
from os import path
from gview.MainWindow import MainWindow
from model import MakePuzzle, StateStorage, output
import model.hint as hint
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QDialog
from PyQt6.QtWidgets import QVBoxLayout, QPlainTextEdit, QDialogButtonBox

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class GController():
    def __init__(self):

        self.outty = output.Output()
        self.puzzle = MakePuzzle.newPuzzle('', '', self.outty, True)
        self.puzzle.shuffleChars()
        self.window = MainWindow(self.puzzle)
        self.window.show()
        self.connectSignals()

    ###########################################################################
    # connectSignals(keySymbol: str, button)
    #
    # DESCRIPTION:
    #   Connects the buttons to the right actions. Each letter builds a new
    #   expression, while the other buttons are connected to their respective
    #   functionality.
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def connectSignals(self):
        # newPuzzle uses provided params
        self.window.newDialog.btns.accepted.connect(self.newPuzzle)

        self.window.centralWidget.entrBtn.clicked.connect(self.guess)

        self.window.centralWidget.uInput.returnPressed.connect(self.guess)

        self.window.saveDialog.btns.accepted.connect(self.saveGame)

        self.window.centralWidget.shflBtn.clicked.connect(self.shuffleLetters)

        self.window.centralWidget.delBtn.clicked.connect(self.deleteInput)

        self.window.loadAction.triggered.connect(self.loadGame)

        self.window.hintAction.triggered.connect(self.hint)

    ###########################################################################
    # newPuzzle(userInput) -> object:
    #
    # DESCRIPTION:
    #   Prompts for input and directs functionality to create a new puzzle
    #   object.
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def newPuzzle(self) -> None:
        dlg = self.window.newDialog
        baseWord = str(dlg.baseWrd.text()).lower()
        keyLetter = str(dlg.keyLett.currentText()).lower()

        if len(set(baseWord)) == 7 or (baseWord == '' and keyLetter == ''):
            retPuzzle = MakePuzzle.newPuzzle
            (baseWord, keyLetter, self.outty, True)
            if retPuzzle is None:
                pass
            else:
                self.puzzle = retPuzzle
                self.puzzle.shuffleChars()
                self.window.newGame(self.puzzle)
        else:
            pass
        dlg.baseWrd.clear()
        dlg.accept()

    ###########################################################################
    # guess(window: object) -> None
    #
    # DESCRIPTION:
    #   Checks the database for valid words, already found words and
    #   words that do not exist
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def guess(self):
        self.window.setStatusTip('')
        # Connect to text field in view and grab
        text = self.window.centralWidget.uInput.text()
        self.window.centralWidget.uInput.clear()
        MakePuzzle.guess(self.puzzle, text, True, self.outty)
        self.window.statsPanel.update(self.puzzle)
        self.window.setStatus(self.outty.getField())

    ###########################################################################
    # saveGame(Game : object) -> None:
    #
    # DESCRIPTION:
    #   Creates a new save entry for the overall status of the game.
    #   creates a new save entry for JUST the puzzle data of the game.
    #
    # PARAMETERS:
    #   game : object
    #     - Puzzle object storing the current game state
    #
    # RETURNS:
    #   None
    ###########################################################################
    def saveGame(self) -> None:
        # Takes file name
        dialog = self.window.saveDialog
        fileName = dialog.fileName.text()
        if len(fileName) < 1:
            badSaveNameDlg = QMessageBox(parent=self.window)
            badSaveNameDlg.setText
            ('Must enter a file name with a length greater than 0.')
            badSaveNameDlg.show()
        else:
            path = str(QFileDialog.getExistingDirectory(self.window,
                                                        "Select Directory"))

            if dialog.justPuzzle.isChecked():
                self.handleSave(self.puzzle, fileName, 1, path)
            else:
                self.handleSave(self.puzzle, fileName, 0, path)

            self.window.setStatus(self.outty.getField())
            dialog.accept()

    ###########################################################################
    # handleSave(game : object, num) -> None:
    #
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
    #
    # RETURNS:
    #   None
    ###########################################################################
    def handleSave(self, game: object,
                   fileName: str, num: int, folder: str) -> None:
        self.window.saveDialog.fileName.clear()
        self.window.saveDialog.justPuzzle.setChecked(False)
        folderPath = folder
        if (path.isfile(folderPath + '/' + fileName + '.json')):
            # Run Dialog Window for overwriting existing file
            # Change if to check if user click yes or no
            self.window.owDialog.show()
            self.window.owDialog.btns.accepted.connect
            (lambda: self.toOverwrite(num, game, fileName, folderPath))

        else:
            if (num == 0):
                StateStorage.saveFromExplorer(folder, fileName, game, False)
            elif (num == 1):
                StateStorage.saveFromExplorer(folder, fileName, game, True)

    ###########################################################################
    # shuffleLetters() -> None
    #
    # DESCRIPTION:
    #   Shuffles the letters in the GUI View
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def shuffleLetters(self) -> None:
        centralWidget = self.window.centralWidget
        self.puzzle.shuffleChars()
        letters = [*self.puzzle.getShuffleLetters().upper()]
        centralWidget.setLetters(letters)
        centralWidget.update()

    ###########################################################################
    # loadGame() -> None:
    #
    # DESCRIPTION:
    #   load an existing save entry into memory
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def loadGame(self) -> None:
        fileName = QFileDialog.getOpenFileName(self.window, 'File')[0]
        # check and make sure game is loading a .json file
        if not fileName.endswith('.json'):
            newPuzzle = None
        else:
            newPuzzle = StateStorage.loadFromExploer(fileName, self.outty)
        if newPuzzle is None:
            self.window.loadFailed.show()
        else:
            self.puzzle = newPuzzle
            self.window.newGame(self.puzzle)

    ###########################################################################
    # deleteInput() -> None:
    #
    # DESCRIPTION:
    #   Deletes char from input field
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def deleteInput(self):
        self.window.centralWidget.uInput.backspace()

    ###########################################################################
    # toOverwrite() -> None:
    #
    # DESCRIPTION:
    #   Completes save overwrite
    #
    # PARAMETERS:
    #   None
    #
    # RETURNS:
    #   None
    ###########################################################################
    def toOverwrite(self, num, game, fileName, folder):
        if (num == 0):
            StateStorage.saveFromExplorer(folder, fileName, game, False)
        elif (num == 1):
            StateStorage.saveFromExplorer(folder, fileName, game, True)
        self.window.owDialog.accept()

    ###########################################################################
    # hint(self) -> None:
    #
    # DESCRIPTION:
    #   Displays a dialog window of the hints grid
    #
    # PARAMETERS:
    #   self
    #     - Gcontroller object
    #
    # RETURNS:
    #   None
    ###########################################################################
    def hint(self) -> None:
        # dialog window
        dlg = QDialog(parent=self.window)
        mDlg = QPlainTextEdit(dlg)
        mDlg.setBackgroundVisible(False)
        layout = QVBoxLayout()
        layout.addWidget(mDlg)
        dlg.setLayout(layout)
        mDlg.setReadOnly(True)
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(button)
        # hint object
        obj = hint.hint(self.puzzle)
        obj.makeHintGrid(self.puzzle)
        button.accepted.connect(dlg.accept)
        font = QFont('Courier', 11)
        self.clear()
        # List representation of the hint grid
        lst = obj.hint
        dlg.setGeometry(700, 300, 600, 600)

        # Format String containing the Grid
        fStr = self.buildHintGrid(lst, obj)

        mDlg.setPlainText(fStr)

        dlg.setFont(font)
        dlg.show()
        self.clear()

    ###########################################################################
    # formatHintsHeader(self) -> str:
    #
    # DESCRIPTION:
    #   Formats the hint grids header
    #
    # PARAMETERS:
    #   self
    #     - Gcontroller object
    #
    # RETURNS:
    #   fStr : str
    #     - Format String that contains the hint grid header
    ###########################################################################
    def formatHintsHeader(self, hint) -> str:
        fStr = 'Spelling Bee Grid \n\n\n'
        fStr += 'Center Letter is Underlined.\n\n'
        letters = self.puzzle.getShuffleLetters()

        counter = 0
        for i in letters:
            fStr += str(i).capitalize() + ' '
            counter += 1
        fStr += '\n-\n\n'
        fStr += ('WORDS: ' + str(hint.countWords(self.puzzle)) + ', POINTS: ')
        fStr += (str(self.puzzle.maxScore) + ', PANGRAMS: ')
        fStr += (str(hint.numPangrams(self.puzzle)) + ' (')
        fStr += (str(hint.numPerfectPangram(self.puzzle)))
        fStr += (' Perfect), BINGO: ')
        fStr += (str(self.puzzle.checkBingo()) + '\n\n\n')

        return fStr

    ###########################################################################
    # removeColumn(self, col, lst) -> list[list[int]]:
    #
    # DESCRIPTION:
    #   removes empty column from the grid
    #
    # PARAMETERS:
    #   self
    #     - Gcontroller object
    #   lst
    #     - The hint grid to remove a column from
    #
    # RETURNS:
    #   lst : list[list[int]]
    ###########################################################################
    def removeColumn(self, col, lst) -> list[list[int]]:
        for i in lst:
            del i[col]
        return lst

    ###########################################################################
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
    #     - List representaion of the hints grid
    #
    # RETURNS:
    #   None
    ###########################################################################
    def removeZeroColumns(self, lst):
        count = len(lst[8]) - 1

        for i in reversed(lst[8]):
            if i == 0:
                self.removeColumn(count, lst)
            count += -1
        return lst

    ###########################################################################
    # buildHintGrid(self,lst : hint):
    #
    # DESCRIPTION:
    #   Builds the Hints grid
    #
    # PARAMETERS:
    #   self
    #      - Gcontroller object
    #
    #   lst: List[List[int]]
    #      - List representation of the hint grid
    #
    # RETURNS:
    #   fStr: str
    #      - Format string containing the complete hint grid
    ###########################################################################
    def buildHintGrid(self, lst, hint) -> str:
        # Build hint grid
        fStr = ''
        letters = ''
        fStr += self.formatHintsHeader(hint)
        # Builds a string of the unique letters from the 2d list
        letters = self.getLettersFromGrid(lst)

        fStr += '    '

        fStr += self.formatHintsGrid(lst, letters)

        # Print the body of the grid
        fStr += "\nTwo Letter List:\n\n"
        fStr += self.formatTwoLetterList(hint)
        return fStr

    ###########################################################################
    # getLettersFromGrid(lst) -> str:
    #
    # DESCRIPTION:
    #   Gets the letters from the 2d list and removes them the returns the
    #   letters
    #
    # PARAMETERS:
    #   lst : list[list[str]]
    #
    # RETURNS:
    #   letters : str
    #       Letters of the puzzle
    ###########################################################################
    def getLettersFromGrid(self, lst) -> str:
        letters = ''
        for i in range(9):
            letters += str(lst[i][0]).capitalize()
            lst[i].pop(0)
        return letters

    def formatHintsGrid(self, lst, letters) -> str:
        fStr = ' '
        self.removeZeroColumns(lst)
        for i in range((len(lst[0]))):
            fStr += f'{lst[0][i]:<4}'
        fStr += '\n\n'
        for i in range(1, 9):
            fStr += f'{letters[i - 1]}:'
            for y in range(len(lst[0])):
                fStr += f' {lst[i][y]:>3}'
            fStr += '\n\n'
        return fStr

    ###########################################################################
    # formatTwoLetterList(hint : object) -> str:
    #
    # DESCRIPTION:
    #   Formats the two letter list for th hints dialog
    #
    # PARAMETERS:
    #   hint : object
    #      - A hint object
    #
    # RETURNS:
    #   fStr : str
    #      - A string that contains the formated string
    ###########################################################################
    def formatTwoLetterList(self, hint: object) -> str:
        hint.twoLetterList(self.puzzle)
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

    def clear(self):
        # For windows
        if name == 'nt':
            _ = system('cls')
        # For mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')


def main():
    app = QApplication([])
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
