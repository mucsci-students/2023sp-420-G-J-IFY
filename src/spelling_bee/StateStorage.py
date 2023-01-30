# Authors: Gaige Zakroski, 
# Course : CSCI 420
# Modified Date: 1/30/2023
# A Module that contains many functions that will be capable of saving 
# and loading the state of a game from a json file

import json
import string

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
        for i in dict:
            if i == element:
                return True
            else :
                return False
        

# Params: dict     - dictionary that will be saved to a json.
#       : fileName - string that contains the file name that will be saved.
# Saves a blank game no matter if ther was progress already established, the function only saves the puzzle no other game state.
# If the file does not exist with the specified fileName then a new file will be created using that name.
# if the file does exist with the specified fileName then the old file will be overwritten
# if dict has a length that is not 1 and doesnt contain the element 'puzzleLetters' an error is raised
# Precondition : dict the puzzle of x amount of letters. dict must not include any found words, rank.
def savePuzzle(dict, fileName):
    if __SearchDict('puzzleLetters', dict) and len(dict) == 1:
        __Save(dict, fileName + ".json")
    else : 

        # raises a value error is a dictionarys length is not equal to 1 and if the dictionary does not contain puzzleLetters
        raise ValueError("Dictionary must only include 1 element named 'puzzleLetters that is an array of characters")
