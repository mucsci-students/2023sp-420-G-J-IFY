from __future__ import annotations
from abc import ABC, abstractmethod
import sys

from model import(
    MakePuzzle,
    output,
    StateStorage
)
from model.puzzle import Puzzle

################################################################################
#
################################################################################
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
################################################################################
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
################################################################################
class NewGame(Command):
    def __init__(self, outty: object, base: str='', keyLett: str='') -> None:
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
    
################################################################################
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
################################################################################
class SaveGame(Command):
    def __init__(
            self,
            puzzle: Puzzle,
            fileName: str,
            path: str='./saves',
            onlyPuzz: bool=False
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

'''   
################################################################################
#
################################################################################
class SavePuzzle(Command):
    def __init__(self) -> None:
        self._name = '!save-puzzle'
        self._description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
    # Returns information about the command
    def get_name(self) -> str:
        return self._name
    
    def get_description(self) -> str:
        return self._description

'''
    
################################################################################
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
################################################################################
class LoadGame(Command):
    def __init__(self, path: str) -> None:
        self._name = '!load'
        self._description = 'Load a previously saved game'

        # params
        self._path = path

    def execute(self) -> None:
        StateStorage.loadFromExploer(self._path)
    
################################################################################
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
################################################################################
class Shuffle(Command):
    def __init__(self, receiver: Puzzle) -> None:
        self._name = '!shuffle'
        self._description = (
            'Shuffle the order of the active puzzle for a fresh view'
        )
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.shuffleChars()
    
################################################################################
#
################################################################################
class Help(Command):
    def __init__(self) -> None:
        self._name = '!help'
        self._description = (
            "Show the list of all available commands with a brief description. "
            "(You're here now!)"
        )

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Hint(Command):
    def __init__(self) -> None:
        self._name = '!hint'
        self._description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Exit(Command):
    def __init__(self) -> None:
        self._name = '!exit'
        self._description = 'Exit the game'

    def execute(self) -> None:
        sys.exit()
    

################################################################################
#
################################################################################
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
            flag=False,
            outty=None
        )