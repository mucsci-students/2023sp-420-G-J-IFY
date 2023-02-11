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
        fileName = "MeetingGame"
        dictionary = StateStorage.loadPuzzle(fileName)
        StateStorage.savePuzzle(dict, fileName)
        dict = {"keyLetter": "a", "uniqueLetters": "acklorw", "shuffleLetters": "aklrowc", "currentScore": 0, "maxScore": 323, "foundWordList": [], 'allWordList' : [], 'rank' : "Beginner"}

        checkIfExists(fileName)
        checkContents(fileName, dict)
        print("testSavePuzzle1: PASSED")
    except:
        "testSavePuzzle1: Failed (puzzle that is saved does not match a empty puzzle)"
    os.remove(fileName + '.json')

# test if we save an empty game and a file is not already created with the same name a new one is created and empty
def testSaveCurrent1():
    try:
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
        dict = {"keyLetter": "a", "uniqueLetters": "warlock", "shuffleLetters": "warlock", "currentScore": 0, "maxScore": 0, "foundWordList": [], "allWordList": [], "rank": " "}
        obj = saveState.Puzzle('a','warlock')
        StateStorage.saveCurrent(obj, fileName)
        checkIfExists(fileNameJson)
        checkContents(fileNameJson, dict)
       # os.remove(fileName + '.json')
        print ("testSaveCurrent1: PASSED")
    except:
            print("testSaveCurrent1: FAILED (new file was not created)")
    # file is removed
    os.remove(fileNameJson)
    

#test if we save  all the state remains and a file is created
def testSaveCurrent2(obj):
    try:
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
        StateStorage.saveCurrent(obj, fileName)
        #dictionary representing obj
        dict = StateStorage.__makeDict(obj)
        checkIfExists(fileNameJson)
        checkContents(fileNameJson,dict)
        print("testSaveCurrent2: PASSED")
    
    except:
        print("testSaveCurrent2: FAILED (what was saved and what was loaded are different)")
    
    # file is removed
    os.remove(fileNameJson)
  

# test if we can overrite a save
def testSaveCurrent3(obj):
    try:
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
        

        StateStorage.saveCurrent(obj, fileName)
        dict1 = StateStorage.__makeDict(obj)    
        checkIfExists(fileNameJson)
        checkContents(fileNameJson, dict1)
        MakePuzzle.guess(obj, 'acock')
        StateStorage.saveCurrent(obj, fileName)
        dict2 = StateStorage.__makeDict(obj)
        checkIfExists(fileNameJson)
        checkContents(fileNameJson, dict2)
        print("testSaveCurrent3: PASSED")

    except:
        print("testSaveCurrent3: FAILED (file was not overwritten)")
    
    os.remove(fileNameJson)

def testLoadGame1(obj):
    try:
        fileName = makeRandomJsonName()
        fileNameJson = fileName + ".json"
    
        MakePuzzle.guess(obj, 'wall')
        StateStorage.saveCurrent(obj, fileName)
        obj2 = StateStorage.loadPuzzle(fileName)
        dict1 = StateStorage.__makeDict(obj)
        dict2 = StateStorage.__makeDict(obj2)
        assert(dict1 == dict2)
        print("testLoadPuzzle1: PASSED")
    
    except:
        print("testLoadPuzzle: FAILED (puzzle fields were not set correctly)")

    os.remove(fileNameJson)



print("for the following prompt enter only the character a for testing purposes")
obj = MakePuzzle.newPuzzle("warlock")
MakePuzzle.guess(obj, "warlock")
MakePuzzle.guess(obj, "warlock")
MakePuzzle.guess(obj, "wrack")
MakePuzzle.guess(obj, "alcool")

testSavePuzzle1(obj)
testSaveCurrent1()
testSaveCurrent2(obj)
testSaveCurrent3(obj)
testLoadGame1(obj)