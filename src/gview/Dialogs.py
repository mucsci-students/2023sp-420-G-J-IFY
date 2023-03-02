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
        
        self.advBtns.accepted.connect(self.accept)
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

        for l in word:
            self.keyLett.addItem(l)

    

    def display(self, i : int=0) -> None:
        self.stack.setCurrentIndex(i)