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
    
################################################################################
#
################################################################################
class SaveGame(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class LoadGame(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Shuffle(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Help(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Hint(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        return super().execute()
    
################################################################################
#
################################################################################
class Exit(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        return super().execute()