from PyQt6 import QtWidgets, QtGui, QtCore
from gview.HexCluster import HexLabel


class Leaderboard(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None,
                 leaderboard: list[tuple]):
        super(Leaderboard, self).__init__(parent)

        self.header = QtWidgets.QLabel()
        self.leadboard = leaderboard
        self._initUI()

    def _initUI(self):
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())

        layout = QtWidgets.QVBoxLayout()

        self.header.setText('Leaderboard')
        self.header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.header)
        wig = self._buildLeaderboard()
        layout.addWidget(wig)
        self.setLayout(layout)

    def _buildLeaderboard(self):
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
            # layout.addWidget(hLine)

        outWig.setLayout(layout)

        return outWig
