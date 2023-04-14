###############################################################################
# GUIAdapter.py
# Author: Isaak Weidman
# Date of Creation: 04/02/2023
#
# DESCRIPTION:
#   Connects GUI to commands that implement functionality from model
#
# CLASSES:
#   GUI_A
###############################################################################

import sys
import os
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFileDialog,
    QApplication,
    QDialog,
    QPlainTextEdit,
    QVBoxLayout,
    QDialogButtonBox,
)
from model.output import Output
from model.hint import hint
from model.puzzle import Puzzle
from gview.MainWindow import MainWindow
from controller import cmd

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Create output
outty = Output()


###############################################################################
# Class GUI_A()
#
# DESCRIPTION:
#   Connects GUI to commands that implement functionality from model
#
# ARGUMENTS:
#   puzzle: Puzzle
#     - the puzzle object that represents active game
#
#   outty: Output
#     - the object that holds output for user
#
# ATTRIBUTES:
#   - _puzzle: Puzzle
#       - The puzzle object that represents the active game
#   - _outty: Output
#       - the object that holds output for user
#   - _window: MainWindow
#       - The main window in which the ui is displayed
#
# FUNCTIONS:
#   - start() -> None
#   - _connectSignals() -> None
#   - _guess() -> None
#   - _shuffle() -> None
#   - _delete() -> None
#   - _newPuzzle() -> None
#   - _save() -> None
#   - _overwrite() -> None
#   - _load() -> None
#   - _hint() -> None
#   - formatHintsHeader(hint: hint) -> str
#   - removeColumn(col: int, lst: list[list[int]]) -> list[list[int]]
#   - removeZeroColumn(lst: list[list[int]]) -> list[list[int]]
#   - buildHintGrid(self, lst: list[list[int]], hint: hint) -> str
#   - getLettersFromGrid(self, lst: list[list[int]]) -> str:
#   - formatHintsGrid(self, lst, letters) -> str:
#   - getLettersFromGrid(self, lst: list[list[int]]) -> str:
###############################################################################
class GUI_A():
    def __init__(self, puzzle: Puzzle):
        self._puzzle = puzzle
        self._puzzle.shuffleChars()
        self._window = None

    ###########################################################################
    # start() -> None
    #
    # DESCRIPTION:
    #   creates application and begins main loop
    ###########################################################################
    def start(self):
        app = QApplication([])
        self._window = MainWindow(self._puzzle)
        self._connectSignals()
        self._window.show()
        sys.exit(app.exec())

    ###########################################################################
    # _connectSignals(self) -> None
    #
    # DESCRIPTION:
    #   connects applicable buttons to backend-reliant functionality
    ###########################################################################
    def _connectSignals(self):
        # Welcome Buttons
        self._window.landingPage.new_btn.clicked.connect(self._newPuzzle)
        self._window.landingPage.load_btn.clicked.connect(self._load)
        self._window.landingPage.exit_btn.clicked.connect(sys.exit)
        # Gameplay Buttons
        self._window.gameWidget.entrBtn.clicked.connect(self._guess)
        self._window.gameWidget.uInput.returnPressed.connect(self._guess)
        self._window.gameWidget.shflBtn.clicked.connect(self._shuffle)
        self._window.gameWidget.delBtn.clicked.connect(self._delete)
        self._window.gameWidget.hintBtn.clicked.connect(self._hint)
        # Game State Buttons
        self._window.newDialog.btns.accepted.connect(self._newPuzzle)
        self._window.saveDialog.btns.accepted.connect(self._save)
        self._window.saveDialog.btns.rejected.connect(self._backToMainWindow)
        self._window.loadAction.triggered.connect(self._load)
        self._window.hintAction.triggered.connect(self._hint)

    ###########################################################################
    # _guess() -> None
    #
    # DESCRIPTION:
    #   Checks the database for valid words, already found words,
    #   and words that do not exist for currently active puzzle.
    ###########################################################################
    def _guess(self) -> None:
        # Clear the status tip
        self._window.setStatus('')
        # retrieve text and make guess
        txt = self._window.gameWidget.uInput.text()
        # create and execute guess command
        guess = cmd.Guess(self._puzzle, txt, outty)
        guess.execute()
        # Update view
        self._window.gameWidget.uInput.clear()
        self._window.statsPanel.update(self._puzzle)
        # Display info
        self._window.setStatus(outty.getField())

    ###########################################################################
    # _shuffle() -> None
    #
    # DESCRIPTION:
    #   Shuffles the order of the letters for a fresh perspective
    ###########################################################################
    def _shuffle(self) -> None:
        shuffle = cmd.Shuffle(self._puzzle)
        shuffle.execute()
        # Update view
        self._window.gameWidget.setLetters(
            [*self._puzzle.getShuffleLetters().upper()]
        )
        self._window.gameWidget.update()

    ###########################################################################
    # _delete() -> None
    #
    # DESCRIPTION:
    #   Mimics the action of pressing backspace
    ###########################################################################
    def _delete(self) -> None:
        self._window.gameWidget.uInput.backspace()

    ###########################################################################
    # _newPuzzle() -> None
    #
    # DESCRIPTION:
    #   Prompts for input and directs functionality to create a new puzzle
    #   object.
    ###########################################################################
    def _newPuzzle(self) -> None:
        dlg = self._window.newDialog  # Quick reference to newDialog object
        # Extract user input
        baseWord = str(dlg.baseWrd.text()).lower()
        keyLetter = str(dlg.keyLett.currentText()).lower()

        # Create new game object so long as it is valid
        if len(set(baseWord)) == 7 or (baseWord == '' and keyLetter == ''):
            newGame = cmd.NewGame(outty, baseWord, keyLetter)
            self._puzzle = newGame.execute()
            # Update view
            self._window.newGame(self._puzzle)
            dlg.baseWrd.clear()
            dlg.accept()
            self._window.stack.setCurrentIndex(1)
        else:
            dlg.setMessage('Invalid base word')

    ###########################################################################
    # _save() -> None
    #
    # DESCRIPTION:
    #   Opens a save dialog and prompts user for required information
    #   (deprecated?)
    ###########################################################################
    def _save(self) -> None:
        # Open file dialog for user to choose location
        dialog = self._window.saveDialog
        saveGame = cmd.SaveGame(
            puzzle=self._puzzle,
            path=dialog.getPath(),
            onlyPuzz=dialog.isOnlyPuzzle(),
            encrypt=dialog.isEncrypted()
        )
        saveGame.execute()
        dialog.reset()
        dialog.accept()
        self._window.stack.setCurrentIndex(0)

    ###########################################################################
    # _load() -> None
    #
    # DESCRIPTION:
    #   Opens a file dialog and returns path to selected .json file
    # PARAMETERS:
    #
    ###########################################################################
    def _load(self):
        # Open file dialog for user to choose file
        fileName = QFileDialog.getOpenFileName(
            parent=self._window,
            caption='Load a game file',
            directory='../saves',
            filter='GameFiles (*.json)'
        )[0]
        # Create a new puzzle object
        loadGame = cmd.LoadGame(fileName, '', outty)
        newPuzzle = loadGame.execute()
        # Checks if puzzle was loaded properly
        if newPuzzle is None:
            self._window.loadFailed.show()
        else:
            # Update puzzle object
            self._puzzle = newPuzzle
            # Update view
            self._window.newGame(self._puzzle)

    ###########################################################################
    # _hint() -> None
    #
    # DESCRIPTION:
    #   builds a dialog to show hint information
    ###########################################################################
    def _hint(self) -> None:
        # Create and build dialog
        dlg = QDialog(parent=self._window)
        mDlg = QPlainTextEdit(dlg)
        mDlg.setBackgroundVisible(False)
        layout = QVBoxLayout()
        layout.addWidget(mDlg)
        dlg.setLayout(layout)
        mDlg.setReadOnly(True)
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(button)

        obj = hint(self._puzzle)
        obj.makeHintGrid(self._puzzle)
        button.accepted.connect(dlg.accept)
        font = QFont('Courier', 11)

        # list representation of the hint grid
        lst = obj.hint
        dlg.setGeometry(700, 300, 600, 600)

        # format String containing the Grid
        fStr = self.buildHintGrid(lst, obj)

        mDlg.setPlainText(fStr)
        dlg.setFont(font)
        dlg.show()

    ###########################################################################
    # formatHintsHeader(self) -> str:
    #
    # DESCRIPTION:
    #   formats the hint grids header
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #
    # RETURNS:
    #   fStr : str
    #       format String that contains the hint grid header
    #
    ###########################################################################
    def formatHintsHeader(self, hint) -> str:
        fStr = 'Spelling Bee Grid \n\n\n'
        fStr += 'Center Letter is Underlined.\n\n'
        letters = self._puzzle.getShuffleLetters()

        counter = 0
        for i in letters:
            fStr += str(i).upper() + ' '
            counter += 1
        fStr += '\n-\n\n'
        fStr += 'WORDS: ' + str(hint.countWords(self._puzzle))
        fStr += ', POINTS: ' + str(self._puzzle.maxScore) + ', PANGRAMS: '
        fStr += str(hint.numPangrams(self._puzzle)) + ' ('
        fStr += str(hint.numPerfectPangram(self._puzzle))
        fStr += ' Perfect), BINGO: '
        fStr += str(self._puzzle.checkBingo()) + '\n\n\n'

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
    #
    ###########################################################################
    def removeColumn(self, col: int, lst: list[list[int]]) -> list[list[int]]:
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
    def removeZeroColumns(self, lst: list[list[int]]) -> list[list[int]]:
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
    #   builds the Hints grid
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #
    #   lst: List[List[int]]
    #       list representation of the hint grid
    #
    # RETURN:
    #   fStr: str
    #       format string containing the complete hint grid
    ###########################################################################
    def buildHintGrid(self, lst: list[list[int]], hint: hint) -> str:
        # build hint grid
        fStr = ''
        letters = ''
        fStr += self.formatHintsHeader(hint)
        # builds a string of the unique letters from the 2d list
        letters = self.getLettersFromGrid(lst)

        fStr += '    '

        fStr += self.formatHintsGrid(lst, letters)
        # print the body of the grid
        fStr += "\nTwo Letter List:\n\n"
        fStr += self.formatTwoLetterList(hint)
        return fStr

    ###########################################################################
    # getLettersFromGrid(lst) -> str:
    #
    # DESCRIPTION:
    #   Gets the letters from the 2d list and removes them the
    # returns the letters
    #
    # PARAMETERS:
    #   lst : list[list[str]]
    #
    # RETURN:
    #   letters : str
    #       letters of the puzzle
    ###########################################################################
    def getLettersFromGrid(self, lst: list[list[int]]) -> str:
        letters = ''
        for i in range(9):
            letters += str(lst[i][0]).capitalize()
            lst[i].pop(0)
        return letters

    ###########################################################################
    # getLettersFromGrid(self, lst) -> str:
    #
    # DESCRIPTION:
    #   formats the hints grid
    #
    # PARAMETERS:
    #   lst : list[list[int]]
    #       list representation of the hints gri
    #   letters : str
    #       letters of the puzzle
    # RETURN:
    #   fStr : str
    #       letters of the puzzle
    ###########################################################################
    def formatHintsGrid(self, lst, letters) -> str:
        fStr = ' '

        self.removeZeroColumns(lst)
        # print lengths

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
    def formatTwoLetterList(self, hint: object) -> str:
        hint.twoLetterList(self._puzzle)
        lst = hint.getTwoLetterList()
        count = 0
        fStr = ''
        for i in lst:
            letters = str(i[0]).upper()
            num = i[1]
            if count >= 0:
                prevLetters = str(lst[count - 1][0]).upper()
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

    ##########################################################################
    # _backToMainWindow():
    #
    # DESCRITPION:
    #   Closes options menu and returns to main menu
    ##########################################################################
    def _backToMainWindow(self):
        self._window.options.close()
        self._window.stack.setCurrentIndex(0)
