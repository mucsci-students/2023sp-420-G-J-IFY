import sys
from PyQt6 import QtCore, QtWidgets, QtGui

class WelcomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)
        
        self.title = QtWidgets.QLabel()
        self.sub_title = QtWidgets.QLabel()
        self.new_btn = QtWidgets.QPushButton()
        self.load_btn = QtWidgets.QPushButton()
        
        self._initUI()
        
    def _initUI(self):
        
        # Initialize widgets
        self.title.setText("Spelling Bee")
        self.sub_title.setText("Presented by: G(J)IFY")
        self.new_btn.setText("New Game")
        self.load_btn.setText("Load Save")
        
        # Formatting
        title_font = QtGui.QFont('Helvetica', 24, 700)
        sub_font = QtGui.QFont('Helvetica', 14, 100)
        self.title.setFont(title_font)
        self.sub_title.setFont(sub_font)
        
        # Alignment
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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