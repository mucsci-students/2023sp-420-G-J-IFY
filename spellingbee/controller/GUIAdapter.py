import cmd
from MainWindow import MainWindow
from puzzle import Puzzle

class GUI_A():

    def __init__(self, puzz: Puzzle):
        window = MainWindow(puzz)

    def start(self):
        pass

    def _connectSignals(self):
        pass

"""
Example of the main module
if __name__ == '__main__':
    flag = True

    if flag:
        app = CLIAdapter.UserInterface()
    else:
        app = GUIAdapter.GUI_A()

    app.start()
"""