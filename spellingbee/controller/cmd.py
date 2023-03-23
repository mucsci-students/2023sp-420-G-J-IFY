from __future__ import annotations
from abc import ABC, abstractmethod

################################################################################
#
################################################################################
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

# Concrete Commands:

################################################################################
#
################################################################################
class NewGame(Command):
    def __init__(self) -> None:
        pass

    def execute(self) -> None:
        return super().execute()