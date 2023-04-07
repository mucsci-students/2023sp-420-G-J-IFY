import sys, os
from PyQt6 import QtCore, QtWidgets, QtGui
from gview.HexCluster import HexLabel, HexButton

class WelcomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)
        
        self.title = HexLabel(self, radius=100)
        self.sub_title = QtWidgets.QLabel()
        self.new_btn = QtWidgets.QPushButton()
        self.load_btn = QtWidgets.QPushButton()
        
        self._initUI()
        
    def _initUI(self):
        
        # Initialize widgets
        self.title.setText("Spelling\nBee")
        self.sub_title.setText("Presented by: G[J]IFY")
        self.new_btn.setText("New Game")
        self.load_btn.setText("Load Save")
        
        # Formatting
        font_id = QtGui.QFontDatabase.addApplicationFont(
            os.getcwd() + '/fonts/Comfortaa-VariableFont_wght.ttf'
        )
        families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        
        title_font = QtGui.QFont(families[0], 36, 700)
        title_f_color = QtGui.QColor('#262626')
        title_color = QtGui.QColor('#FFCC2F')
        sub_font = QtGui.QFont(families[0], 18, 400)
        self.title.setFont(title_font)
        self.title.setFontColor(title_f_color)
        self.title.setColor(title_color)
        self.sub_title.setFont(sub_font)
        
        # Alignment
        # self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sub_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        
        # Layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.title, 0, 0, 1, 2)
        layout.addWidget(self.sub_title, 1, 0, 1, 2)
        layout.addWidget(
            self.new_btn,
            2,
            0,
            QtCore.Qt.AlignmentFlag.AlignTop
            | QtCore.Qt.AlignmentFlag.AlignRight
        )
        layout.addWidget(
            self.load_btn,
            2,
            1,
            QtCore.Qt.AlignmentFlag.AlignTop
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.setLayout(layout)
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = WelcomePage()
    window.show()
    sys.exit(app.exec())