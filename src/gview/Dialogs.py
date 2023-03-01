import sys
from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtGui import (
    QFont,
)
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QComboBox,
)


class LoadDialog(QDialog):
    def __init__(self, parent: QWidget, *args, **kwargs):
        super(LoadDialog, self).__init__(parent, *args, **kwargs)

        self.uInput = QLineEdit(self)
        self.btns = QDialogButtonBox(self)

        self.initUI()

    def initUI(self):

        self.setFixedSize(200, 100)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.uInput.setPlaceholderText('Save File Name')

        self.btns.setStandardButtons (
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Open
        )

        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)

        layout.addWidget(self.uInput)
        layout.addWidget(self.btns)

        self.setLayout(layout)



class LoadFailedDialog(QDialog):
    def __init__(self, parent : QWidget, *args, **kwargs):
        super(LoadFailedDialog, self).__init__(parent, *args, **kwargs)

        self.message = QLabel(self)
        self.btns = QDialogButtonBox(self)

        self.initUI()

    def initUI(self):

        self.setFixedSize(200, 100)

        layout = QVBoxLayout()

        font = QFont()
        font.setFamily('Helvetica')
        font.setPointSize(16)

        self.message.setFont(font)
        self.message.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.message.setText('Load game failed...')

        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
        )
        self.btns.accepted.connect(self.accept)

        layout.addWidget(self.message)
        layout.addWidget(self.btns)

        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication([])
    dialog = LoadFailedDialog(parent=None)
    dialog.show()
    sys.exit(app.exec())