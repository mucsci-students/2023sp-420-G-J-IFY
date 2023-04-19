from __future__ import annotations
from abc import ABC, abstractmethod
import os

from model import (
    MakePuzzle,
    StateStorage
)
from model.puzzle import Puzzle
from model.hint import hint
from model.output import Output
from model import highScore

outty = Output.getInstance()
##############################################################################
#
##############################################################################


class Command(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self._name = None
        self._description = None

    @abstractmethod
    def execute(self) -> None:
        pass

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description


# Concrete Commands:
##############################################################################
# class NewGame(Command):
#
# DESCRIPTION:
#   Executes the required code in model to create a new puzzle object.
# ARGUMENTS:
#
# ATTRIBUTES:
#
# FUNCTIONS:
#
###############################################################################
class NewGame(Command):
    def __init__(self,
                 base: str = '',
                 keyLett: str = '') -> None:
        self._name = '!new'
        self._description = (
            'Generates a new puzzle from a base word with exactly 7 unique'
            'characters or an auto-generated base word.'
        )
        self._base = base
        self._keyLett = keyLett

    # Executes defined function
    def execute(self) -> Puzzle:
        puzzle = MakePuzzle.newPuzzle(
            baseWord=self._base,
            keyLetter=self._keyLett,
            flag=False
        )
        puzzle.shuffleChars()
        return puzzle


###############################################################################
# class SaveGame(Command)
#
# DESCRIPTION:
#
# ARGUMENTS:
#
# ATTRIBUTES:
#
# FUNCTIONS:
#
###############################################################################
class SaveGame(Command):
    def __init__(
        self,
        puzzle: Puzzle,
        path: str,
        onlyPuzz: bool,
        encrypt: bool
    ) -> None:

        self._name = '!save'
        self._description = 'Create a new save for the currently active game'

        # params
        self._puzzle = puzzle
        self._fileName = os.path.basename(path)
        self._path = os.path.dirname(path)
        self._onlyPuzz = onlyPuzz

    def execute(self) -> None:

        # pass responsibility off to State Storage
        StateStorage.saveFromExplorer(
            path=self._path,
            fileName=self._fileName,
            puzzle=self._puzzle,
            onlyPuzz=self._onlyPuzz
        )

    def executeCLIPuzzle(self) -> None:
        StateStorage.savePuzzle(self._puzzle, self._fileName)

    def exceuteCLICurrent(self) -> None:
        StateStorage.saveCurrent(self._puzzle, self._fileName)

###############################################################################
# class LoadGame(Command)
#
# DESCRIPTION:
#
# ARGUMENTS:
#
# ATTRIBUTES:
#
# FUNCTIONS:
#
###############################################################################


class LoadGame(Command):
    def __init__(self, path: str, fileName) -> None:
        self._name = '!load'
        self._description = 'Load a previously saved game'

        # params
        self._path = path
        self._fileName = fileName

    def execute(self) -> object:
        return StateStorage.loadFromExploer(self._path)

    def executeCLI(self) -> object:
        return StateStorage.loadPuzzle(self._fileName)


###############################################################################
# class Shuffle(Command)
#
# DESCRIPTION:
#
# ARGUMENTS:
#
# ATTRIBUTES:
#
# FUNCTIONS:
#
###############################################################################


class Shuffle(Command):
    def __init__(self, receiver: Puzzle) -> None:
        self._name = '!shuffle'
        self._description = (
            'Shuffle the order of the active puzzle for a fresh view'
        )
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.shuffleChars()

###############################################################################
# class Hint(Command):
#
# DESCRIPTION:
#
# ARGUMENTS:
#
# ATTRIBUTES:
#
# FUNCTIONS:
#
###############################################################################


class Hint(Command):
    def __init__(self, puzzle: object) -> None:
        self._name = '!hint'
        self._description = (
            "Show show data from the current game to help user make a guess"
        )

        # params
        self._puzzle = puzzle

    def execute(self) -> dict:
        hints = hint(self._puzzle)
        hints.makeHintGrid(self._puzzle)
        hints.twoLetterList(self._puzzle)

        shuffleLetts = self._puzzle.getShuffleLetters()
        keyLett = shuffleLetts[0].upper()
        rest = ' '.join(shuffleLetts[1: len(shuffleLetts)]).upper()

        return {
            'letters': f'\u0332{keyLett}\u0332 {rest}',
            'numWords': hints.countWords(self._puzzle),
            'points': self._puzzle.maxScore,
            'numPan': hints.numPangrams(self._puzzle),
            'numPerf': hints.numPerfectPangram(self._puzzle),
            'bingo': self._puzzle.checkBingo(),
            'matrix': hints.getHintGrid(),
            'twoLetLst': hints.getTwoLetterList()
        }


###############################################################################
# class Guess(Command)
#
# DESCRIPTION:
#   Submits a guess to the model
#
# ARGUMENTS:
#   puzzle: Puzzle
#       the object representing the currently running game
#   word: str
#       the word to be submitted as a guess
#   outty: object
#       the output object
#
# FUNCTIONS:
#   execute() -> None:
#       exectutes the attached function call to make a guess
###############################################################################
class Guess(Command):
    def __init__(self, puzzle: Puzzle, word: str) -> None:
        self._name = '!guess'
        self._description = 'description pending'

        # params
        self._puzzle = puzzle
        self._word = word

    def execute(self) -> None:
        MakePuzzle.guess(
            puzzle=self._puzzle,
            input=self._word,
            flag=False
        )


###############################################################################
# class Leaderboard(Command)
#
# DESCRIPTION
#   returns the leaderboard for this game
###############################################################################
class Leaderboard(Command):
    def __init__(self, puzzle: Puzzle) -> None:
        self._puzzle = puzzle

    def execute(self) -> list[tuple]:
        # grab hS
        # format to list of [(name, rank, score)]
        lst = highScore.getHighScore(
            self._puzzle.getUniqueLetters(),
            self._puzzle.getKeyLetter()
        )
        lb = []
        for row in lst:
            lb.append((row[1], row[2], row[3]))

        return lb


###############################################################################
# SaveScore(name: str, puzzle: Puzzle)
#
# DESCRIPTION
#   adds a new high score to the database
###############################################################################
class SaveScore(Command):
    def __init__(self, name: str, puzzle: Puzzle) -> None:
        self._name = name
        self._rank = puzzle.getRank()
        self._score = puzzle.getScore()
        self._uniqueLett = puzzle.getUniqueLetters()
        self._keyLett = puzzle.getKeyLetter()

    def execute(self) -> None:
        highScore.qualify(
            self._name,
            self._rank,
            self._score,
            self._uniqueLett,
            self._keyLett
        )
