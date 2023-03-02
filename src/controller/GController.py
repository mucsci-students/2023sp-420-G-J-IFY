################################################################################
# GController.py
# AUTHOR: Isaak Weidman, Yah'hymbey Baruti Ali-Bey, Francesco Spagnolo 
# DATE OF CREATION: 2/25/2023
#
# DESCRIPTION:
#   Routes functionality from user-input into backend of the project, then
#   updates the display to reflect those changes.
#
# CLASSES:
# GUIController
#
# FUNCTIONS:
# connectSignals(keySymbol: str, button)
################################################################################

#LaunchSetting() { 
#Ask user for gui or cli 
#While not gui or cli 
    #Print invalid input 
    #If CLI then CLI 
        #Else if GUI then GUI 
        #Else GUI 
#maybe return the setting to somewhere else 
#} 

import sys
import os
from os import path
from functools import partial
from gview.MainWindow import MainWindow
from model import MakePuzzle, StateStorage, output
from model.puzzle import Puzzle
import PyQt6
from PyQt6.QtWidgets import QApplication
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
        
#Global Var



        
        
################################################################################
# connectSignals(keySymbol: str, button)
#
# DESCRIPTION:
#   Connects the buttons to the right actions. Each letter builds a new
#   expression, while the other buttons are connected to their respective
#   functionality.
#
# PARAMETERS:
#  keySymbol : str
#  button : unsure
#  user input as a single character (one at a time)
################################################################################
def connectSignals(puzzle, window, outty):
    dialog = window.newDialog

    baseWord = dialog.baseWrd.text()
    keyLett = dialog.keyLett.currentText()

    # newPuzzle uses default params
    dialog.warningBtns.accepted.connect(newPuzzle)
    # newPuzzle uses provided params
    dialog.advBtns.accepted.connect(lambda: newPuzzle(puzzle, outty,baseWord, keyLett))
    
    window.centralWidget.entrBtn.clicked.connect(lambda: guess(puzzle, outty, window))
    window.centralWidget.uInput.returnPressed.connect(lambda: guess(puzzle, outty, window))
    
    # window.saveDialog.btns.accepted.connect(saveGame)
    
    # window.helpDialog.btns.accepted.connect(help)
    
    window.centralWidget.shflBtn.clicked.connect(lambda: shuffleLetters(puzzle))
    
    window.loadDialog.btns.accepted.connect(lambda: loadGame(puzzle, window))
    
    window.centralWidget.delBtn.clicked.connect(lambda: deleteInput(window))  

################################################################################
# newPuzzle(userInput) -> object:
#
# DESCRIPTION:
#   prompts for input and directs functionality to create a new puzzle object.
#
# RETURN:
#   object
#     - new puzzle object
################################################################################
def newPuzzle(puzzle: Puzzle, outty,baseWord : str = '', keyLetter : str = '') -> None:
    sender = sender().parent
    baseWord = sender.basWrd.text()
    keyLetter = sender.keyLett.currentText()
    out = MakePuzzle.newPuzzle(baseWord, keyLetter, outty, True).shuffleChars()
    puzzle = out
    sender.accept()
################################################################################
# guess(window: object) -> None
#
# DESCRIPTION:
#   Checks the database for valid words, already found words and 
#   words that do not exist
#
# PARAMETERS:
#  window : Obj
#   the GUI window we will be manipulating
################################################################################
def guess(puzzle, outty, window):
    #Connect to text field in view and grab 
    text = window.centralWidget.uInput.text()
    window.centralWidget.uInput.clear()
    MakePuzzle.guess(puzzle, text, True, outty)    
    window.statsPanel.update(puzzle)
    window.setStatusTip(outty.getField())
    print(outty.getField())
################################################################################
# saveGame(Game : object) -> None:
#
# DESCRIPTION:
#   creates a new save entry for the overall status of the game.
#   creates a new save entry for JUST the puzzle data of the game.
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state
################################################################################
def saveGame(puzzle) -> None:
    # Takes file name
    handleSave(puzzle, 0)
    handleSave(puzzle, 1)    
################################################################################
# handleSave(game : object, num) -> None:
#
# DESCRIPTION:
#   saves the games state and handles input from the user to determin if they
#   want to overwrite a file or not
# 
# PARAMETERS:
#   game : object
#     - puzzle object storing current game state
#   num : int
#     - an integer value to determin if we are saving all the game progress
#       or just the pzzle. 0 for saveCurrent() and 1 for savePuzzle().
################################################################################
def handleSave(game : object, fileName: str ,num : int) -> None:
    saveStatus = False
    if(path.isfile(fileName +'.json')):
        # Run Dialog Window for overwriting existing file
        # Change if to check if user click yes or no
        if(True):
            if(num == 0):
                StateStorage.saveCurrent(game, fileName)
                saveStatus = True
            elif(num == 1):
                StateStorage.savePuzzle(game, fileName)
                saveStatus = True
    else: 
        if(num == 0):
            StateStorage.saveCurrent(game, fileName)
            saveStatus = True
        elif(num == 1):
            StateStorage.savePuzzle(game, fileName)
            saveStatus = True
    
        if saveStatus:
            # Run dialog window for successful save
            pass
        else:
            # Run dialog window for failed save
            pass       
################################################################################
# help() -> None
#
# DESCRIPTION:
#   provides a brief description of game rules and generally how to play as well
#   as a list of all available commands.
################################################################################
def help() -> None:
    # Display Game Intructions
    pass
################################################################################
# help() -> None
#
# DESCRIPTION:
#   provides a brief description of game rules and generally how to play as well
#   as a list of all available commands.
################################################################################
def shuffleLetters(puzzle) -> None:
    puzzle.shuffleChars()
################################################################################
# loadGame(game : object) -> None:
#
# DESCRIPTION:
#   load an existing save entry into memory
#
# PARAMETERS:
#   game : object
#     - puzzle object storing the current game state
################################################################################
def loadGame(game : object, window) -> None: 
    sender = sender().parent.uInput.text()
    fileName = sender
    if path.isfile(fileName +'.json'):
        newGame =  StateStorage.loadPuzzle(fileName)
        
        if newGame != None:
            game = newGame
        else:
            window.loadFailed.show()
    else:
        window.loadFailed.show()
################################################################################
# deleteInput() -> None:
#
# DESCRIPTION:
#   deletes char from input field
#
# PARAMETERS:
#   none
################################################################################
def deleteInput(window):
    window.centralWidget.uInput.backspace()


def main():
    outty = output.Output()
    puzzle = MakePuzzle.newPuzzle('','',outty,True)
    app = QApplication([])
    window = MainWindow(puzzle) 
    connectSignals(puzzle, window, outty)
    window.show()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()