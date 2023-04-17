from gview.Leaderboard import Leaderboard
from model.puzzle import Puzzle
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets


###############################################################################
# WrapUpPage(parent: QWidget = None)
#
# DESCRIPTION:
#   Displays information about the user's session after they leave the game
###############################################################################
class WrapUpPage(QtWidgets.QWidget):

    ###########################################################################
    # __init__(parent: QWidget = None, leaderboard: list[tuple])
    #
    # DESCRIPTION:
    #   declares widget's attributes and calles any necessary helper functions
    #
    # PARAMS:
    #   parent: QWidget = None
    #     - This widget's parent widget. Defaults to None if it is the main
    #       window.
    #   puzzle: Puzzle = None
    #     - the puzzle object for currently active game
    #   leaderboard: list[tuple] = []
    #     - The leaderboard saved for this particular game.
    ###########################################################################
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        puzzle: Puzzle = None,
        leaderboard: list[tuple] = []
    ) -> None:
        super(WrapUpPage, self).__init__(parent)

        # Declare attributes
        self.congrats = QtWidgets.QInputDialog(self)
        self.leader_board = Leaderboard(self, leaderboard)
        self._score = 78
        self._rank = 'beginner'
        self.save_btn = QtWidgets.QPushButton()
        self.exit_btn = QtWidgets.QPushButton()

        self._initUI()

    ###########################################################################
    # _initUI() -> None:
    #
    # DESCRIPTION:
    #   initialize widget's UI
    ###########################################################################
    def _initUI(self) -> None:
        # Apply style sheet
        with open("spellingbee/gview/style.css", "r") as file:
            self.setStyleSheet(file.read())

        # Initialize congrats dialog
        self.congrats.setLabelText(
            "Congrats! You made the top 10!\n"
            "Enter a name for the Leaderboard!"
        )
        self.congrats.setModal(True)

        # Build layout
        layout = QtWidgets.QHBoxLayout()

        # Format left side widget
        lb_widget = self._buildLeaderboard()
        layout.addWidget(lb_widget)

        # Format right side widget
        vlayout = QtWidgets.QVBoxLayout()

        # Save_btn
        self.save_btn.setText("Save and Exit")
        self.save_btn.setFixedSize(200, 45)
        vlayout.addWidget(self.save_btn)
        vlayout.setAlignment(
            self.save_btn,
            QtCore.Qt.AlignmentFlag.AlignBottom
        )

        # exit_btn
        self.exit_btn.setText("Exit Without Saving")
        self.exit_btn.setFixedSize(200, 45)
        vlayout.addWidget(self.exit_btn)
        vlayout.setAlignment(
            self.exit_btn,
            QtCore.Qt.AlignmentFlag.AlignTop
        )

        layout.addLayout(vlayout)

        self.setLayout(layout)

    ###########################################################################
    # _buildLeaderboard() -> QWidget
    #
    # DESCRIPTION
    #   Builds the leaderboard side of the widget
    ###########################################################################
    def _buildLeaderboard(self) -> QtWidgets.QWidget:
        out = QtWidgets.QWidget()

        # Build layout
        layout = QtWidgets.QVBoxLayout()

        # Leaderboard layout
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(self.leader_board)
        scroll_area.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter |
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        layout.addWidget(scroll_area)

        # Current Score
        lbl = QtWidgets.QLabel()
        lbl.setText("Your Score")
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        # Score layout
        hlayout = QtWidgets.QHBoxLayout()
        score_lbl = QtWidgets.QLabel()
        score_lbl.setText(f"Score: {self._score}")
        score_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(score_lbl)

        # Rank Layout
        rank_lbl = QtWidgets.QLabel()
        rank_lbl.setText(f"Rank: {self._rank}")
        rank_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(rank_lbl)
        layout.addLayout(hlayout)

        out.setLayout(layout)

        return out

    ###########################################################################
    # _updateLeaderboard(newlb: list[tuple]) -> None
    #
    # DESCRIPTION
    #   updates the shown leaderboard
    ###########################################################################
    def _updateLeaderboard(self, newlb: list[tuple]) -> None:
        self.leader_board = Leaderboard(self, newlb)
