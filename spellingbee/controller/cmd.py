from __future__ import annotations
from abc import ABC, abstractmethod

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
        self.name = None
        self.description = None

    @abstractmethod
    def execute(self) -> None:
        print("implementation pending")


# Concrete Commands:
################################################################################
#
################################################################################
class NewGame(Command):
    def __init__(self) -> None:
        self.name = '!new'
        self.description = 'Description Pending'

    def execute(self, word: str, keyLett: str, puzzle: Puzzle) -> None:
        puzzle = MakePuzzle.newPuzzle(baseWord=word, keyLetter=keyLett)
        puzzle.shuffleChars()
        return puzzle
    
################################################################################
#
################################################################################
class SaveGame(Command):
    def __init__(self) -> None:
        self.name = '!save'
        self.description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class SavePuzzle(Command):
    def __init__(self) -> None:
        self.name = '!save-puzzle'
        self.description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class LoadGame(Command):
    def __init__(self) -> None:
        self.name = '!load'
        self.description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Shuffle(Command):
    def __init__(self) -> None:
        self.name = '!shuffle'
        self.description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Help(Command):
    def __init__(self) -> None:
        self.name = '!help'
        self.description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Hint(Command):
    def __init__(self) -> None:
        self.name = '!hint'
        self.description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Exit(Command):
    def __init__(self) -> None:
        self.name = '!exit'
        self.description = 'Description Pending'

    def execute(self) -> None:
        return super().execute()