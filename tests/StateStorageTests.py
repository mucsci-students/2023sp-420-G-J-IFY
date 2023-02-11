# author: Gaige Zakroski
# tests for various parts of a StateStorage module

import os.path 
from os import path
import string
import random
import StateStorage
import json
import unittest
import saveState 
import MakePuzzle

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

# tests the savePuzzle function to see if the information saved is saved correctly
# meaning that only the baseWord and rhe manditory character is saved no other part of the game
def testSavePuzzle1(obj):
    try:
        fileName = "MeetingGame.json"
        dictionary = StateStorage.loadPuzzle(fileName)
        StateStorage.savePuzzle(dict, fileName)
        dict = {"keyLetter": "a", "uniqueLetters": "acklorw", "shuffleLetters": "aklrowc", "currentScore": 0, "maxScore": 323, "foundWordList": [], 'allWordList' : [], 'rank' : "Beginner"}

        checkIfExists(fileName)
        checkContents(fileName, dict)
        print("testSavePuzzle1: PASSED")
    except:
        "testSavePuzzle1: Failed (puzzle that is saved does not match a empty puzzle)"

# test if we save an empty game and a file is not already created with the same name a new one is created and empty
def testSaveCurrent1(obj):
    try:
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
        StateStorage.saveCurrent({}, fileNameJson)
        checkIfExists(fileNameJson)
        checkContents(fileNameJson, {})
       # os.remove(fileName + '.json')
        print ("testSaveCurrent1: PASSED")
    except:
            print("testSaveCurrent1: FAILED (new file was not created)")
    # file is removed
    

#test if we save  all the state remains and a file is created
def testSaveCurrent2(obj):
    try:

        dict = {'health' : 29, 'name' : 'Gaige'}
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
        StateStorage.saveCurrent(dict, fileName)

        checkIfExists(fileNameJson)
        checkContents(fileNameJson,dict)
        #os.remove(fileNameJson)
        print("testSaveCurrent2: PASSED")
    
    except:
        print("testSaveCurrent2: FAILED (what was saved and what was loaded are different)")
    
    # file is removed
  

# test if we can overrite a save
def testSaveCurrent3(obj):
    try:
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
        dict = {'health' : 29, 'name' : 'Gaige'}

        StateStorage.saveCurrent(fileNameJson, {})

        checkIfExists(fileNameJson)
        checkContents(fileNameJson, {})

        StateStorage.saveCurrent(dict, fileName)

        checkIfExists(fileNameJson)
        checkContents(fileNameJson, dict)
        print("testSaveCurrent3: PASSED")

    except:
        print("testSaveCurrent3: FAILED (file was not overwritten)")

    # file is removed
    os.remove(fileNameJson)

def testLoadGame1(fileName):
    try:
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
        obj1 = MakePuzzle.newPuzzle('warlock')
        MakePuzzle.guess(obj1, "warlock")
        MakePuzzle.guess(obj1, "wrack")
        MakePuzzle.guess(obj1, "alcool")
        StateStorage.saveCurrent(obj1, fileNameJson)
        obj2 = StateStorage.loadGame(fileNameJson)

        assert(obj1 == obj2)
        print("testLoadPuzzle1: PASSED")
    
    except:
        print("testLoadPuzzle: FAILED (puzzle fields were not set correctly)")

    os.remove(fileNameJson)




obj = MakePuzzle.newPuzzle("warlock")
MakePuzzle.guess(obj, "warlock")
MakePuzzle.guess(obj, "warlock")
MakePuzzle.guess(obj, "wrack")
MakePuzzle.guess(obj, "alcool")

testSavePuzzle1(obj)
testSaveCurrent1(obj)
testSaveCurrent2(obj)
testSaveCurrent3(obj)
testLoadGame1()