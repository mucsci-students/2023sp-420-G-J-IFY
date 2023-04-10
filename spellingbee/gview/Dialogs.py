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


################################################################################
# class LoadDialog()
#
# DESCRIPTION
#   Opens a simple menu that allows user to load a saved game by providing
#   the save's name.
#
# ATTRIBUTES
#   uInput : QLineEdit
#     - User input field
#   btns : QDialogButtonBox
#     - standard buttons for acceptance or rejection
# FUNCTIONS
#   initUI() -> None
#     - initializes and builds the user interface
################################################################################
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
        # acceptance event must be handled by controller. Rejection follows
        # standard rejection procedure.
        self.btns.rejected.connect(self.reject)

        layout.addWidget(self.uInput)
        layout.addWidget(self.btns)

        self.setLayout(layout)



################################################################################
# class LoadFailedDialog()
#
# DESCRIPTION
#   Notifies the user that a file failed to load.
#
# ATTRIBUTES
#   message : QLabel
#     - Message for user
#   btns : QDialogButtonBox
#     - Stnadard buttons for acceptance/rejection
################################################################################
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


##############################################################################
# class NewDialog()
#
# DESCRIPTION
#   GUI giving the user the ability to create either a new random game or to
#   create a new game from a provided baseword and keyletter.
#
# ATTRIBUTES
#   stack : QStackedWidget
#   warningMsg : QLabel
#   advBtn : QPushButton
#   backBtn : QPushButton
#   baseWrd : QLineEdit
#   keyLett : QComboBox
#   btns : QDialogButtonBox
# 
# FUNCTIONS
#   display(i : int=0) -> None
#
#   reject() -> None:
#
#   accept() -> None:
##############################################################################
class NewDialog(QDialog):
    def __init__(self, parent: QWidget = None, *args, **kwargs):
        super(NewDialog, self).__init__(parent, *args, **kwargs)

        self.setFixedSize(self.minimumSize())
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        # Sets dialog to modal meaning nothing can be done in parent widget
        # until this dialog is either accepted or rejected.
        self.setModal(True)
         
        # Declare attributes
        self.stack = QStackedWidget(self)

        self.warningMsg = QLabel(self)
        self.advBtn = QPushButton(self)
        self.backBtn = QPushButton(self)

        self.baseWrd = QLineEdit(self)
        self.keyLett = QComboBox(self)

        self.btns = QDialogButtonBox(self)
         
        # initialize display
        self._initUI()
         
        # display first page on stack
        self.display(0)
     
    ############################################################################
    # _initUI() -> None
    ############################################################################
    def _initUI(self) -> None:

        layout = QVBoxLayout()
        
        # Create pages
        warning = self._initWarningPage()
        advanced = self._initAdvNewPage()

        # Add pages to stack
        self.stack.addWidget(warning)
        self.stack.addWidget(advanced)

        layout.addWidget(self.stack)

        # Set standard buttons
        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        # Acceptance must but defined in controller
        self.btns.rejected.connect(self.reject)

        layout.addWidget(self.btns)

        self.setLayout(layout)


    ############################################################################
    # _initWarningPage() -> QWidget
    ############################################################################
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
        font = QFont('Comfortaa')
        font.setUnderline(True)
        self.advBtn.setStyleSheet("color: blue;")
        self.advBtn.setFont(font)
        self.advBtn.setText('Advanced')
        self.advBtn.setFlat(True)
        self.advBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        """
        self.advBtn.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )"""
        # self.advBtn.setFixedSize(self.advBtn.minimumSizeHint())
        self.advBtn.clicked.connect(lambda: self.display(1))

        # Spacer to move Advanced button to the right
        advLayout.addSpacerItem(
            QSpacerItem(5, 0, QSizePolicy.Policy.MinimumExpanding)
        )
        advLayout.addWidget(self.advBtn)

        # Populate the widget
        layout.addWidget(self.warningMsg)
        layout.addLayout(advLayout)
        page.setLayout(layout)
        return page


    ############################################################################
    # _initAdvNewPage() -> QWidget
    ############################################################################
    def _initAdvNewPage(self) -> QWidget:

        # Create page attributes
        page = QWidget(self)
        layout = QVBoxLayout()
        backLayout = QHBoxLayout()
        form = QFormLayout()

        # Set validator to only accept alphas
        regex = QRegularExpression(
            '[A-Z|a-z]+'
        )
        validator = QRegularExpressionValidator(regex)
        self.baseWrd.setValidator(validator)

        # Populate combo box with unique letters from baseWrd
        self.baseWrd.textEdited.connect(self._populateCombo)

        # Format backBtn and place to the right
        font = QFont()
        font.setUnderline(True)
        self.backBtn.setStyleSheet("color: blue; border: none")
        self.backBtn.setFont(font)
        self.backBtn.setText('Back')
        self.backBtn.setFlat(True)
        self.backBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backBtn.setSizePolicy(
             QSizePolicy.Policy.Fixed,
             QSizePolicy.Policy.Fixed
        )
        self.backBtn.setFixedSize(self.backBtn.minimumSizeHint())
        self.backBtn.clicked.connect(lambda: self.display(0))

        # Spacer to move Advanced button to the right
        backLayout.addSpacerItem(
            QSpacerItem(5, 0, QSizePolicy.Policy.MinimumExpanding)
        )
        backLayout.addWidget(self.backBtn)

        form.addRow('Baseword:', self.baseWrd)
        form.addRow('Key Letter:', self.keyLett)

        layout.addLayout(form)
        layout.addLayout(backLayout)
        page.setLayout(layout)
        return page


    ############################################################################
    # _populateCombo(word : str) -> None
    ############################################################################
    def _populateCombo(self, word: str) -> None:
        self.keyLett.clear()

        uniqueLett = list(set(word))

        for l in uniqueLett:
            self.keyLett.addItem(l.upper())


    ############################################################################
    # display(i : int=0) -> None
    ############################################################################
    def display(self, i : int=0) -> None:
        self.stack.setCurrentIndex(i)


    ############################################################################
    # reject() -> None
    ############################################################################
    def reject(self) -> None:
        self.baseWrd.clear()
        self.keyLett.clear()
        self.display(0)
        super().reject()


    ############################################################################
    # accept() -> None
    ############################################################################
    def accept(self) -> None:
        self.baseWrd.clear()
        self.keyLett.clear()
        self.display(0)
        super().accept()



