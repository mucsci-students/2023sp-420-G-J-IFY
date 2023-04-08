#!/usr/bin/env

################################################################################
# MainWindow.py
# Author: Isaak Weidman
# Date of Creation: 02-18-2023
#
# CLASSES:
#   MainWindow()
#
# FUNCTIONS:
#
#
################################################################################

import sys, os, time
filePath = os.path.dirname(__file__)
sys.path.append(filePath)

from model.puzzle import Puzzle
from gview.StatsPanel import StatsPanel
from gview.HexCluster import HexCluster
from gview.WelcomePage import WelcomePage
from gview import Dialogs
from PyQt6.QtGui import (
    QAction,
    QFont,
    QRegularExpressionValidator,
    QFontDatabase,
)
from PyQt6.QtCore import (
    Qt,
    QRegularExpression,
    QEvent,
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QStatusBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpacerItem,
    QStackedWidget,
    QFrame
)

################################################################################
# class MainWindow()
#
# DESCRIPTION:
#   represents the main window of the application, handles overall layout
#
# ARGUMENTS:
#   *args : 
#
#   **kwargs :
#
#
################################################################################
class MainWindow(QMainWindow):
    def __init__(self, puzzle : Puzzle, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.gameWidget = GameWidget(
            self, 
            puzzle.getShuffleLetters().upper(),
            puzzle.getKeyLetter()
        )
        self.statsPanel = StatsPanel(self)
        
        self.stack = QStackedWidget(self)
        self.centralWidget = self._buildGameWidget()
        self.landingPage = WelcomePage(self)
        
        self.newDialog = Dialogs.NewDialog(self)
        self.loadFailed = Dialogs.LoadFailedDialog(self)
        self.saveDialog = Dialogs.SaveDialog(self)
        self.owDialog = Dialogs.SaveOverwriteDialog(self)
        self.helpDialog = Dialogs.HelpDialog(self)
        self.toolBar = self._createToolBar()
        
        self._initUI()
        
    def _initUI(self) -> None:
        
        QFontDatabase.addApplicationFont(
            os.getcwd() + '/fonts/Comfortaa-VariableFont_wght.ttf'
        )
        
        self.setWindowTitle('Spelling Bee')
        self.setMinimumSize(700, 400)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )
        
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
        self.stack.addWidget(self.landingPage)
        self.stack.addWidget(self.centralWidget)
        self.stack.setCurrentIndex(0)
        
        self.setCentralWidget(self.stack)
       
        
    def _buildGameWidget(self) -> QWidget:
        layout = QHBoxLayout()
        layout.addWidget(self.gameWidget)
        layout.addWidget(self.statsPanel)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def newGame(self, puzzle: Puzzle) -> None:

        self.gameWidget.cluster.setLetters(puzzle.getShuffleLetters().upper())
        self.statsPanel.update(puzzle)
        self.gameWidget.newGame(puzzle.getShuffleLetters().upper())
        self.setStatus('')
        self.stack.setCurrentIndex(1)
        self.gameWidget.uInput.setFocus()

    def setStatus(self, text):
        self.gameWidget.uInput.clearFocus()
        self.gameWidget.uInput.setPlaceholderText(text)


    ############################################################################
    # _createToolBar()
    #
    # DESCRIPTION:
    #   creates toolbar buttons and actions
    ############################################################################
    def _createToolBar(self) -> QToolBar:

        # Create static tool bar
        toolBar = QToolBar('Tools', self)
        toolBar.setMovable(False)

        # add buttons to tool bar
        newAction = QAction('New', self)
        saveAction = QAction('Save', self)
        self.loadAction = QAction('Load', self)
        helpAction = QAction('Help', self)
        self.hintAction = QAction('Hint', self)

        newAction.triggered.connect(self.newDialog.show)
        saveAction.triggered.connect(self.saveDialog.show)
        helpAction.triggered.connect(self.helpDialog.show)

        # add actions to tool bar
        toolBar.addAction(newAction)
        toolBar.addAction(saveAction)
        toolBar.addAction(self.loadAction)
        toolBar.addAction(helpAction)
        toolBar.addAction(self.hintAction)

        return toolBar


    ############################################################################
    # _createInfoBar()
    #
    # DESCRIPTION:
    #   creates status bar to the right to display user progress and found words
    ############################################################################
    def _createInfoBar(self) -> QToolBar:

        # create static tool
        infoBar = QToolBar('Stats', self)
        infoBar.setMovable(False)

        self.statsPanel.setParent(infoBar)
        infoBar.addWidget(self.statsPanel)

        return infoBar 



