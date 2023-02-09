# Authors: Gaige Zakroski, 
# Course : CSCI 420
# Last Modified Date: 2/7/2023
# A Module that contains many functions that will be capable of saving 
# and loading the state of a game from a json file

import json
import string
import os.path
from os import path
import saveState
import MakePuzzle
from pathlib import Path

# Params: dict     - dictionary that will be saved to a json
#       : fileName - string that contains the file name that will be saved.
# Stores a dictionary to a json file under the name fileName.
def __Save(dict, fileName):
    with open(fileName, 'w') as file:
        json.dump(dict, file)

# Params: dict    - dictionary to search
#       : element - element to search for in dict
# Searches a dictionary to find a specific element and returns true if it is found and false if it is not.
def __SearchDict(dict, element):
    dictionaryKeys = dict.keys()
    return element in dictionaryKeys

# Params: saveStateObj - a saveState object
# takes a saveState objects fields and puts them into a dictionary to make saving easier
# Return: Returns a dictionary of all fields of a saveState object
def __makeDict(saveStateObj):
    dict = {'keyLetter': saveStateObj.showKeyLetter(), 'uniqueLetters': saveStateObj.showUniqueLetters(), 
            'shuffleLetters': saveStateObj.showShuffleLetters(), 'currentScore': saveStateObj.showScore(), 'maxScore' : saveStateObj.showMaxScore(), 
            'foundWordList' : saveStateObj.showFoundWords(), 'allWordList': saveStateObj.showAllWords(), 'rank' : saveStateObj.showRank()}
    return dict

# Params: dict - a dictionary that contains the values of each feild of a saveState Object
# sets the fields of the saveState object to the corisponing value in the dictionary
# Returns: returns a saveState Object with all its fields set
def __setFields(dict):
    obj = saveState.Puzzle(dict['keyLetter'], dict['uniqueLetters'])
    obj.setShuffleLetters(dict['shuffleLetters'])
    obj.setScore(dict['currentScore'])
    obj.setMaxScore(dict['maxScore'])
    obj.setFoundWords(dict['foundWordList'])
    obj.setAllWordList(dict['allWordsList'])
    obj.setRank(dict['rank'])
    return obj
    
        

# Params: saveStateObj - The saveStateObj
#       : fileName     - string that contains the file name that will be saved.
# Saves a blank game no matter if ther was progress already established, the function only saves the puzzle no other game state.
# If the file does not exist with the specified fileName then a new file will be created using that name.
# if the file does exist with the specified fileName then the old file will be overwritten
# if dict has a length that is not 1 and doesnt contain the element 'puzzleLetters' an error is raised
# Precondition : dict the puzzle of x amount of letters. dict must not include any found words, rank.
def savePuzzle(saveStateObj, fileName):
    # creates dict to be saved
    newObj = saveState.Puzzle(saveStateObj.showKeyLetter(), saveStateObj.showUniqueLetters())
    newObj.setMaxScore(saveStateObj.showMaxScore())
    newObj.setAllWordList(saveStateObj.showAllWords())
    newObj.updateRank()

    dict = __makeDict(newObj)
    __Save(dict, fileName + ".json")
    
# Params: filename: name of the file you are loading      
# loads the puzzle given a file name
def loadPuzzle(fileName):
    return __Load(fileName)

# Params: filename: name of the file you are loading 
#         puzzle: object you want to be saved     
# saves a current iteration of the puzzle
def saveCurrent(fileName, puzzle):
    __Save(__makeDict(puzzle), fileName + ".json")
    
# Params: pathToFile path to a specified file
# checks to see if a file exists in the current directory
# returns: true if file does exist and false otherwise
def __checkFileExists(pathToFile):
    p = pathToFile
    if(not p.exists()):
        raise FileNotFoundError('file not Found')
    else:
        return p.exists()

# Params: fileName is the name of the file ex 'help'
# loads the file and creates a dictionary that will be returned
# returns: a dictionary that contains all the game data
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
       print ("The file " + newFileName + "does not exist in this directory")

       



"""
Puzzle = MakePuzzle.newPuzzle("warlock")
saveCurrent("random", Puzzle)
LoadPuzzle = loadPuzzle("random")
print(__makeDict(LoadPuzzle))
"""