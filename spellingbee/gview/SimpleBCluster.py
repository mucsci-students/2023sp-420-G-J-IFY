#!/usr/bin/env

################################################################################
# ButtonCluster.py
# Author: Isaak Weidman
# Date of Creation: 02-18-2023
#
# Classes:
#
# Functions:
#
################################################################################

import sys, os
filePath = os.path.dirname(__file__)
sys.path.append(filePath)

from PyQt6.QtGui import (
    QFont,
)
from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtWidgets import (
    QSizePolicy,
    QSpacerItem,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
)


################################################################################
# class simpleButtonCluster()
#
# DESCRIPTION:
#   
#
# ARGUMENTS:
#   *args : 
#
#   **kwargs :
#
#
################################################################################
class simpleButtonCluster(QWidget):
    def __init__(
        self,
        parent: QWidget | None,
        letters: list[str] | None,
        *args, 
        **kwargs
    ) -> None:
        super(simpleButtonCluster, self).__init__(parent, *args, **kwargs)

        self.uInput = QLineEdit(self)
        self.btnCluster = _Cluster(self, letters)
        self.delBtn = QPushButton('Delete', self)
        self.shflBtn = QPushButton('Shuffle', self)
        self.entrBtn = QPushButton('Enter', self)

        self._initUI()

    def _initUI(self) -> None:

        vLayout = QVBoxLayout()
        hLayout = QHBoxLayout()
        ctrlBtns = QWidget(self)
        hLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.uInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uInput.setFrame(False)
        self.uInput.setFont(QFont("Helvetica", 25))
        self.uInput.setStyleSheet("background : rgba(0, 0, 0, 0)")

        self.uInput.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding
        )

        self.btnCluster.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding
        )

        self.delBtn.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )
        self.shflBtn.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        self.entrBtn.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        ctrlBtns.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding
        )

        hLayout.addWidget(self.delBtn)
        hLayout.addWidget(self.shflBtn)
        hLayout.addWidget(self.entrBtn)
        ctrlBtns.setLayout(hLayout)

        vLayout.addWidget(self.uInput)
        vLayout.addWidget(self.btnCluster)
        vLayout.addWidget(ctrlBtns)

        self.setLayout(vLayout)


class _Cluster(QWidget):
    def __init__(
        self,
        parent: QWidget | None,
        letters: list[str],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(parent, *args, **kwargs)

        outerLayout = QVBoxLayout()
        r1layout = QHBoxLayout()
        r2layout = QHBoxLayout()
        r3layout = QHBoxLayout()

        self._letters = letters
        self.buttons = self._createButtons()

        r1layout.addWidget(self.buttons[1])
        r1layout.addWidget(self.buttons[2])

        r2layout.addWidget(self.buttons[3])
        r2layout.addWidget(self.buttons[0])
        r2layout.addWidget(self.buttons[4])

        r3layout.addWidget(self.buttons[5])
        r3layout.addWidget(self.buttons[6])

        outerLayout.addLayout(r1layout)
        outerLayout.addLayout(r2layout)
        outerLayout.addLayout(r3layout)

        outerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(outerLayout)


    def _createButtons(self) -> list[QWidget]:
        bList: list[QWidget] = []
        for l in self._letters:
            btn = QPushButton(l, self)
            btn.setFixedSize(60, 60)
            bList.append(btn)
        return bList