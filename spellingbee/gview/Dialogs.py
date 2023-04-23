import os
from PyQt6.QtCore import (
    Qt,
    QRegularExpression,
)
from PyQt6.QtGui import (
    QFont,
    QRegularExpressionValidator,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QWidget,
    QDialog,
    QSizePolicy,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QDialogButtonBox,
    QComboBox,
    QStyle,
    QFileDialog,
)


##############################################################################
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
##############################################################################
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
        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Open
        )
        # acceptance event must be handled by controller. Rejection follows
        # standard rejection procedure.
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.uInput)
        layout.addWidget(self.btns)
        self.setLayout(layout)


##############################################################################
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
##############################################################################
class LoadFailedDialog(QDialog):
    def __init__(self, parent: QWidget, *args, **kwargs):
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
        self.baseWrd = QLineEdit(self)
        self.keyLett = QComboBox(self)
        self.btns = QDialogButtonBox(self)
        # initialize display
        self._initUI()

    ##########################################################################
    # _initUI() -> None
    ##########################################################################
    def _initUI(self) -> None:
        layout = QVBoxLayout()
        # Create pages
        advanced = self._initAdvNewPage()
        # Add pages to stack
        layout.addWidget(advanced)
        # Set standard buttons
        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        # Acceptance must but defined in controller
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)
        self.setLayout(layout)

    ##########################################################################
    # _initAdvNewPage() -> QWidget
    ##########################################################################
    def _initAdvNewPage(self) -> QWidget:
        # Create page attributes
        page = QWidget(self)
        layout = QVBoxLayout()
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
        form.addRow('Baseword:', self.baseWrd)
        form.addRow('Key Letter:', self.keyLett)
        layout.addLayout(form)
        page.setLayout(layout)
        return page

    ##########################################################################
    # _populateCombo(word : str) -> None
    ##########################################################################
    def _populateCombo(self, word: str) -> None:
        self.keyLett.clear()
        uniqueLett = list(set(word))
        for lett in uniqueLett:
            self.keyLett.addItem(lett.upper())

    ##########################################################################
    # reject() -> None
    ##########################################################################
    def reject(self) -> None:
        self.baseWrd.clear()
        self.keyLett.clear()
        super().reject()

    ##########################################################################
    # accept() -> None
    ##########################################################################
    def accept(self) -> None:
        self.baseWrd.clear()
        self.keyLett.clear()
        super().accept()


##############################################################################
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
##############################################################################
class SaveDialog(QDialog):
    def __init__(self, parent: QWidget | None, *args, **kwargs):
        super(SaveDialog, self).__init__(parent, *args, **kwargs)

        # Dialog is persistent
        self.setModal(True)
        # Declare attributes/widgets
        self.fileName = QLineEdit(self)
        self.justPuzzle = QCheckBox(self)
        self.encrypt = QCheckBox(self)
        self.btns = QDialogButtonBox(self)

        # initialize widgets and build ui
        self._initUI()

    ###########################################################################
    # _initUI() -> None
    #
    # DESCRIPTION:
    #   initializes widget data and populates dialog with them
    ###########################################################################
    def _initUI(self):
        layout = QVBoxLayout()
        # Add labels to checkboxes
        self.justPuzzle.setText('Save blank puzzle')
        self.encrypt.setText('Encrypt words list')
        # Initialize fileName with default path and name
        self.fileName.setText(f'{os.getcwd()}/untitled.json')
        # Add button at end of fileName to open file dialog
        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogOpenButton
        )
        self._open_dlg_action = self.fileName.addAction(
            icon,
            QLineEdit.ActionPosition.TrailingPosition
        )
        self._open_dlg_action.triggered.connect(self._open)
        # Add save and cancel buttons
        self.btns.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Save
        )
        # Connect cacel button to default rejection (save is user defined)
        self.btns.rejected.connect(self.reject)
        # Populate dialog with widgets
        layout.addWidget(self.justPuzzle)
        layout.addWidget(self.encrypt)
        layout.addWidget(self.fileName)
        layout.addWidget(self.btns)
        self.setLayout(layout)

    ###########################################################################
    # _validatePath(self, str) -> bool:
    #
    # DESCRIPTION:
    #   private function that returns true if path exists and file name ends
    #   with '.json'
    ###########################################################################
    def _validatePath(self, str) -> bool:
        return self.getPath().endswith('.json')

    ###########################################################################
    # _open() -> None
    #
    # DESCRIPTION:
    #   private function that opens a file dialog and returns path + user
    #   defined filename
    ###########################################################################
    def _open(self) -> None:
        path = QFileDialog.getSaveFileName(
            self,
            'Save Game',
            os.getcwd(),
            "Game Files (*.json)"
        )
        self.fileName.setText(path[0])

    ###########################################################################
    # isOnlyPuzzle() -> bool
    #
    # DESCRIPTION:
    #   returns true if user checked 'save puzzle only' option, otherwise false
    ###########################################################################
    def isOnlyPuzzle(self) -> bool:
        return self.justPuzzle.isChecked()

    ###########################################################################
    # isEncrypted() -> bool
    #
    # DESCRIPTION:
    #   returns true if user checked 'encrypt word list' option, otherwise
    #   false
    ###########################################################################
    def isEncrypted(self) -> bool:
        return self.encrypt.isChecked()

    ###########################################################################
    # getPath() -> str
    #
    # DESCRIPTION:
    #   returns the full path to the new file to be saved
    ###########################################################################
    def getPath(self) -> str:
        return self.fileName.text()

    def reset(self) -> None:
        self.justPuzzle.setChecked(False)
        self.encrypt.setChecked(False)
        self.fileName.setText(f'{os.getcwd()}/untitled.json')