################################################################################
# class GameWidget:
#
# DESCRIPTION:
#   Game widget is the primary user interface. It contains all the controls the
#   user needs to play the game, allowing full control of the game with both
#   mouse input and keyboard input.
#
# ARGUMENTS:
#   parent: QWidget
#     - GameWidget's parent widget, typically QMainWindow object.
#   letters: list[str]
#     - List of 7 key letters
#
# ATTRIBUTES:
#   uInput : QLineEdit
#     - text field where guesses are prepared before enter
#   cluster : HexCluster
#     - cluster of HexButtons that can be clicked to enter key letters
#   delBtn : QPushButton
#     - button used to delete input one character at a time
#   shflBtn : QPushButton
#     - button used to shuffle the layout of cluster
#   entrBtn : QPushButton
#     - button used to submit uInput text as a guess
#   letters : list[str]
#     - List of key letters
################################################################################
class GameWidget(QWidget):
    def __init__(
            self, 
            parent: QWidget, 
            letters: list[str], 
            keyLett: str,
            *args, 
            **kwargs
        ):
        super(GameWidget, self).__init__(parent, *args, **kwargs)

        # Declare primary attributes
        self.uInput = QLineEdit(self)
        self.hLine = QFrame(self)
        self.cluster = HexCluster(self, letters, keyLett)
        self.delBtn = QPushButton('Delete', self)
        self.shflBtn = QPushButton('Shuffle', self)
        self.entrBtn = QPushButton('Enter', self)
        self.letters = letters

        # Append each cluster button's text to user input field when clicked
        for btn in self.cluster.buttons:
            btn.clicked.connect(self._onHexClicked)
        # Connect textEdited signal to defined function that validates input
        self.uInput.textEdited.connect(self._onUInputEdited)

        self._initUI()

    ############################################################################
    # newGame(letters : list[str])
    # 
    # DESCRIPTIONS:
    #   updates all applicable widgets to reflect the state of the new game.
    ############################################################################
    def newGame(self, letters : list[str]) -> None:
        self.letters = letters

        # Create new validator for uInput
        regex = QRegularExpression(
            f"[{'|'.join(self.letters).upper()}|"
            f"{'|'.join(self.letters).lower()}]+"
        )
        # Create and set uInput validator
        self.uInput.clear()
        validator = QRegularExpressionValidator(regex)
        self.uInput.setValidator(validator)

    ############################################################################
    # setLetters (newLetters : list[str])
    #
    # DESCRIPTION:
    #   change the key letters
    ############################################################################
    def setLetters(self, newletters: list[str]) -> None:
        self.letters = newletters
        self.cluster.setLetters(self.letters)


    ############################################################################
    # _initUI
    #  
    # DESCRIPTION:
    #   initialize layout of widgets and set important attributes
    ############################################################################
    def _initUI(self):

        with open("spellingbee/gview/style.css","r") as file:
            self.setStyleSheet(file.read())
        
        # Create layouts and set allignment attributes
        outerLayout = QVBoxLayout()
        outerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clusterLayout = QHBoxLayout()
        btnsLayout = QHBoxLayout()
        btnsLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # create spacer item to keep cluster centered
        spacer = QSpacerItem(
            50,
            0,
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        
        # Set formatting attributes of user input field
        self.uInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uInput.setFrame(False)
        self.uInput.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # regular expression that only allows key letters, upper and lower.
        # ex. [W|A|R|L|O|C|K]+|[w|a|r|l|o|c|k]+
        regex = QRegularExpression(
            f"[{'|'.join(self.letters).upper()}|"
            f"{'|'.join(self.letters).lower()}]+"
        )
        # Create and set uInput validator
        validator = QRegularExpressionValidator(regex)
        self.uInput.setValidator(validator)
        # Set size policies
        self.uInput.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        
        self.hLine.setFrameShape(QFrame.Shape.HLine)
        self.hLine.setStyleSheet('color: rgb(210, 210, 210);')

        self.cluster.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.MinimumExpanding
        )
        
        self.delBtn.setFixedSize(90, 40)
        self.shflBtn.setFixedSize(90, 40)
        self.entrBtn.setFixedSize(90, 40)

        # Populate layouts, moving top to bottom
        outerLayout.addWidget(self.uInput)
        
        outerLayout.addWidget(self.hLine)

        outerLayout.addSpacerItem(spacer)
        
        clusterLayout.addSpacerItem(spacer)
        clusterLayout.addWidget(self.cluster)
        clusterLayout.addSpacerItem(spacer)
        outerLayout.addLayout(clusterLayout)

        outerLayout.addSpacerItem(spacer)

        btnsLayout.addWidget(self.delBtn)
        btnsLayout.addWidget(self.shflBtn)
        btnsLayout.addWidget(self.entrBtn)
        outerLayout.addLayout(btnsLayout)

        self.setLayout(outerLayout)


    ############################################################################
    # _onHexClicked
    # 
    # DESCRIPTION:
    #   Catch signal from cluster and update uInput text field to reflect signal
    ############################################################################
    def _onHexClicked(self):
        sender = self.sender()
        self.uInput.setText(f'{self.uInput.text()}{sender.text}')

    ############################################################################
    # _onUInputEdited(self, txt):
    #  
    # DESCRIPTION:
    #   force input text to uppercase
    ############################################################################
    def _onUInputEdited(self, txt):
        self.uInput.setText(txt.upper())