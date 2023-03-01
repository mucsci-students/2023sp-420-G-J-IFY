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

import sys, os
filePath = os.path.dirname(__file__)
sys.path.append(filePath)

from SimpleBCluster import simpleButtonCluster
from StatsPanel import StatsPanel
from HexCluster import HexCluster
from Dialogs import (
    LoadDialog,
    LoadFailedDialog,
)
from PyQt6.QtGui import (
    QAction,
    QFont,
    QRegularExpressionValidator,
    QValidator,
)
from PyQt6.QtCore import (
    Qt,
    QRegularExpression,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpacerItem,
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
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Attributes
        

        # Tentative placeholder
        self.setWindowTitle('Spelling Bee')
        self.setGeometry(100, 100, 700, 400)

        self.letters = ['W', 'A', 'R', 'L', 'O', 'C', 'K']
        

        # Creation Functions
        self._createCentralWidget()
        self._createMenuBar()
        self._createToolBar()
        self._createStatsBar()
        

    ############################################################################
    # _createMenuBar()
    #
    # DESCRIPTION:
    #   creates menubar attributes and actions
    ############################################################################
    def _createMenuBar(self):

        # Create manu bar
        menuBar = self.menuBar()

        # Add menu bar options
        fileMenu = menuBar.addMenu('&File')
        windowMenu = menuBar.addMenu('&Window')
        helpMenu = menuBar.addMenu('Help')
        
        # Attach example action to each option
        action = QAction('A menu action', self)
        fileMenu.addAction(action)
        windowMenu.addAction(action)
        helpMenu.addAction(action)


    ############################################################################
    # _createToolBar()
    #
    # DESCRIPTION:
    #   creates toolbar buttons and actions
    ############################################################################
    def _createToolBar(self):

        # Create static tool bar
        toolBar = QToolBar('Tools', self)
        toolBar.setMovable(False)

        # add buttons to tool bar
        newAction = QAction('New', self)
        saveAction = QAction('Save', self)
        loadAction = QAction('Load', self)
        loadAction.triggered.connect(self._onLoadBtnClicked)
        statsAction = QAction('Stats', self)
        helpAction = QAction('Help', self)

        # add actions to tool bar
        toolBar.addAction(newAction)
        toolBar.addAction(saveAction)
        toolBar.addAction(loadAction)
        toolBar.addAction(statsAction)
        toolBar.addAction(helpAction)

        self.addToolBar(toolBar)


    ############################################################################
    # _createStatsbar()
    #
    # DESCRIPTION:
    #   creates status bar to the right to display user progress and found words
    ############################################################################
    def _createStatsBar(self):

        # create static tool
        statsBar = QToolBar('Stats', self)
        statsBar.setMovable(False)

        # Create StatsPanel widget parented to this toolbar
        statsPanel = StatsPanel(statsBar)
        statsBar.addWidget(statsPanel)

        # Move toolbar to the right of Central Widget
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, statsBar)


    ############################################################################
    # _createCentralWidget(self):
    #
    # DESCRIPTION:
    #   creates central widget
    ############################################################################
    def _createCentralWidget(self):
        self.setCentralWidget(GameWidget(self, self.letters))

    def _onLoadBtnClicked(self):

        loadDlg = LoadDialog(self)
        loadDlg.show()




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
    def __init__(self, parent: QWidget, letters: list[str], *args, **kwargs):
        super(GameWidget, self).__init__(parent, *args, **kwargs)

        self.uInput = QLineEdit(self)
        self.cluster = HexCluster(self, letters)
        self.delBtn = QPushButton('Delete', self)
        self.shflBtn = QPushButton('Shuffle', self)
        self.entrBtn = QPushButton('Enter', self)
        self.letters = letters

        # Append each cluster button's text to user input field when clicked
        for btn in self.cluster.buttons:
            btn.clicked.connect(self._onHexClicked)

        self.uInput.textEdited.connect(self._onUInputEdited)

        self._initUI()


    ############################################################################
    # _initUI
    #  
    # DESCRIPTION:
    #   initialize layout of widgets and set important attributes
    ############################################################################
    def _initUI(self):

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
        font = QFont("Arial", 30)
        font.setBold(True)
        self.uInput.setFont(font)
        self.uInput.setStyleSheet("background : rgba(0, 0, 0, 0)")

        # regular expression that only allows key letters, upper and lower.
        # ex. [W|A|R|L|O|C|K]+|[w|a|r|l|o|c|k]+
        regex = QRegularExpression(
            f"[{'|'.join(self.letters).upper()}|"
            f"{'|'.join(self.letters).lower()}]+"
        )
        print(regex)
        # Create and set uInput validator
        validator = QRegularExpressionValidator(regex)
        self.uInput.setValidator(validator)

        # Set size policies
        self.uInput.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding
        )

        self.cluster.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.MinimumExpanding
        )

        # Populate layouts, moving top to bottom
        outerLayout.addWidget(self.uInput)

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

    def _onUInputEdited(self, txt):
        self.uInput.setText(txt.upper())

def main():
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()