##############################################################################
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
##############################################################################
class SaveOverwriteDialog(QDialog):
    def __init__(self, parent: QWidget | None, *args, **kwargs):
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


##############################################################################
# class HelpDialog()
#
# DESCRIPTION
#   Gives the user a breif overview of the game and how its played.
##############################################################################
class HelpDialog(QDialog):
    def __init__(self, parent: QWidget | None, *args, **kwargs):
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


##############################################################################
# class OptionsDialog()
#
# DESCRIPTION
#   Provides a list of options the user can use to control the application
##############################################################################
class OptionsDialog(QDialog):
    def __init__(self, parent: QWidget):
        super(OptionsDialog, self).__init__(parent)
        self.title = QLabel(self)
        self.backToGameBtn = QPushButton(self)
        self.leaderboardBtn = QPushButton(self)
        self.helpBtn = QPushButton(self)
        self.shareBtn = QPushButton(self)
        self.mainMenuBtn = QPushButton(self)
        self._initUI()

    ##########################################################################
    # _initUI(self)
    #
    # DESCRIPTION:
    #   initialize ui components
    ##########################################################################
    def _initUI(self):
        # Set style sheet
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())
        # Set size policy
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        # Set basic window properties
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setWindowTitle('Options')
        # initialize components
        self.title.setText('Options')
        self.backToGameBtn.setText('Back to game')
        self.backToGameBtn.setFixedSize(180, 40)
        self.leaderboardBtn.setText('Leaderboard')
        self.leaderboardBtn.setFixedSize(180, 40)
        self.helpBtn.setText('Help')
        self.helpBtn.setFixedSize(180, 40)
        self.shareBtn.setText('Share')
        self.shareBtn.setFixedSize(180, 40)
        self.mainMenuBtn.setText('Save and quit')
        self.mainMenuBtn.setFixedSize(180, 40)
        # Populate the widget
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.backToGameBtn)
        layout.addWidget(self.leaderboardBtn)
        layout.addWidget(self.helpBtn)
        layout.addWidget(self.shareBtn)
        layout.addWidget(self.mainMenuBtn)
        self.setLayout(layout)
        self.setMaximumSize(self.width(), self.height())
        # Connect close button
        self.backToGameBtn.clicked.connect(self.close)


