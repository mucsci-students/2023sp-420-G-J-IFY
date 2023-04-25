from gview.Leaderboard import Leaderboard
from model.puzzle import Puzzle
from PyQt6 import QtCore
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
        self.scroll_area = QtWidgets.QScrollArea()
        self._score = puzzle.getScore()
        self._rank = puzzle.getRank()
        self._score_lbl = QtWidgets.QLabel()
        self._rank_lbl = QtWidgets.QLabel()
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
        self.leader_board.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )
        self.scroll_area.setWidget(self.leader_board)
        self.scroll_area.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter |
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        layout.addWidget(self.scroll_area)

        # Current Score
        lbl = QtWidgets.QLabel()
        lbl.setText("Your Score")
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        # Score layout
        hlayout = QtWidgets.QHBoxLayout()
        self._score_lbl = QtWidgets.QLabel()
        self._score_lbl.setText(f"Score: {self._score}")
        self._score_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(self._score_lbl)

        # Rank Layout
        self._rank_lbl = QtWidgets.QLabel()
        self._rank_lbl.setText(f"Rank: {self._rank}")
        self._rank_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(self._rank_lbl)
        layout.addLayout(hlayout)

        out.setLayout(layout)

        return out

    ###########################################################################
    # _updateLeaderboard(newlb: list[tuple]) -> None
    #
    # DESCRIPTION
    #   updates the shown leaderboard
    ###########################################################################
    def _updateLeaderboard(self, newlb: list[tuple], puzzle: Puzzle) -> None:
        self.leader_board = Leaderboard(self, newlb)
        self.leader_board.update()
        self._score_lbl.setText(str(puzzle.getScore()))
        self._rank_lbl.setText(puzzle.getRank())
        self.scroll_area.setWidget(self.leader_board)
