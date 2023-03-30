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
from View.GUI.MainWindow import MainWindow
from model import MakePuzzle, StateStorage, output
from model.puzzle import Puzzle
import PyQt6
import model.hint as hint
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QDialog, QDialogButtonBox
from PyQt6.QtWidgets import QVBoxLayout, QTextEdit, QLabel, QGridLayout, QPlainTextEdit
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

        self.window.hintAction.triggered.connect(self.hint)
        

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

        if len(set(baseWord)) == 7 or (baseWord == '' and keyLetter == ''):
            #dlg.setMessage('')
            #print(f'\nBaseword: {baseWord}\n KeyLetter: {keyLetter}\n')
            self.puzzle = MakePuzzle.newPuzzle(baseWord, keyLetter, self.outty, True)
            self.puzzle.shuffleChars()
            self.window.newGame(self.puzzle)
            dlg.baseWrd.clear()
            dlg.accept()
        else:
            #dlg.setMessage('Invalid base word')
            pass
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
        self.window.setStatus(self.outty.getField())
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
        path = str(QFileDialog.getExistingDirectory(self.window, "Select Directory"))

        if dialog.justPuzzle.isChecked():
            self.handleSave(self.puzzle, fileName, 1, path)
        else: 
            self.handleSave(self.puzzle, fileName,  0, path)   


        self.window.setStatus(self.outty.getField())
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
    def handleSave(self, game : object, fileName: str ,num : int, folder : str) -> None:
        saveStatus = False
        self.window.saveDialog.fileName.clear()
        self.window.saveDialog.justPuzzle.setChecked(False)
        folderPath = folder
        if(path.isfile(folderPath + '/' + fileName + '.json')):
            # Run Dialog Window for overwriting existing file
            # Change if to check if user click yes or no
            self.window.owDialog.show()
            self.window.owDialog.btns.accepted.connect(lambda: self.toOverwrite(num, game, fileName, folderPath))
            
        else: 
            if(num == 0):
                StateStorage.saveFromExplorer(folder, fileName, game, False)
                saveStatus = True
            elif(num == 1):
                StateStorage.saveFromExplorer(folder, fileName, game, True)
                saveStatus = True
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
        os.chdir('./saves')
        if path.isfile(fileName +'.json'):
            newGame =  StateStorage.loadPuzzle(fileName, self.outty)
            
            if newGame != None:
                self.puzzle = newGame
            else:
                self.window.loadFailed.show()
        else:
            self.window.loadFailed.show()
        os.chdir('..')
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
    def toOverwrite(self, num, game, fileName, folder):
        if(num == 0):
            StateStorage.saveFromExplorer(folder, fileName, game, False)
            saveStatus = True
        elif(num == 1):
            StateStorage.saveFromExplorer(folder, fileName, game, True)
            saveStatus = True
        self.window.owDialog.accept()

    ################################################################################
    # hint(self) -> None:
    #
    # DESCRIPTION:
    #   Displays a dialog window of the hints grid
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    ################################################################################
    def hint(self) -> None:
        # dialog window
        dlg = QDialog(parent=self.window)
        mDlg = QPlainTextEdit(dlg)
        mDlg.setBackgroundVisible(False)
        layout = QVBoxLayout()
        layout.addWidget(mDlg)
        dlg.setLayout(layout)
        mDlg.setReadOnly(True)
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(button)
        # hint object
        obj = hint.hint(self.puzzle)
        obj.makeHintGrid(self.puzzle)
        button.accepted.connect(dlg.accept)
        font = QFont('Courier', 11)
        # list representation of the hint grid
        lst = obj.hint
        dlg.setGeometry(700,300,600,600)
     
        # format String containing the Grid
        fStr = self.buildHintGrid(lst, obj)

        mDlg.setPlainText(fStr)
        
        dlg.setFont(font)
        #dlg.setLayout(self.populateHintGrid(dlg, lst))
        dlg.show()
        #execute command
        #parse data
        #display 2 user
    
    ################################################################################
    # formatHintsHeader(self) -> str:
    #
    # DESCRIPTION:
    #   formats the hint grids header
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #
    # RETURNS:
    #   fStr : str
    #       format String that contains the hint grid header
    ################################################################################
    def formatHintsHeader(self, hint) -> str:
        fStr = 'Spelling Bee Grid \n\n\n'
        fStr += 'Center Letter is Capitalized.\n\n'
        letters = self.puzzle.getShuffleLetters()

        counter = 0
        for i in letters:
            if counter == 0:
                fStr += i.capitalize() + ' '
            else:
                fStr += i + ' '
            counter += 1
        fStr += '\n\n\n'
        fStr += 'WORDS: ' + str(hint.countWords(self.puzzle)) + ', POINTS: ' + str(self.puzzle.maxScore) + ', PANGRAMS: ' +  str(hint.numPangrams(self.puzzle)) + ' ('  + str(hint.numPerfectPangram(self.puzzle)) + ' Perfect), BINGO: '+ str(self.puzzle.checkBingo())+ '\n\n\n' 

        return fStr
    
    ################################################################################
    # removeEmptyColumn(self, lst):
    #
    # DESCRIPTION:
    #   removes empty columns from the grid
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #   
    #   lst : List[List[int]]
    #
    ################################################################################
    def removeEmptyColumn(self, lst):
        pass

    ################################################################################
    # buildHintGrid(self,lst : hint):
    #
    # DESCRIPTION:
    #   builds the Hints grid
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #
    #   lst: List[List[int]]
    #       list representation of the hint grid
    #
    # RETURN:
    #   fStr: str
    #       format string containing the complete hint grid
    ################################################################################
    def buildHintGrid(self,lst, hint) -> str:
        #build hint grid
        fStr =''
        letters = ''
        fStr += self.formatHintsHeader(hint)
        # builds a string of the unique letters from the 2d list
        letters = self.getLettersFromGrid(lst)
        
        fStr += '    '

        #print the word lengths from 4 - sigma
        
        fStr += self.formatLengthHeader()

        fStr += self.formatHintsGrid(lst, letters)
        #print the body of the grid
        

        fStr += "\nTwo Letter List:\n\n"
        
        return fStr
        #return a formated string of the grid
    
    ################################################################################
    # getLettersFromGrid(lst) -> str:
    #
    # DESCRIPTION:
    #   Gets the letters from the 2d list and removes them the returns the letters
    #
    # PARAMETERS:
    #   lst : list[list[str]]
    #
    # RETURN:
    #   letters : str
    #       letters of the puzzle
    ################################################################################
    def getLettersFromGrid(self, lst) -> str:
        letters = ''
        for i in range(8):
            letters += str(lst[i][0]).capitalize()
            lst[i].pop(0)
        return letters
    
    def formatHintsGrid(self,lst ,letters) -> str:
        fStr =''
        for i in range(8):
            fStr += f'{letters[i]}:'
            for y in range(0, 13):
                fStr += f' {lst[i][y]:>3}'
                
            fStr += '\n\n'
        return fStr
    ################################################################################
    # formatLengthHeader() -> str:
    #
    # DESCRIPTION:
    #   formats the lengths of the words to be displayed for the hint grid
    #
    # PARAMETERS:
    #   None
    #
    # RETURN:
    #   fStr : str
    #       format String of the lengths Header
    ################################################################################
    def formatLengthHeader(self) -> str:
        sigma = 'Σ'
        fStr = ' '
        for i in range(4, 17):
            if i != 0 and i != 16:   
                fStr += f'{i:<4}'
            if i == 16:
                fStr += f'{sigma:3}'
        fStr += '\n\n'

        return fStr
        
    ################################################################################
    # populateHintGrid(self, parent, grid) -> QGridLayout:
    #
    # DESCRIPTION:
    #   populate the hints grid
    #
    # PARAMETERS:
    #   self
    #       Gcontroller object
    #   parent : 
    #       parent of the window
    #   grid : List[List[int]]
    #       List representation of the hint grid
    #
    # RETURN:
    #   gridLayout : QGridLayout
    #       The layout of the hint grid
    ################################################################################
    def populateHintGrid(self, parent, grid) -> QGridLayout:

        # Create QGridLayout object
        gridLayout = QGridLayout(parent)
            
        # Iterate 2D List
        for row in grid:
            for col in row:
            # For each element in the grid, create a label with text as element,
            #  then add label to the grid layout at position [row][col]
                lbl = QLabel(text=grid[row][col])
                gridLayout.addWidget(lbl, row, col)
            
        return gridLayout

def main():
    outty = output.Output()
    app = QApplication([])
    control = GController()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()