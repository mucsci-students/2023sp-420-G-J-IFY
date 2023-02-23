#!/usr/bin/env

################################################################################
# StatsPanel.py
# AUTHOR: Isaak Weidman
# DATE OF CREATION: 02-18-2023
#
# CLASSES:
#   
#
# FUNCTIONS:
#
#
################################################################################

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QSizePolicy,
    QGridLayout,
    QWidget,
    QLabel,
    QProgressBar,
    QTextEdit,
)

class StatsPanel(QWidget):
    def __init__(self, parent: QWidget | None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.level = QLabel(self)
        self.pBar = QProgressBar(self)
        self.foundWords = QTextEdit(self)

        self.initUI()

    def initUI(self) -> None:

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding
        )

        # initialize defaults for level
        self.level.setFont(QFont('Helvetica', 18))
        self.level.setText('Level')
        # initialize defaults for pBar
        self.pBar.setValue(30)
        # initialize defaults for foundWords:
        self.foundWords.setReadOnly(True)
        self.foundWords.setFont(QFont('Helvetica', 16))
        self.foundWords.setText('Found Words:')

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

        layout.addWidget(self.level, 0, 0)
        layout.addWidget(self.pBar, 0, 1)
        # found Words spans both columns in grid
        layout.addWidget(
            self.foundWords,
            1,
            0,
            1,
            2
        )

        self.setLayout(layout)