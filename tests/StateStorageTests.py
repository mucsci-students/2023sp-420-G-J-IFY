# author: Gaige Zakroski
# tests for various parts of a StateStorage module

import os.path 
from os import path
import string
import random
import sys
import os


current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)
import src
import json
import unittest

list =[]
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
        dict = {'keyLetter': saveStateObj.getKeyLetter(), 'uniqueLetters': saveStateObj.getUniqueLetters(), 
            'shuffleLetters': saveStateObj.getShuffleLetters(), 'currentScore': saveStateObj.getScore(), 'maxScore' : saveStateObj.getMaxScore(), 
            'foundWordList' : saveStateObj.getFoundWords(), 'allWordList': saveStateObj.getAllWords(), 'rank' : saveStateObj.getRank()}
        return dict


    

# test if we save an empty game and a file is not already created with the same name a new one is created and empty

    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    dict = {"keyLetter": "a", "uniqueLetters": "warlock", "shuffleLetters": "warlock", "currentScore": 0, "maxScore": 0, "foundWordList": [], "allWordList": [], "rank": " "}
    obj = src.Puzzle('a','warlock')
    src.saveCurrent(obj, fileName)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict)
    print ("testSaveCurrent1: PASSED")
    
    # file is removed
    os.remove(fileNameJson)
    

#test if we save  all the state remains and a file is created
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    print("for the following prompt enter only the character a for testing purposes")
    obj = src.newPuzzle("warlock")
    src.guess(obj, "warlock")
    src.guess(obj, "warlock")
    src.guess(obj, "wrack")
    src.guess(obj, "alcool")
    src.saveCurrent(obj, fileName)
    #dictionary representing obj
    file = open(fileNameJson)
    dict = json.load(file)
    checkContents(fileNameJson,dict)
    print("testSaveCurrent2: PASSED")
    list.append(fileNameJson)
    
    
    # tests the savePuzzle function to see if the information saved is saved correctly
    # meaning that only the baseWord and rhe manditory character is saved no other part of the game
    def testSavePuzzle(self):
        fileName = 'shortestGame'
        fileNameJson = fileName + ".json"
        obj1 = src.loadPuzzle(fileName)
        src.guess(obj1, 'kamotiq')
        dict1 = {"keyLetter": "q", "uniqueLetters": "aikmoqt", "shuffleLetters": "aikmoqta", "currentScore": 0, "maxScore": 14, "foundWordList": [], "allWordList": ["kamotiq"], "rank": "Beginner"}
        src.savePuzzle(obj1,fileName)
        obj1 = src.loadPuzzle(fileName)
        self.assertNotEquals(obj1.foundWordList, ["kamotiq"])
        assert(obj1.score == 0)
        assert(obj1.rank == "Beginner")
      
        print("testSavePuzzle1: PASSED")
    # file is removed
    
 
  

# test if we can overrite a save

    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
        

    src.saveCurrent(obj, fileName)
    file = open(fileNameJson)
    dict1 = json.load(file)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict1)
    src.guess(obj, 'acock')
    src.saveCurrent(obj, fileName)
    file = open(fileNameJson)
    dict2 = json.load(file)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict2)
    print("testSaveCurrent3: PASSED")
    list.append(fileNameJson)
    #load a game and make sure the feilds are set correctly
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    
    src.guess(obj, 'wall')
    src.saveCurrent(obj, fileName)
    obj2 = src.loadPuzzle(fileName)
    dict1 = __makeDict(obj)
    
    dict2 = __makeDict(obj2)
    assert(dict1 == dict2)
    print("testLoadPuzzle1: PASSED")
    
    list.append(fileNameJson)


if __name__ == '__main__':
    unittest.main()

