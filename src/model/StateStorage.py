################################################################################
# StateStorage.py
# Author: Gaige Zakroski, Yah'hymbey Baruti Ali-Bey
# Date of Creation: 2-8-2023
#
# A Module that contains many functions that will be capable of saving 
# and loading the state of a game from a json file
#
# (Global, public) functions:
#   savePuzzle(saveStateObj: Obj, fileName : str)
#       - saves a blank puzzle state
#   loadPuzzle(fileName : str) -> Puzzle Obj
#       - loads a saved puzzle
#   saveCurrent(puzzle: Obj, fileName : str)
#       - saves a current state of a puzzle
################################################################################
import sys
import os


current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import json
import string
import os.path
from os import path
import model
from pathlib import Path
import shutil


################################################################################
# __Save(dict: dict, fileName: str)
#
# DESCRIPTION:
#   Stores a dictionary to a json file under the name fileName.
#
# PARAMETERS:
#  dict : dict
#   dictionary that will be saved to a json
#  filename: str
#   string that contains the file name that will be saved.
################################################################################
def __Save(dict, fileName):
    with open(fileName, 'w') as file:
        json.dump(dict, file)
        
################################################################################
# __SearchDict(dict: dict, fileName: str) -> Element
#
# DESCRIPTION:
#   Searches a dictionary to find a specific element and returns true if it is 
#   found and false if it is not.
#
# PARAMETERS:
#  dict : dict
#   dictionary to search
#  element: E generic
#   element to search for in dict
# RETURNS:
#  element
#   Returns a searched for element in the dictionary
################################################################################
def __SearchDict(dict, element):
    dictionaryKeys = dict.keys()
    return element in dictionaryKeys

################################################################################
# __makeDict(saveStateObj: obj) -> dict
#
# DESCRIPTION:
#   takes a saveState objects fields and puts them into a dictionary to make 
#   saving easier
#
# PARAMETERS:
#  saveStateObj: obj
#   a saveState object
#
# RETURNS:
#  dict
#   Returns a dictionary of all fields of a saveState object
################################################################################
def __makeDict(saveStateObj):
    dict = {'keyLetter': saveStateObj.getKeyLetter(), 'uniqueLetters': saveStateObj.getUniqueLetters(), 
            'shuffleLetters': saveStateObj.getShuffleLetters(), 'currentScore': saveStateObj.getScore(), 'maxScore' : saveStateObj.getMaxScore(), 
            'foundWordList' : saveStateObj.getFoundWords(), 'allWordList': saveStateObj.getAllWords(), 'rank' : saveStateObj.getRank()}
    return dict

################################################################################
# __setFields(dict: dict) -> obj
#
# DESCRIPTION:
#   sets the fields of the saveState object to the corisponing value in the dictionary
#
# PARAMETERS:
#  dict: dict
#   a dictionary that contains the values of each feild of a saveState Object
#
# RETURNS:
#  obj
#   returns a saveState Object with all its fields set
################################################################################
def __setFields(dict):
    obj = model.Puzzle(dict['keyLetter'], dict['uniqueLetters'])
    obj.setShuffleLetters(dict['shuffleLetters'])
    obj.setScore(dict['currentScore'])
    obj.setMaxScore(dict['maxScore'])
    obj.setFoundWords(dict['foundWordList'])
    obj.setAllWordList(dict['allWordList'])
    obj.setRank(dict['rank'])
    return obj
    
################################################################################
# savePuzzle(saveStateObj: obj, fileName: str)
#
# DESCRIPTION:
#   Saves a blank game no matter if ther was progress already established, 
#   the function only saves the puzzle no other game state. 
#   If the file does not exist with the specified fileName then a new file 
#   will be created using that name.
#   If the file does exist with the specified fileName then the old file 
#   will be overwritten
#   If dict has a length that is not 1 and doesnt contain the element 
#   'puzzleLetters' an error is raised
#
# PRECONDITION: 
#   dict the puzzle of x amount of letters. dict must not include any found words, rank.
#
# PARAMETERS:
#  saveStateObj: obj
#   a saveState object
#  fileName: str
#   string that contains the file name that will be saved
################################################################################
def savePuzzle(saveStateObj, fileName):
    # creates dict to be saved
    newObj = model.Puzzle(saveStateObj.getKeyLetter(), saveStateObj.getUniqueLetters())
    newObj.setMaxScore(saveStateObj.getMaxScore())
    newObj.setAllWordList(saveStateObj.getAllWords())
    newObj.updateRank()

    dict = __makeDict(newObj)
    __Save(dict, fileName + ".json")
    
################################################################################
# loadPuzzle(fileName: str) -> obj
#
# DESCRIPTION:
#   loads the puzzle given a file name
#
# PARAMETERS:
#  fileName: str
#   name of the file you are loading  
#
# RETURNS:
#  __Load(fileName)
#   Loaded puzzle obj
################################################################################
def loadPuzzle(fileName):
    return __Load(fileName)

################################################################################
# saveCurrent(puzzle: obj, fileName: str)
#
# DESCRIPTION:
#   saves a current iteration of the puzzle
#
# PARAMETERS:
#  puzzle: obj
#   object you want to be saved
#  fileName: str
#   name of the file you are loading 
################################################################################
def saveCurrent(puzzle, fileName):
    __Save(__makeDict(puzzle), fileName + ".json")
    
################################################################################
# __checkFileExists(pathToFile: str) -> bool
#
# DESCRIPTION:
#   checks to see if a file exists in the current directory
#
# PARAMETERS:
#  pathToFIle : str
#   path to a specified file
#
# RETURNS:
#  p.exists()
#   true if file does exist and false otherwise
#
# RAISES:
#  FileNotFoundError
#   if path to file does not exist
################################################################################
def __checkFileExists(pathToFile):
    p = pathToFile
    if(not p.exists()):
        raise FileNotFoundError('file not Found')
    else:
        return p.exists()

################################################################################
# __Load(fileName: str) -> Obj
#
# DESCRIPTION:
#   loads the file and creates a dictionary that will be returned
#
# PARAMETERS:
#  fileName : str
#   the name of the file ex 'help'
#
# RETURNS:
#  obj
#   a dictionary that contains all the game data
#
# RAISES:
#  FileNotFoundError
#   file that is trying to be loaded does not exist
################################################################################
def __Load(fileName):
    # checks if file exists
    try:
        newFileName = fileName + '.json'
        # create a path to the current directory
        path1 = Path(Path.cwd())
        # append the file in question to the path
        a = path1 / newFileName
        __checkFileExists(a)

        # opens file
        file = open(newFileName)

        # puts elements in the file in a dictionary
        dict = json.load(file)
        obj = __setFields(dict)
        return obj
    except FileNotFoundError:

        # if fileName does not exist then a FileNotFoundError is raised saying the file does not exist
       print ("The file " + newFileName + " does not exist in this directory\n"
              "Returning to game...")
