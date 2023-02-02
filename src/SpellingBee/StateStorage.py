# Authors: Gaige Zakroski, 
# Course : CSCI 420
# Modified Date: 2/2/2023
# A Module that contains many functions that will be capable of saving 
# and loading the state of a game from a json file

import json
import string
import os.path
from os import path

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
        

# Params: dict     - dictionary that will be saved to a json.
#       : fileName - string that contains the file name that will be saved.
# Saves a blank game no matter if ther was progress already established, the function only saves the puzzle no other game state.
# If the file does not exist with the specified fileName then a new file will be created using that name.
# if the file does exist with the specified fileName then the old file will be overwritten
# if dict has a length that is not 1 and doesnt contain the element 'puzzleLetters' an error is raised
# Precondition : dict the puzzle of x amount of letters. dict must not include any found words, rank.
def savePuzzle(dict, fileName):
    if (__SearchDict('baseWord', dict)) and (__SearchDict('maditoryChar', dict)):
        dictToSave = {'baseWord' : dict['baseWord'], 'maditoryChar' : dict['maditoryChar']}
        __Save(dictToSave, fileName + ".json")
    else : 
        # raises a value error is a dictionary does not include a baseWord and a manditory char
        raise ValueError("Dictionary must include at least 2 elements named baseWord that is an string and manditoryChar which is the manditory character")

# Params: fileName is the name of the file
# checks to see if a file exists in the current directory
# returns: true if file does exist and false otherwise
def __checkFileExists(fileName):
    return path.isFile(fileName)

# Params: fileName is the name of the file
# loads the file and creates a dictionary that will be returned
# returns: a dictionary that contains all the game data
def __Load(fileName):
    # checks if file exists
    if (__checkFileExists(fileName + ".json")):

        # opens file
        file = open(fileName + ".json")

        # returns a dictionary from file
        return json.load(file)
    else:

        # if fileName does not exist then a FileNotFoundError is raised saying the file does not exist
        raise FileNotFoundError("The file" + fileName + ".json does not exist in this directory")
