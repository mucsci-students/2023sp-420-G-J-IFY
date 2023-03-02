import sys
from PyQt6.QtCore import (
    Qt,
    QRegularExpression,
)
from PyQt6.QtGui import (
    QFont,
    QRegularExpressionValidator,
    QCursor,
)
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QSpacerItem,
    QStackedWidget,
    QLabel,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QComboBox,
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


class NewDialog(QDialog):
     def __init__(self, parent : QWidget=None, *args, **kwargs):
         super(NewDialog, self).__init__(parent, *args, **kwargs)

         self.setFixedSize(self.minimumSize())
         self.setSizePolicy(
             QSizePolicy.Policy.Fixed,
             QSizePolicy.Policy.Fixed
         )
         self.setModal(True)

         self.stack = QStackedWidget(self)

         self.warningMsg = QLabel(self)
         self.advBtn = QPushButton(self)
         self.warningBtns = QDialogButtonBox(self)

         self.baseWrd = QLineEdit(self)
         self.keyLett = QComboBox(self)
         self.advBtns = QDialogButtonBox(self)

         self._initUI()

         self.display()

     def _initUI(self):

         layout = QVBoxLayout()

         warning = self._initWarningPage()
         advanced = self._initAdvNewPage()

         self.stack.addWidget(warning)
         self.stack.addWidget(advanced)

         layout.addWidget(self.stack)

         self.setLayout(layout)



     def _initWarningPage(self) -> QWidget:

         page = QWidget(self)
         layout = QVBoxLayout()
         advLayout = QHBoxLayout()

         # Warning message setup and formatting
         self.warningMsg.setText(
             'Are you sure? All unsaved progress will be lost.'
         )
         self.warningMsg.setWordWrap(True)
         self.warningMsg.setSizePolicy(
             QSizePolicy.Policy.MinimumExpanding,
             QSizePolicy.Policy.MinimumExpanding
         )

         # Advanced button setup and formatting
         font = QFont()
         font.setUnderline(True)
         self.advBtn.setStyleSheet("color: blue; border: none")
         self.advBtn.setFont(font)
         self.advBtn.setText('Advanced')
         self.advBtn.setFlat(True)
         self.advBtn.setCursor(Qt.CursorShape.PointingHandCursor)
         self.advBtn.setSizePolicy(
             QSizePolicy.Policy.Fixed,
             QSizePolicy.Policy.Fixed
         )
         self.advBtn.setFixedSize(self.advBtn.minimumSizeHint())
         self.advBtn.clicked.connect(lambda: self.display(1))

         # Spacer to move Advanced button to the right
         advLayout.addSpacerItem(
             QSpacerItem(5, 0, QSizePolicy.Policy.MinimumExpanding)
         )
         advLayout.addWidget(self.advBtn)

         # Dialog buttons setup, formatting, and tentative connections
         self.warningBtns.setStandardButtons(
             QDialogButtonBox.StandardButton.Cancel
             | QDialogButtonBox.StandardButton.Ok
         )
         self.warningBtns.button(
             QDialogButtonBox.StandardButton.Ok
         ).setText('Yes')
         self.warningBtns.accepted.connect(self.accept)
         self.warningBtns.rejected.connect(self.reject)

         # Populate the widget
         layout.addWidget(self.warningMsg)
         layout.addLayout(advLayout)
         layout.addWidget(self.warningBtns)
         page.setLayout(layout)
         return page



     def _initAdvNewPage(self) -> QWidget:

         page = QWidget(self)
         layout = QVBoxLayout()
         form = QFormLayout()

         regex = QRegularExpression(
             '[A-Z|a-z]+'
         )
         validator = QRegularExpressionValidator(regex)
         self.baseWrd.setValidator(validator)

         self.baseWrd.textEdited.connect(self._populateCombo)

         self.advBtns.setStandardButtons(
             QDialogButtonBox.StandardButton.Cancel
             | QDialogButtonBox.StandardButton.Ok
         )
         self.advBtns.button(
             QDialogButtonBox.StandardButton.Cancel
         ).setText('Back')
         self.advBtns.button(
             QDialogButtonBox.StandardButton.Ok
         ).setText('Apply')

         self.advBtns.rejected.connect(lambda: self.display(0))

         form.addRow('Baseword:', self.baseWrd)
         form.addRow('Key Letter:', self.keyLett)

         layout.addLayout(form)
         layout.addWidget(self.advBtns)
         page.setLayout(layout)
         return page

     def _populateCombo(self, word: str) -> None:
         self.keyLett.clear()

         uniqueLett = list(set(word))

         for l in uniqueLett:
             self.keyLett.addItem(l.upper())



     def display(self, i : int=0) -> None:
         self.stack.setCurrentIndex(i)


class SaveDialog(QDialog):
    def __init__(self, parent : QWidget | None, *args, **kwargs):
        super(SaveDialog, self).__init__(parent, *args, **kwargs)

        self.fileName = QLineEdit(self)
        self.justPuzzle = QCheckBox(self)
        self.btns = QDialogButtonBox(self)

        self.setFixedSize(200, 150)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        self._initUI()

    def _initUI(self):

        layout = QVBoxLayout()

        regex = QRegularExpression(
            '[A-Z|a-z|0-9|\.|_|-]+'
        )
        validator = QRegularExpressionValidator(regex)
        self.fileName.setValidator(validator)
        self.fileName.setPlaceholderText('File Name')

        self.justPuzzle.setText('Save blank puzzle')

        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Save
        )
        self.btns.rejected.connect(self.reject)

        layout.addWidget(self.fileName)
        layout.addWidget(self.justPuzzle)
        layout.addWidget(self.btns)

        self.setLayout(layout)



class SaveOverwriteDialog(QDialog):
    def __init__(self, parent : QWidget | None, *args, **kwargs):
        super(SaveOverwriteDialog, self).__init__(parent, *args, **kwargs)

        self.message = QLabel(self)
        self.btns = QDialogButtonBox(self)

        self.setFixedSize(200, 125)

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        self._initUI()

    def _initUI(self):

        layout = QVBoxLayout()

        self.message.setText(
            'The file name you entered already exists. '
            'Would you like to overwrite?'
        )
        self.message.setWordWrap(True)

        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        self.btns.rejected.connect(self.reject)

        layout.addWidget(self.message)
        layout.addWidget(self.btns)

        self.setLayout(layout)
