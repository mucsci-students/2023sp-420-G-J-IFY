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
from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QApplication, QFileDialog
from tkinter import filedialog as fd
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
        
#Global Var

        
class GController():

    def __init__(self):

        self.outty = output.Output()
        self.puzzle = MakePuzzle.newPuzzle('', '', self.outty, True)
        self.puzzle.shuffleChars()
        self.window = MainWindow(self.puzzle)
        self.window.show()

        self.connectSignals()


    ############################################################################
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
    ############################################################################
    def connectSignals(self):
        '''
        # newPuzzle uses default params
        newDlg.warningBtns.accepted.connect(
            lambda: self.newPuzzle('', '')
        )
        '''

        # newPuzzle uses provided params
        self.window.newDialog.btns.accepted.connect(self.newPuzzle)
        
        self.window.centralWidget.entrBtn.clicked.connect(self.guess)
        self.window.centralWidget.uInput.returnPressed.connect(self.guess)
        
        self.window.saveDialog.btns.accepted.connect(self.saveGame)
        
        #self.window.helpDialog.btns.accepted.connect()
        
        self.window.centralWidget.shflBtn.clicked.connect(self.shuffleLetters)
        
        #self.window.loadDialog.accepted.connect(self.loadGame)
        
        self.window.centralWidget.delBtn.clicked.connect(self.deleteInput)  

        self.window.loadAction.triggered.connect(self.loadGame)
        

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
    def newPuzzle(self) -> None:
        dlg = self.window.newDialog
        baseWord = str(dlg.baseWrd.text()).lower()
        keyLetter = str(dlg.keyLett.currentText()).lower()
        print(f'\nBaseword: {baseWord}\n KeyLetter: {keyLetter}\n')
        self.puzzle = MakePuzzle.newPuzzle(baseWord, keyLetter, self.outty, True)
        self.puzzle.shuffleChars()
        self.window.newGame(self.puzzle)
        dlg.baseWrd.clear()
        dlg.accept()
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
    def guess(self):
        self.window.setStatusTip('')
        #Connect to text field in view and grab 
        text = self.window.centralWidget.uInput.text()
        self.window.centralWidget.uInput.clear()
        MakePuzzle.guess(self.puzzle, text, True, self.outty)    
        self.window.statsPanel.update(self.puzzle)
        self.window.setStatusTip(self.outty.getField())
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
    def saveGame(self) -> None:
        # Takes file name
        dialog = self.window.saveDialog
        fileName = dialog.fileName.text()
        
        if dialog.justPuzzle.isChecked():
            self.handleSave(self.puzzle, fileName, 1)
        else: 
            self.handleSave(self.puzzle, fileName, 0)   

        dialog.accept() 
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
    def handleSave(self, game : object, fileName: str ,num : int) -> None:
        saveStatus = False
        self.window.saveDialog.fileName.clear()
        self.window.saveDialog.justPuzzle.setChecked(False)
        os.chdir('./src/data/saves')
        if(path.isfile(fileName +'.json')):
            # Run Dialog Window for overwriting existing file
            # Change if to check if user click yes or no
            self.window.owDialog.show()
            self.window.owDialog.btns.accepted.connect(lambda: self.toOverwrite(num, game, fileName))
            
        else: 
            if(num == 0):
                StateStorage.saveCurrent(game, fileName)
                saveStatus = True
            elif(num == 1):
                StateStorage.savePuzzle(game, fileName)
                saveStatus = True
        
        StateStorage.move3dirBack()
        #    if saveStatus:
                # Run dialog window for successful save
        #        pass
        #    else:
                # Run dialog window for failed save
        #        pass       
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
    # shuffleLetters() -> None
    #
    # DESCRIPTION:
    #   Shuffles the letters in the GUI View
    ################################################################################
    def shuffleLetters(self) -> None:
        centralWidget = self.window.centralWidget
        self.puzzle.shuffleChars()
        letters = [*self.puzzle.getShuffleLetters().upper()]
        centralWidget.setLetters(letters)
        centralWidget.update()
    ################################################################################
    # loadGame() -> None:
    #
    # DESCRIPTION:
    #   load an existing save entry into memory
    #
    # PARAMETERS:
    # 
    ################################################################################
    def loadGame(self) -> None:
        '''
        fileName = self.window.loadDialog.uInput.text()
        os.chdir('./src/data/saves')
        if path.isfile(fileName +'.json'):
            newGame =  StateStorage.loadPuzzle(fileName, self.outty)
            
            if newGame != None:
                self.puzzle = newGame
            else:
                self.window.loadFailed.show()
        else:
            self.window.loadFailed.show()
        StateStorage.move3dirBack()
        '''
        fileName = QFileDialog.getOpenFileName(self.window, 'File')[0]
        
        newPuzzle = StateStorage.loadFromExploer(fileName, self.outty)
        if newPuzzle == None:
            self.window.loadFailed.show()
        else:
            self.puzzle = newPuzzle
            self.window.newGame(self.puzzle)
    ################################################################################
    # deleteInput() -> None:
    #
    # DESCRIPTION:
    #   deletes char from input field
    #
    # PARAMETERS:
    #   none
    ################################################################################
    def deleteInput(self):
        self.window.centralWidget.uInput.backspace()
    ################################################################################
    # toOverwrite() -> None:
    #
    # DESCRIPTION:
    #   completes save overwrite
    #
    # PARAMETERS:
    #   none
    ################################################################################
    def toOverwrite(self, num, game, fileName):
        if(num == 0):
            StateStorage.saveCurrent(game, fileName)
            saveStatus = True
        elif(num == 1):
            StateStorage.savePuzzle(game, fileName)
            saveStatus = True
        self.window.owDialog.accept()

################################################################################
# openExplorer() -> None:
#
# DESCRIPTION:
#  opens the file explorer and returns the path to the selected file
#
# PARAMETERS:
#   none
# RETURNS:
#   filePath  
#       the path to the file selected

################################################################################
def openExplorer() -> path:
    filetypes = (
        ('textFiles', '*.json'),
        ('All files' , '*.*')
        )

    filePath = fd.askopenfilename(
            title = 'open a file',
            initialdir= '/',
            filetypes =filetypes)
    return filePath


def main():
    outty = output.Output()
    app = QApplication([])
    control = GController()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()