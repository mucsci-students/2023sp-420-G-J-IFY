# author: Gaige Zakroski
# tests for various parts of a StateStorage module

import os.path 
from os import path
import string
import random
import StateStorage
import json
import unittest
import puzzle 
import MakePuzzle
import pytest

class StateStorageTests(unittest.TestCase):
    # Creates a random string of length 10 
    def makeRandomJsonName():
        letters = string.ascii_lowercase
        result = ""
        for i in range(10):
            result += random.choice(letters)

        return result

# Params: fileName    - name of the file to check
#       : dictToCheck -  the dictionary to comapre to the dictionary in the file
# Checks the contents of a file and ensures the file has the correct data in it.
# If the file does not have the correct data in it then an asserionError will be raised
    def checkContents(fileName, dictToCheck):
        file = open(fileName)
        dict = json.load(file)
        assert(dict == dictToCheck)

# Params: fileName - Name of the file 
# Checks to see if the file exists in the current directory
# If the file specified does not exist in the directory then an assertionError will be raised
    def checkIfExists(fileName):
        assert(path.isfile(fileName))
    
    def __makeDict(saveStateObj):
        dict = {'keyLetter': saveStateObj.showKeyLetter(), 'uniqueLetters': saveStateObj.showUniqueLetters(), 
            'shuffleLetters': saveStateObj.showShuffleLetters(), 'currentScore': saveStateObj.showScore(), 'maxScore' : saveStateObj.showMaxScore(), 
            'foundWordList' : saveStateObj.showFoundWords(), 'allWordList': saveStateObj.showAllWords(), 'rank' : saveStateObj.showRank()}
        return dict

# tests the savePuzzle function to see if the information saved is saved correctly
# meaning that only the baseWord and rhe manditory character is saved no other part of the game
    fileName = "MeetingGame"
    obj = StateStorage.loadPuzzle(fileName)
    dict = {"keyLetter": "a", "uniqueLetters": "acklorw", "shuffleLetters": "acklorw", "currentScore": 0, "maxScore": 323, "foundWordList": [], "allWordList": ["acro", "alar", "alow", "arak", "arco", "awol", "caca", "calk", "call", "calo", "cark", "carl", "carr", "claw", "coal", "coca", "cola", "craw", "kaka", "kola", "kora", "lack", "lall", "lark", "loca", "okra", "olla", "oral", "orca", "orra", "rack", "roar", "wack", "walk", "wall", "wark", "wawl", "acock", "alack", "allow", "arrow", "cacao", "calla", "carol", "clack", "claro", "cloak", "coala", "cocoa", "coral", "craal", "crack", "crawl", "croak", "karoo", "koala", "kraal", "local", "loral", "wacko", "walla", "wrack", "alcool", "arrack", "calcar", "callow", "carack", "cloaca", "coccal", "collar", "corral", "karroo", "wallow", "caracal", "caracol", "carrack", "cloacal", "corolla", "oarlock", "warlock", "warwork", "callaloo", "caracara", "rackwork", "wallaroo"], "rank": "Beginner"}
    StateStorage.savePuzzle(obj,fileName + '1')
    checkIfExists(fileName + '.json')
    checkContents(fileName + '.json', dict)
    print("testSavePuzzle1: PASSED")
    

# test if we save an empty game and a file is not already created with the same name a new one is created and empty

    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    dict = {"keyLetter": "a", "uniqueLetters": "warlock", "shuffleLetters": "warlock", "currentScore": 0, "maxScore": 0, "foundWordList": [], "allWordList": [], "rank": " "}
    obj = puzzle.Puzzle('a','warlock')
    StateStorage.saveCurrent(obj, fileName)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict)
    print ("testSaveCurrent1: PASSED")
    
    # file is removed
    os.remove(fileNameJson)
    

#test if we save  all the state remains and a file is created
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    print("for the following prompt enter only the character a for testing purposes")
    obj = MakePuzzle.newPuzzle("warlock")
    MakePuzzle.guess(obj, "warlock")
    MakePuzzle.guess(obj, "warlock")
    MakePuzzle.guess(obj, "wrack")
    MakePuzzle.guess(obj, "alcool")
    StateStorage.saveCurrent(obj, fileName)
    #dictionary representing obj
    file = open(fileNameJson)
    dict = json.load(file)
    checkContents(fileNameJson,dict)
    print("testSaveCurrent2: PASSED")
    
    
    # file is removed
    os.remove(fileNameJson)
  

# test if we can overrite a save

    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
        

    StateStorage.saveCurrent(obj, fileName)
    file = open(fileNameJson)
    dict1 = json.load(file)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict1)
    MakePuzzle.guess(obj, 'acock')
    StateStorage.saveCurrent(obj, fileName)
    file = open(fileNameJson)
    dict2 = json.load(file)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict2)
    print("testSaveCurrent3: PASSED")
    
    os.remove(fileNameJson)
    #load a game and make sure the feilds are set correctly
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    
    MakePuzzle.guess(obj, 'wall')
    StateStorage.saveCurrent(obj, fileName)
    obj2 = StateStorage.loadPuzzle(fileName)
    dict1 = __makeDict(obj)
    
    dict2 = __makeDict(obj2)
    assert(dict1 == dict2)
    print("testLoadPuzzle1: PASSED")
    
    os.remove(fileNameJson)


if __name__ == '__main__':
    unittest.main()