##############################################################################
# class ShareDialog(QDialog):
#
# DESCRIPTION:
#   shows user a preview of an image that displays the current hive, score,
#   and rank. User is given the option to choose a save location. Otherwise,
#   screenshot is saved to desktop.
##############################################################################
class ShareDialog(QDialog):

    ##########################################################################
    # __init__()
    ##########################################################################
    def __init__(self, parent: QWidget | None, score: QPixmap, hive: QPixmap):
        super(ShareDialog, self).__init__(parent)
        # Declare attributes
        self._image = self._buildOutWidget(score, hive)
        self._path = QLineEdit()
        self._btns = QDialogButtonBox()

        self._initUI()

    ##########################################################################
    # _initUI() -> None:
    #
    # DESCRIPTION:
    #   initialize UI components
    ##########################################################################
    def _initUI(self) -> None:
        self.setModal(True)
        # Define layout:
        v_layout = QVBoxLayout()
        # Initialize Attributes and add to layout (top to bottom)
        # Format image preview
        self._image.setStyleSheet(
            '''
            border: 1px solid;
            border-color: rgb(210, 210, 210);
            border-radius: 15px;
            '''
        )
        v_layout.addWidget(self._image)
        # Filepath
        # Default path is ~/user/Desktop. File will be saved as untitled.png
        # unless otherwise specified
        self._buildPathInput()
        v_layout.addWidget(
            self._path,
            Qt.AlignmentFlag.AlignCenter
        )
        # Buttons
        self._btns.addButton('Share', QDialogButtonBox.ButtonRole.AcceptRole)
        self._btns.addButton(QDialogButtonBox.StandardButton.Cancel)
        v_layout.addWidget(self._btns)
        # Apply layout
        self.setLayout(v_layout)
        # Connections
        self._btns.accepted.connect(self.accept)
        self._btns.rejected.connect(self.reject)

    ##########################################################################
    # _buildOutWidget(score: QPixmap, hive: QPixmap) -> QWidget
    #
    # DESCRIPTION:
    #   arranges the two pixmaps proveded on object creation into a sinlgle
    #   QWidget object. This allows for exporting the new Widgets pixmap to
    #   be saved later.
    #
    # PARAMS:
    #   score: QPixmap
    #     - Image with the users current rank, progress bar, score and score
    #       to rankup
    #   hive: QPixmap
    #     - Image with the hex cluster of buttons used during currently
    #       active game
    #
    # RETURN:
    #   QWidget
    #     - The arranged widget that can be displayed to user before export
    ##########################################################################
    def _buildOutWidget(self, score: QPixmap, hive: QPixmap) -> QWidget:
        # Define local attributes
        v_layout = QVBoxLayout()
        score_display = QLabel()
        hive_display = QLabel()
        # Add pixmaps to widgets
        score_display.setPixmap(score)
        hive_display.setPixmap(hive)
        # Remove style sheet
        score_display.setStyleSheet('border: none;')
        hive_display.setStyleSheet('border: none;')
        # Populate layout
        v_layout.addWidget(
            score_display,
            Qt.AlignmentFlag.AlignCenter
        )
        v_layout.addWidget(
            hive_display,
            Qt.AlignmentFlag.AlignCenter
        )
        # Create widget and return
        out = QWidget()
        out.setLayout(v_layout)
        return out

    ##########################################################################
    # _buildPathInput() -> None:
    #
    # DESCRIPTION:
    #   Initializes the file path text input widget with a default path,
    #   and a button that opens a file dialog
    ##########################################################################
    def _buildPathInput(self) -> None:
        # Default path is as follows:
        #   MacOS:      ~/Users/<username>/Desktop/untitled.png
        #   Windows:    ~/
        #   Linux:      ~/
        default_path = f"{os.path.expanduser('~')}/Desktop/untitled.png"
        self._path.setText(default_path)
        # Create Icon for action
        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogOpenButton
        )
        # Add action to open file dialog
        file_dlg_action = self._path.addAction(
            icon,
            self._path.ActionPosition.TrailingPosition
        )
        file_dlg_action.triggered.connect(self._getSaveFilePath)

    ##########################################################################
    # _getSaveFilePath() -> None
    #
    # DESCRIPTION
    #   Opens a file dialog and sets _path's text to the user's chosen
    #   location and filename. By default, dialog opens at Desktop folder.
    ##########################################################################
    def _getSaveFilePath(self) -> None:
        # store tuple returned from file dialog
        f_path = QFileDialog.getSaveFileName(
            caption="Save Screenshot",
            directory=self._path.text(),
            filter='Image Files (*.PNG)'
        )
        # set _paths text to the first index of the tuple, which is the path
        self._path.setText(f_path[0])

    ##########################################################################
    # _captureScreenshot() -> QPixmap
    #
    # DESCRIPTION:
    #   overts outWidget into a pixmap to be exported
    #
    # RETURN:
    #   QPixmap
    #     - An image of the outwidget
    ##########################################################################
    def _captureScreenshot(self) -> QPixmap:
        self._image.setStyleSheet('border: none;')
        image = self._image.grab()
        return image

    ##########################################################################
    # accept() -> None
    #
    # DESCRIPTION:
    #   saves the result of _captureScreenshot as a .png image at the
    #   specified file path, with the specified file name.
    ##########################################################################
    def accept(self):
        # Fetch file path
        file_path = self._path.displayText()
        # Capture screenshot and save file
        self._captureScreenshot().save(file_path, 'PNG')
        # continue with standard accept procedure
        super().accept()


##############################################################################
# QueenBeeDialog(QDialog)
#
# DESCRIPTION:
#   opens when the player has finished a game. User is provided two options.
#     they can either end the game, or they can share their score, then end
#     the game.
##############################################################################
class QueenBeeDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super(QueenBeeDialog, self).__init__(parent)

        self._message = QLabel(self)
        self._buttons = QDialogButtonBox(self)
        self._closeBtn = QPushButton(self)
        self._shareBtn = QPushButton(self)

        self.__initUI()

    def __initUI(self):
        self.setModal(True)
        self._message.setText(
            'Congratulations!\n'
            'You are the Queen Bee!'
        )
        # initialize dialog buttons
        self._shareBtn.setText('Share')
        self._buttons.addButton(
            self._shareBtn,
            QDialogButtonBox.ButtonRole.ActionRole
        )
        self._closeBtn.setText('Close')
        self._buttons.addButton(
            self._closeBtn,
            QDialogButtonBox.ButtonRole.AcceptRole
        )

        layout = QVBoxLayout()
        layout.addWidget(self._message)
        layout.addWidget(self._buttons)
        self.setLayout(layout)
