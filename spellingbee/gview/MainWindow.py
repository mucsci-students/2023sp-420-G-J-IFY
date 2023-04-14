#!/usr/bin/env
###############################################################################
# MainWindow.py
# Author: Isaak Weidman
# Date of Creation: 02-18-2023
#
# CLASSES:
#   MainWindow()
#
#   GameWidget()
###############################################################################

from gview.StatsPanel import StatsPanel
from gview.HexCluster import HexCluster
from gview.WelcomePage import WelcomePage
from gview import Dialogs
from PyQt6.QtGui import (
    QAction,
    QRegularExpressionValidator,
    QFontDatabase,
    QIcon,
)
from PyQt6.QtCore import (
    Qt,
    QRegularExpression,
    QSize
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpacerItem,
    QStackedWidget,
    QFrame,
)
from model.puzzle import Puzzle
import sys
import os
filePath = os.path.dirname(__file__)
sys.path.append(filePath)


###############################################################################
# class MainWindow()
#
# DESCRIPTION:
#   represents the main window of the application, handles overall layout
#
# ARGUMENTS:
#   puzzle: Puzzle
#     - the puzzle object the window is initialized with
###############################################################################
class MainWindow(QMainWindow):
    def __init__(self, puzzle: Puzzle, *args, **kwargs):
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

        self.options = Dialogs.OptionsDialog(self)
        self.newDialog = Dialogs.NewDialog(self)
        self.loadFailed = Dialogs.LoadFailedDialog(self)
        self.saveDialog = Dialogs.SaveDialog(self)
        self.owDialog = Dialogs.SaveOverwriteDialog(self)
        self.helpDialog = Dialogs.HelpDialog(self)
        self.toolBar = self._createToolBar()

        self._initUI()

    ###########################################################################
    # _initUI(self) -> None:
    #
    # DESCRIPTION:
    #   Initializes the ui to its default state
    ###########################################################################
    def _initUI(self) -> None:
        # Add custom font to database
        QFontDatabase.addApplicationFont(
            os.getcwd() + '/fonts/Comfortaa-VariableFont_wght.ttf'
        )
        # Set basic window geometry
        self.setWindowTitle('Spelling Bee')
        self.setMinimumSize(800, 500)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )
        # Add toolbar to the top of window
        # self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        # Add pages to the stack, showing landingPage initially
        self.stack.addWidget(self.landingPage)
        self.stack.addWidget(self.centralWidget)
        self.stack.setCurrentIndex(0)
        self.setCentralWidget(self.stack)
        # Connect basic signals
        self.gameWidget.menuBtn.clicked.connect(self.options.show)
        self.options.mainMenuBtn.clicked.connect(self.saveDialog.show)
        self.options.helpBtn.clicked.connect(self.helpDialog.show)
        self.options.shareBtn.clicked.connect(self._share)

    ###########################################################################
    # _buildGameWidget() -> QWidget
    #
    # DESCRIPTION:
    #   Builds and returns the main game widget with the gameplay controls
    #   on the left and status information on the right
    ###########################################################################
    def _buildGameWidget(self) -> QWidget:
        layout = QHBoxLayout()
        layout.addWidget(self.gameWidget)
        layout.addWidget(self.statsPanel)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    ###########################################################################
    # _newGame() -> None:
    #
    # DESCRIPTION:
    #   Updates the userinterface when a new puzzle is chosen.
    ###########################################################################
    def newGame(self, puzzle: Puzzle) -> None:
        self.gameWidget.cluster.setLetters(puzzle.getShuffleLetters().upper())
        self.statsPanel.update(puzzle)
        self.gameWidget.newGame(puzzle.getShuffleLetters().upper())
        self.setStatus('')
        self.stack.setCurrentIndex(1)
        self.gameWidget.uInput.setFocus()

    ###########################################################################
    # setStatus(self, text: str) -> None:
    #
    # DESCRIPTION:
    #   Displays text to the user when they make a guess
    ###########################################################################
    def setStatus(self, text: str) -> None:
        self.gameWidget.uInput.clearFocus()
        self.gameWidget.uInput.setPlaceholderText(text)

    ###########################################################################
    # _createToolBar() -> QToolBar:
    #
    # DESCRIPTION:
    #   creates toolbar buttons and actions
    ###########################################################################
    def _createToolBar(self) -> QToolBar:
        # Create static tool bar
        toolBar = QToolBar('Tools')
        toolBar.setMovable(False)
        toolBar.setBaseSize(100, 100)
        toolBar.setStyleSheet(
            '''
            border: none;
            background-color: rgb(200, 200, 200);
            '''
        )

        # add buttons to tool bar
        menuAction = QAction('Menu', self)
        newAction = QAction('New', self)
        saveAction = QAction('Save', self)
        self.loadAction = QAction('Load', self)
        helpAction = QAction('Help', self)
        self.hintAction = QAction('Hint', self)

        # Add style
        menuAction.setIcon(QIcon('SpellingBee/gview/assets/menu.png'))

        # Make connections to simple actions
        newAction.triggered.connect(self.newDialog.show)
        saveAction.triggered.connect(self.saveDialog.show)
        helpAction.triggered.connect(self.helpDialog.show)
        self.landingPage.custom_btn.clicked.connect(self.newDialog.show)

        # add actions to tool bar
        toolBar.addAction(menuAction)
        toolBar.addAction(newAction)
        toolBar.addAction(saveAction)
        toolBar.addAction(self.loadAction)
        toolBar.addAction(helpAction)
        toolBar.addAction(self.hintAction)

        return toolBar

    ##########################################################################
    # _createInfoBar()
    #
    # DESCRIPTION:
    #   creates status bar to the right to display user progress and found
    #   words
    ##########################################################################
    def _createInfoBar(self) -> QToolBar:
        # create static tool
        infoBar = QToolBar('Stats', self)
        infoBar.setMovable(False)
        self.statsPanel.setParent(infoBar)
        infoBar.addWidget(self.statsPanel)
        return infoBar

    ##########################################################################
    # _returnToMenu() -> None
    #
    # DESCRIPTION:
    #   Begins wrap up sequence
    ##########################################################################
    def _returnToMenu(self) -> None:
        self.stack.setCurrentIndex(0)
        self.options.close()

    ##########################################################################
    # _share() -> None:
    #
    # DESCRIPTION:
    #   Opens the share dialog with proper pixmaps
    ##########################################################################
    def _share(self) -> None:
        # Get pixmaps
        stats_pix = self.statsPanel.statsWidget.grab()
        hex_pix = self.gameWidget.cluster.grab()

        # Create dialog
        share_dlg = Dialogs.ShareDialog(self, stats_pix, hex_pix)
        share_dlg.show()


