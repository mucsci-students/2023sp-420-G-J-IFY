################################################################################
# GController.py
# AUTHOR: Francesco Spagnolo, Yah'hymbey
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
# connectSignals(self, keySymbol: str, button)
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
from functools import partial
from gview import SimpleBCluster
from model import MakePuzzle, StateStorage
import PyQt6
from PyQt6.QtWidgets import QApplication
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class GUIController:
    def __init__(self, model, view, userinput: str, keyword: str):
        self.evaluate = model
        self.view = view
        self.userinput = userinput
        self.puzzle = None
        self.connectSignals()
        
        
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
    def connectSignals(self, keySymbol: str, button):
        for keySymbol, button in self.view.buttonMap.items():
            if keySymbol not in {"Delete", "Shuffle", "Enter"}:
                button.clicked.connect(partial(self.buildExpr, keySymbol))
                
        self.view.buttonMap["Delete"].clicked.connect(self.deleteInput)
        self.view.display.deletePressed.connect(self.deleteInput) #will have to test
        self.view.buttonMap["Shuffle"].clicked.connect(self) #will have to figure out
        self.view.display.spacePressed.connect(self) #will have to test and figure out
        self.view.buttonMap["Enter"].clicked.connect(self.guess)
        self.view.display.returnPressed.connect(self.guess) #will have to test
        
        
################################################################################
# buildExpr(subExpression: str)
#
# DESCRIPTION:
#   Displays the newly formed expression while
#   building it in the backend to use
#
# PARAMETERS:
#  input : str
#   user input as a single character (one at a time)
################################################################################        
    def buildExpr(self, subExpression: str) -> None:
        
        expression = self.view.displayText() + subExpression
        self.view.setDisplayText(expression)       
    
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
    def newPuzzle(self, usrinput: str) -> object:
        out = MakePuzzle.newPuzzle(usrinput.lower())
        out.shuffleChars()
        self.puzzle =  out
    
################################################################################
# guess(puzzle, input: str)
#
# DESCRIPTION:
#   Checks the database for valid words, already found words and 
#   words that do not exist
#
# PARAMETERS:
#  puzzle : Obj
#   puzzle object of current played game space
#  input : str
#   user input 
################################################################################
    def guess(self, puzzle: object, input: str):
        MakePuzzle.guess(puzzle, input)
        
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
    def saveGame(self, game : object) -> None:
        self.handleSave(game, 0)
        self.handleSave(game, 1)
        
        
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
    def handleSave(self, game : object, num : int) -> None:
        saveStatus = False
        output = ''
        fileName = input('Please enter the name of the file you would like to save '
                     'for example "Game1"\n> ')
        if(path.isfile(fileName +'.json')):
            yesOrNo = input('Would you like to overwrite the file ' + fileName + '?'
                        '\n Enter Y for yes or N for no\n> ')
            if(yesOrNo == 'Y'):
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
            return 'Save Complete!'
        else:
            return 'Game could not be saved.'
        
        
################################################################################
# help() -> None
#
# DESCRIPTION:
#   provides a brief description of game rules and generally how to play as well
#   as a list of all available commands.
################################################################################
    def help() -> None:
        descHead = ('How to play: \ ')
        descBody = ("Simply type a word and press enter "
                    "to submit a guess. \ \ ")

        commHead = ('Available Commands: \ ')
        commBody = ('!new: \ '
                'Generates a new puzzle from a base word with exactly 7 '
                'unique characters, or an auto-generated base word. \ '
                '!shuffle: \ '
                'Shuffle the order of the active puzzle for a fresh view \ '
                '!save: \ '
                'Create a new save for the current game \ '
                '!load: \ '
                'Load a previously saved game \ '
                '!help: \ '
                'Show the list of all available commands with a brief '
                "description. (You're here now!) \ "
                '!exit: \ '
                'Exit the game ')
    
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
    def loadGame(self, game : object) -> None:
        fileName = input('Please enter the name of the game you are looking for.'
                     '\n> ')
        newGame =  StateStorage.loadPuzzle(fileName)
        if newGame != None:
            game = newGame
        return (game)
    
    #TODO
    def deleteInput(self):
        self.view.clearDisplay() #might have to fix if this clears the whole display

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()




