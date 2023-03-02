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
from functools import partial
from SimpleBCluster import SimpleButtonCluster
import MakePuzzle
import MainWindow
import puzzle
import PyQt6
from PyQt6.QtWidgets import QApplication

class GUIController:
    def __init__(self, model, view):
        self.evaluate = model
        self.view = view
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