###############################################################################
# Leaderboard.py
# Author: Gaige Zakroski, Isaak Weidman
# Date of Creation: 04/16/2023
#
# DESCRIPTION:
#   A custom leaderboard dialog that holds the list of highScores
#
# CLASSES:
#   Leaderboard
###############################################################################
from PyQt6 import QtWidgets, QtGui, QtCore
from gview.HexCluster import HexLabel

###############################################################################
# class Leaderboard(QtWidgets.QWidget)
#
# DESCRIPTION:
#   Leaderboard dialog box of the high scores
#
# ARGUMENTS:
#   parent: QtWidgets.QWidget
#    - the parent of the dialog box
#
#   leaderboard: list[tuple]
#    - the list of highscores for a given game
#
# ATRIBUTES:
#   header: QtWidgets.QLabel
#    - header for the leader board dialog box
#
#   leaderboad: list[tupel]
#    - the list of highscores for a given game
#
# FUNCTIONS:
#   _initUI() -> None
#    - creates and fills the leaderboard dialog box
#
#   _buildLeaderboard() -> QtWidgets.QWidget:
#    - fills the layout of the dialog box


class Leaderboard(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None,
                 leaderboard: list[tuple]):
        super(Leaderboard, self).__init__(parent)

        self.header = QtWidgets.QLabel()
        self.leadboard = leaderboard
        self._initUI()

    def _initUI(self) -> None:
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())

        layout = QtWidgets.QVBoxLayout()

        self.header.setText('Leaderboard')
        self.header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.header)
        wig = self._buildLeaderboard()
        wig.setFixedSize(300, 700)  
        layout.addWidget(wig)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # set the layout of the scroll area widget
        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setLayout(layout)
        scrollArea.setWidget(scrollWidget)

        # set the Leaderboard widget as the child of the scroll area widget
        scroll_area_layout = QtWidgets.QVBoxLayout()
        scroll_area_layout.addWidget(scrollArea)
        self.setLayout(scroll_area_layout)
        self.setLayout(layout)

    def _buildLeaderboard(self) -> QtWidgets.QWidget:
        outWig = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        for i in range(10):
            placeLabel = HexLabel(None, str(i + 1), 15)
            if i == 0:
                placeLabel.setColor(QtGui.QColor('#ffcc2f'))
            else:
                placeLabel.setColor(QtGui.QColor(210, 210, 210))

            rowLayout = QtWidgets.QHBoxLayout()
            rowLayout.addWidget(placeLabel)

            hLine = QtWidgets.QFrame(self)
            hLine.setStyleSheet('color: rgb(210, 210, 210);')
            hLine.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            hLine.setFixedHeight(1)

            if not i >= len(self.leadboard):
                elm = self.leadboard[i]
                nameLabel = QtWidgets.QLabel(elm[0])
                nameLabel.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                rankLabel = QtWidgets.QLabel(elm[1])
                rankLabel.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                scoreLabel = QtWidgets.QLabel(str(elm[2]))
                scoreLabel.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                rowLayout.addWidget(nameLabel)
                rowLayout.addWidget(rankLabel)
                rowLayout.addWidget(scoreLabel)

            else:
                dashWig = QtWidgets.QLabel('---')
                rowLayout.addWidget(dashWig)

            layout.addLayout(rowLayout)
            layout.addWidget(hLine)

        outWig.setLayout(layout)

        return outWig
