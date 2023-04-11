import os
from PyQt6 import QtCore, QtWidgets, QtGui
from gview.HexCluster import HexLabel


##############################################################################
# class WelcomePage(QtWidgets.QWidget)
#
# DESCRIPTION:
#   defines the landing page the user sees when the game is launched
##############################################################################
class WelcomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)

        self.title = HexLabel(self, radius=100)
        self.sub_title = QtWidgets.QLabel()
        self.new_btn = QtWidgets.QPushButton()
        self.custom_btn = QtWidgets.QPushButton()
        self.load_btn = QtWidgets.QPushButton()
        self.exit_btn = QtWidgets.QPushButton()

        self._initUI()

    ##########################################################################
    # _initUI() -> None
    #
    # DESCRIPTION:
    #   initializes the layout and basic functionality of the UI
    ##########################################################################
    def _initUI(self):
        # Apply style sheet
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())

        # Initialize widgets
        self.title.setText("Spelling\nBee")
        self.sub_title.setText("Presented by: G[J]IFY")
        self.new_btn.setText("New Game")
        self.custom_btn.setText("Custom Game")
        self.load_btn.setText("Load Save")
        self.exit_btn.setText("Quit To Desktop")

        # Formatting
        font_id = QtGui.QFontDatabase.addApplicationFont(
            os.getcwd() + '/fonts/Comfortaa-VariableFont_wght.ttf'
        )
        families = QtGui.QFontDatabase.applicationFontFamilies(font_id)

        title_font = QtGui.QFont(families[0], 36, 900)
        title_f_color = QtGui.QColor('#262626')
        title_color = QtGui.QColor('#FFCC2F')
        sub_font = QtGui.QFont(families[0], 18, 400)
        self.title.setFont(title_font)
        self.title.setFontColor(title_f_color)
        self.title.setColor(title_color)
        self.sub_title.setFont(sub_font)
        # Define btn sizes
        self.new_btn.setFixedSize(200, 45)
        self.custom_btn.setFixedSize(200, 45)
        self.load_btn.setFixedSize(200, 45)
        self.exit_btn.setFixedSize(200, 45)
        # Alignment
        self.sub_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        # Build left side of the widget
        imageLayout = QtWidgets.QVBoxLayout()
        imageLayout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        imageLayout.addWidget(self.title)
        imageLayout.addWidget(self.sub_title)
        imageWidget = QtWidgets.QWidget()
        imageWidget.setLayout(imageLayout)
        # Build right side of the widget
        btnsLayout = QtWidgets.QVBoxLayout()
        btnsLayout.addSpacerItem(QtWidgets.QSpacerItem(
            0,
            30,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        ))
        btnsLayout.addWidget(
            self.new_btn,
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignRight
        )
        btnsLayout.addWidget(
            self.custom_btn,
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignRight
        )
        btnsLayout.addWidget(
            self.load_btn,
            QtCore.Qt.AlignmentFlag.AlignVCenter
            | QtCore.Qt.AlignmentFlag.AlignRight
        )
        btnsLayout.addWidget(
            self.exit_btn,
            QtCore.Qt.AlignmentFlag.AlignTop
            | QtCore.Qt.AlignmentFlag.AlignRight
        )
        btnsLayout.addSpacerItem(QtWidgets.QSpacerItem(
            0,
            30,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        ))
        btnsWidget = QtWidgets.QWidget()
        btnsWidget.setLayout(btnsLayout)
        # Put the two halves together
        layout = QtWidgets.QHBoxLayout()
        layout.addSpacerItem(QtWidgets.QSpacerItem(
            30,
            0,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        ))
        layout.addWidget(imageWidget)
        layout.addSpacerItem(QtWidgets.QSpacerItem(
            30,
            0,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        ))
        layout.addWidget(btnsWidget)
        layout.addSpacerItem(QtWidgets.QSpacerItem(
            50,
            0,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        ))

        self.setLayout(layout)
