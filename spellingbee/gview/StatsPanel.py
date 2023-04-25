#!/usr/bin/env
###############################################################################
# StatsPanel.py
# AUTHOR: Isaak Weidman
# DATE OF CREATION: 02-18-2023
#
# CLASSES:
#   StatsPanel(QWidget)
###############################################################################
from model.puzzle import Puzzle
from PyQt6.QtWidgets import (
    QSizePolicy,
    QGridLayout,
    QWidget,
    QLabel,
    QProgressBar,
    QTextEdit,
)


###############################################################################
# class StatsPanel()
#
# DESCRIPTION:
#   Widget that displays game progress to the user
#
# ARGUMENTS:
#   parent : QWidget | None
#     - parent widget
#
# ATTRIBUTES:
#   level : QLabel
#     - Text representation of players progress
#   pBar : QProgressbar
#     - progress bar displaying % of game completed
#   foundWords : QTextEdit
#     - list of all words found by the user
###############################################################################
class StatsPanel(QWidget):
    def __init__(self, parent: QWidget | None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.level = QLabel(self)
        self.pBar = QProgressBar(self)
        self.ptsToNxt = QLabel(self)
        self.statsWidget = QWidget()
        self.foundWords = QTextEdit(self)
        self.header = '**Found Words:** \n ___\n'

        self.initUI()

    ###########################################################################
    # initUI() -> None
    #
    # DESCRIPTION:
    #   initialize attributes and layout
    ###########################################################################
    def initUI(self) -> None:
        # Apply style sheet
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())

        self.setFixedWidth(300)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.MinimumExpanding
        )

        # initialize defaults for level
        self.level.setText('Beginner')
        # initialize defaults for pBar
        self.pBar.setValue(0)

        # initialize ptsToNxt
        self.ptsToNxt.setText(
            'Score: 0\n'
            'Points To Next Level: 1'
        )

        # initialize defaults for foundWords:
        self.foundWords.setReadOnly(True)
        self.foundWords.setMarkdown(self.header)

        # Size Policies:
        # level is at its minimum size defined
        self.level.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed
        )
        # pBar stretches horizontally
        self.pBar.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.Fixed
        )
        # foundWords takes up maximum vertical space possible
        self.foundWords.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )

        # Populate widget
        layout = QGridLayout()
        self.statsWidget = self._buildStatusWidget()
        layout.addWidget(self.statsWidget)
        # found Words spans both columns in grid
        layout.addWidget(
            self.foundWords,
            2,
            0,
            1,
            2
        )

        self.setLayout(layout)

    ###########################################################################
    # update(puzzle : Puzzle) -> None
    #
    # DESCRIPTION:
    #   Update information in stats panel to reflect current state of the game
    ###########################################################################
    def update(self, puzzle: Puzzle) -> None:

        self.level.setText(puzzle.getRank())

        # Calculate percentage as integer to display on pBar
        self.pBar.setValue(int((puzzle.getScore() /
                                puzzle.getMaxScore()) * 100))

        # Create formatted string to display score information
        ptsToNxtStr = (
            'Score: {score}\n'
            'Points to next level: {pts}'
        ).format(score=puzzle.getScore(), pts=puzzle.getPointsTilRank())
        self.ptsToNxt.setText(ptsToNxtStr)

        # Build body of found words area
        body = self.header
        for word in puzzle.getFoundWords():
            body += f'{word.upper()} \n\n'
        self.foundWords.setMarkdown(body)

    ##########################################################################
    # _buildStatusWidget() -> QWidget:
    #
    # DESCRIPTION
    #   builds a separate widget to display the top portion of the widget
    ##########################################################################
    def _buildStatusWidget(self) -> QWidget:
        widget = QWidget()
        layout = QGridLayout()

        layout.addWidget(self.level, 0, 0)
        layout.addWidget(self.pBar, 0, 1)
        layout.addWidget(
            self.ptsToNxt,
            1,
            0,
            1,
            2
        )

        widget.setLayout(layout)
        return widget
