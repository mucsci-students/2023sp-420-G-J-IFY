from __future__ import annotations
from abc import ABC, abstractmethod

from model import (
    MakePuzzle,
    StateStorage
)
from model.puzzle import Puzzle
from model.hint import hint

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
        print("implementation pending")

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
    def __init__(self, outty: object, base: str = '',
                 keyLett: str = '') -> None:
        self._name = '!new'
        self._description = (
            'Generates a new puzzle from a base word with exactly 7 unique'
            'characters or an auto-generated base word.'
        )
        self._base = base
        self._keyLett = keyLett
        self._outty = outty

    # Executes defined function
    def execute(self) -> Puzzle:
        puzzle = MakePuzzle.newPuzzle(
            baseWord=self._base,
            keyLetter=self._keyLett,
            outty=self._outty,
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
            fileName: str,
            path: str = './saves',
            onlyPuzz: bool = False
            ) -> None:

        self._name = '!save'
        self._description = 'Create a new save for the currently active game'

        # params
        self._puzzle = puzzle
        self._fileName = fileName
        self._path = path
        self._onlyPuzz = onlyPuzz

    def execute(self) -> None:

        # pass responsibility off to State Storage
        StateStorage.saveFromExplorer(
            path=self._path,
            fileName=self._fileName,
            puzzle=self._puzzle,
            onlyPuzz=self._onlyPuzz
        )

    def executeCLI(self) -> None:
        StateStorage.savePuzzle(self._puzzle, self._fileName)

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
    def __init__(self, path: str, fileName, outty: object) -> None:
        self._name = '!load'
        self._description = 'Load a previously saved game'

        # params
        self._path = path
        self._outty = outty
        self._fileName = fileName

    def execute(self) -> object:
        return StateStorage.loadFromExploer(self._path, self._outty)

    def executeCLI(self) -> object:
        return StateStorage.loadPuzzle(self._fileName, self._outty)

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
    def __init__(self, puzzle: Puzzle, word: str, outty: object) -> None:
        self._name = '!guess'
        self._description = 'description pending'

        # params
        self._puzzle = puzzle
        self._word = word
        self._outty = outty

    def execute(self) -> None:
        MakePuzzle.guess(
            puzzle=self._puzzle,
            input=self._word,
            flag=False,
            outty=self._outty
        )
