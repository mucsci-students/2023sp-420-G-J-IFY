################################################################################
# GUIAdapter.py
# Author: Isaak Weidman
# Date of Creation: 04/02/2023
#
# DESCRIPTION:
#
# CLASSES:
#
# FUNCTIONS:
#
################################################################################

import sys
import os
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFileDialog, 
    QMessageBox, 
    QApplication,
    QDialog,
    QPlainTextEdit,
    QVBoxLayout,
    QDialogButtonBox,
    QTextEdit,
)
from model import (
    MakePuzzle,
    StateStorage,
    output
)
from model.hint import hint
from model.puzzle import Puzzle
from gview.MainWindow import MainWindow
from controller import cmd

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

################################################################################
# Class GUI_A()
#
# DESCRIPTION:
#
# ARGUMENTS:
#
# ATTRIBUTES:
#
# FUNCTIONS:
#
################################################################################
class GUI_A():

    def __init__(self, puzzle: Puzzle, outty: output.Output):
        self._puzzle = puzzle
        self._puzzle.shuffleChars()
        self._outty = outty
        self._window = None


    def start(self):
        app = QApplication([])
        self._window = MainWindow(self._puzzle)
        self._connectSignals()
        self._window.show()
        sys.exit(app.exec())

    def _connectSignals(self):

        # Gameplay Buttons
        self._window.centralWidget.entrBtn.clicked.connect(self._guess)
        self._window.centralWidget.uInput.returnPressed.connect(self._guess)
        self._window.centralWidget.shflBtn.clicked.connect(self._shuffle)
        self._window.centralWidget.delBtn.clicked.connect(self._delete)

        # Game State Buttons
        self._window.newDialog.btns.accepted.connect(self._newPuzzle)
        self._window.saveDialog.btns.accepted.connect(self._save)
        self._window.loadAction.triggered.connect(self._load)
        self._window.hintAction.triggered.connect(self._hint)

    ############################################################################
    # _guess() -> None
    #
    # DESCRIPTION:
    #   Checks the database for valid words, already found words, and words that
    #   do not exist for currently active puzzle.
    ############################################################################
    def _guess(self) -> None:
        # Clear the status tip
        self._window.setStatus('')
        # retrieve text and make guess
        txt = self._window.centralWidget.uInput.text()
        # create and execute guess command
        guess = cmd.Guess(self._puzzle, txt, self._outty)
        guess.execute()
        # Update view
        self._window.centralWidget.uInput.clear()
        self._window.statsPanel.update(self._puzzle)
        # Display info
        self._window.setStatus(self._outty.getField())

    ############################################################################
    # _shuffle() -> None
    #
    # DESCRIPTION:
    #   Shuffles the order of the letters for a fresh perspective
    ############################################################################
    def _shuffle(self) -> None:
        shuffle = cmd.Shuffle(self._puzzle)
        shuffle.execute()
        # Update view
        self._window.centralWidget.setLetters(
            [*self._puzzle.getShuffleLetters().upper()]
        )
        self._window.centralWidget.update()

    ############################################################################
    # _delete() -> None
    #
    # DESCRIPTION:
    #   Mimics the action of pressing backspace
    ############################################################################
    def _delete(self) -> None:
        self._window.centralWidget.uInput.backspace()

    ############################################################################
    # _newPuzzle() -> None
    #
    # DESCRIPTION:
    #   Prompts for input and directs functionality to create a new puzzle
    #   object.
    ############################################################################
    def _newPuzzle(self) -> None:
        dlg = self._window.newDialog # Quick reference to newDialog object
        # Extract user input
        baseWord = str(dlg.baseWrd.text()).lower()
        keyLetter = str(dlg.keyLett.currentText()).lower()

        # Create new game object so long as it is valid
        if len(set(baseWord)) == 7 or (baseWord == '' and keyLetter == ''):
            newGame = cmd.NewGame(self._outty, baseWord, keyLetter)
            self._puzzle = newGame.execute()
            # Update view
            self._window.newGame(self._puzzle)
            dlg.baseWrd.clear()
            dlg.accept()
        else:
            dlg.setMessage('Invalid base word')

    ############################################################################
    # <function name>
    #
    # DESCRIPTION:
    #
    # PARAMETERS:
    #
    ############################################################################
    def _save(self):
        # Open file dialog for user to choose location
        dialog = self._window.saveDialog
        fileName = dialog.fileName.text()
        if len(fileName) < 1:
            badSaveNameDlg = QMessageBox(parent=self._window)
            badSaveNameDlg.setText(
                'Must enter a file name with a length greater than 0.'
            )
            badSaveNameDlg.show()
        else:
            path = str(QFileDialog.getExistingDirectory(
                self._window,
                'Select Directory'
            ))

            saveGame = cmd.SaveGame(
                puzzle=self._puzzle,
                fileName=fileName,
                path=path,
                onlyPuzz=self._window.saveDialog.justPuzzle.isChecked()
            )

            if(os.path.isfile(path + '/' + fileName + '.json')):
                self._window.owDialog.show()
                self._window.owDialog.btns.accepted.connect(
                    lambda: self.overwrite(saveGame)
            )
            
            else:
                saveGame.execute()

            self._window.saveDialog.fileName.clear()
            self._window.saveDialog.justPuzzle.setChecked(False)
            
            self._window.setStatus(self._outty.getField())
            dialog.accept()

    def overwrite(self, command):
        command.execute()
        self._window.owDialog.accept()

    ############################################################################
    # <function name>
    #
    # DESCRIPTION:
    #
    # PARAMETERS:
    #
    ############################################################################
    def _load(self):
        # Open file dialog for user to choose file
        fileName = QFileDialog.getOpenFileName(
            parent=self._window,
            caption='Load a game file',
            directory='../saves',
            filter='GameFiles (*.json)'
        )[0]

        if not fileName.endswith('.json'):
            newPuzzle = None
        else:
            loadGame = cmd.LoadGame(fileName, self._outty)
            newPuzzle = loadGame.execute()

        if newPuzzle == None:
            self._window.loadFailed.show()
        else:
            # Update puzzle object
            self._puzzle = newPuzzle
            # Update view
            self._window.newGame(self._puzzle)


    ############################################################################
    # <function name>
    #
    # DESCRIPTION:
    #
    # PARAMETERS:
    #
    ############################################################################
    def _hint(self):
        # dialog window
        dlg = QDialog(parent=self._window)
        display = QTextEdit(dlg)
        #display.setFont(QFont('Courier', 11))
        #display.setBackgroundVisible(False)
        display.setReadOnly(True)
        layout = QVBoxLayout()
        dlg.setLayout(layout)
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button.accepted.connect(dlg.accept)
        layout.addWidget(display)
        layout.addWidget(button)
        # hint object
        hint = cmd.Hint(self._puzzle)
        output = hint.execute()
        display.setMarkdown(self._formatHint(output))
        dlg.show()

    def _formatHint(self, data: dict) -> str:

        out = (
            '## Spelling Bee Hints\n\n\n'
            'Center Letter is underlined.\n\n'
            '{letters}\n\n'
            '---\n\n'
            '* Words: {numWrds}\n'
            '* Points: {numPts}\n'
            '* Total Pangrams: {numPan}\n'
            '* Total Perfect Pangrams: {numPerf}\n'
            '* Bingo: {bingo}\n'
            '---\n\n'
        ).format(
            letters=data['letters'],
            numWrds=data['numWords'],
            numPts=data['points'],
            numPan=data['numPan'],
            numPerf=data['numPerf'],
            bingo=data['bingo']
        )
        return out
    
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
    #
    ################################################################################
    def _removeColumn(self, col, lst) -> list[list[int]]:
        for i in lst:
            del i[col]
        return lst