################################################################################
# class SaveDialog()
#
# DESCRIPTION
#   A simple dialog prompting user for relavant information required to save
#   their game
#
# ATTRIBUTES
#   fileName : QLineEdit
#     - The name under which the file will be4 saved
#   justPuzzle : QCheckBox
#     - a checkbox giving the user to save a blank copy of their game
#   btns : QDialogButtonBox
#     - standard buttons for acceptance/rejection
################################################################################
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



################################################################################
# class SaveOverwriteDialog()
#
# DESCRIPTION
#   Notifies the user that a game already exists under the provided name and
#   asks if they would like to overwrite that save.
#
# ATTRIBUTES
#   message : QLabel
#       Notification message
#   btns : QDialogButtonBox
#       standard buttons for acceptance/rejection
# FUNCTIONS
################################################################################
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



################################################################################
# class HelpDialog()
#
# DESCRIPTION
#   Gives the user a breif overview of the game and how its played.
################################################################################
class HelpDialog(QDialog):
    def __init__(self, parent : QWidget | None, *args, **kwargs):
        super(HelpDialog, self).__init__(parent, *args, **kwargs)

        self.instructions = QLabel(self)
        self.btns = QDialogButtonBox(self)

        self.setMinimumHeight(170)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        self._initUI()

    def _initUI(self):
        
        layout = QVBoxLayout()
        self.setModal(True)
        self.instructions.setText(
            'Welcome to Spelling Bee! (presented by G(J)IFY)\n'
            'To play, simply enter a word using only the letters in the '
            'honey comb (must include the center letter) by either typing '
            'on your keyboard or by clicking on the letters directly.'
        )
        self.instructions.setWordWrap(True)

        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
        )
        self.btns.accepted.connect(self.accept)

        layout.addWidget(self.instructions)
        layout.addWidget(self.btns)

        self.setLayout(layout)



################################################################################
# class WelcomeDialog()
#
# DESCRIPTION
#   Welcome page that can be showed at launch.
################################################################################
class WelcomeDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(WelcomeDialog, self).__init__(parent=None, *args, **kwargs)

        self.message = QLabel(self)
        self.btns = QDialogButtonBox(self)

        self._initUI()

    def _initUI(self):

        layout = QVBoxLayout()

        self.message.setText(
            "Welcome to Spelling Bee!"
            "Would you like to load a game?"
        )
        self.message.setWordWrap(True)

        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.No
            | QDialogButtonBox.StandardButton.Yes
        )

        layout.addWidget(self.message)
        layout.addWidget(self.btns)

        self.setLayout(layout)


class OptionsDialog(QDialog):
    def __init__(self, parent: QWidget):
        super(OptionsDialog, self).__init__(parent)
        self.title = QLabel(self)
        self.backToGameBtn = QPushButton(self)
        self.leaderboardBtn = QPushButton(self)
        self.helpBtn = QPushButton(self)
        self.mainMenuBtn = QPushButton(self)

        self._initUI()
        self._connectSignals()

    def _initUI(self):
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setWindowTitle('Options')

        self.title.setText('Options')
        self.backToGameBtn.setText('Back to game')
        self.backToGameBtn.setFixedSize(180, 40)
        self.leaderboardBtn.setText('Leaderboard')
        self.leaderboardBtn.setFixedSize(180, 40)
        self.helpBtn.setText('Help')
        self.helpBtn.setFixedSize(180, 40)
        self.mainMenuBtn.setText('Quit to Main Menu')
        self.mainMenuBtn.setFixedSize(180, 40)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.backToGameBtn)
        layout.addWidget(self.leaderboardBtn)
        layout.addWidget(self.helpBtn)
        layout.addWidget(self.mainMenuBtn)
        self.setLayout(layout)
        self.setMaximumSize(self.width(), self.height())

    def _connectSignals(self):
        self.backToGameBtn.clicked.connect(self.close)