###############################################################################
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
###############################################################################
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
        self.menuBtn = QPushButton(self)
        self.hintBtn = QPushButton(self)
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

    ###########################################################################
    # newGame(letters : list[str])
    #
    # DESCRIPTIONS:
    #   updates all applicable widgets to reflect the state of the new game.
    ###########################################################################
    def newGame(self, letters: list[str]) -> None:
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

    ###########################################################################
    # setLetters (newLetters : list[str])
    #
    # DESCRIPTION:
    #   change the key letters
    ###########################################################################
    def setLetters(self, newletters: list[str]) -> None:
        self.letters = newletters
        self.cluster.setLetters(self.letters)

    ###########################################################################
    # _initUI
    #
    # DESCRIPTION:
    #   initialize layout of widgets and set important attributes
    ###########################################################################
    def _initUI(self):
        # Set style sheet
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())

        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )

        # Create layouts and set allignment attributes
        toolsLayout = QHBoxLayout()
        outerLayout = QVBoxLayout()
        outerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outerLayout.setContentsMargins(0, 0, 0, 0)
        clusterLayout = QHBoxLayout()
        btnsLayout = QHBoxLayout()
        btnsLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # create spacer item to keep cluster centered
        spacer = QSpacerItem(
            0,
            0,
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )

        # Fromat tool buttons
        self.menuBtn.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.menuBtn.setStatusTip('Menu')
        self.menuBtn.setIcon(QIcon('SpellingBee/gview/assets/menu.png'))
        self.menuBtn.setIconSize(QSize(30, 30))
        self.hintBtn.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.hintBtn.setStatusTip('Hint')
        self.hintBtn.setIcon(QIcon('SpellingBee/gview/assets/hint.png'))
        self.hintBtn.setIconSize(QSize(30, 30))
        self.hintBtn.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
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
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.Minimum
        )

        self.hLine.setFrameShape(QFrame.Shape.HLine)
        self.hLine.setStyleSheet('color: rgb(210, 210, 210);')
        self.hLine.setFixedHeight(3)
        self.hLine.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.MinimumExpanding
        )

        self.cluster.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )

        self.delBtn.setFixedSize(90, 40)
        self.shflBtn.setFixedSize(90, 40)
        self.entrBtn.setFixedSize(90, 40)

        # Populate layouts, moving top to bottom
        toolsLayout.addWidget(
            self.menuBtn,
            alignment=Qt.AlignmentFlag.AlignLeft
        )
        toolsLayout.addWidget(
            self.hintBtn,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        # outerLayout.addLayout(toolsLayout)
        outerLayout.addWidget(self.uInput)
        outerLayout.addWidget(self.hLine)
        # outerLayout.addSpacerItem(spacer)
        outerLayout.addLayout(toolsLayout)

        clusterLayout.addWidget(
            self.cluster,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        outerLayout.addLayout(clusterLayout)
        outerLayout.addSpacerItem(spacer)

        btnsLayout.addWidget(self.delBtn)
        btnsLayout.addWidget(self.shflBtn)
        btnsLayout.addWidget(self.entrBtn)
        outerLayout.addLayout(btnsLayout)
        outerLayout.addSpacerItem(spacer)

        self.setLayout(outerLayout)

    ###########################################################################
    # _onHexClicked
    #
    # DESCRIPTION:
    #   Catch signal from cluster and update uInput text field to reflect
    #   signal
    ###########################################################################
    def _onHexClicked(self):
        sender = self.sender()
        self.uInput.setText(f'{self.uInput.text()}{sender.text}')

    ###########################################################################
    # _onUInputEdited(self, txt):
    #
    # DESCRIPTION:
    #   force input text to uppercase
    ###########################################################################
    def _onUInputEdited(self, txt):
        self.uInput.setText(txt.upper())
