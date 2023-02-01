# author: Gaige Zakroski
# tests for various parts of a StateStorage module

import os.path 
from os import path
import string
import random
import StateStorage
import json
import unittest

# Creates a random string of length 10
def makeRandomJsonName():
    letters = string.ascii_lowercase
    result = ""
    for i in range(10):
        result += random.choice(letters)

    return result + '.json'

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
def testSavePuzzle1():
    fileName = makeRandomJsonName()
    dict = {"baseWord" : "warlock", "maditoryChar" : 'a'}
    StateStorage.savePuzzle(dict, fileName)

    checkIfExists(fileName)
    checkContents(fileName, {"baseWord" : "warlock", "manditoryChar" : 'a'})

# tests the savePuzzle function to see if the information saved is saved correctly
# meaning that only the baseWord and rhe manditory character is saved no other part of the game
def testSavePuzzle2():
    fileName = makeRandomJsonName()
    dict = { "baseWord" : "warlock", "maditoryChar" : 'a', "foundWords" : ["lock", "clock", "warlock"], "level" : 10}
    StateStorage.savePuzzle(dict, fileName)

    checkIfExists(fileName)
    checkContents(fileName, {"baseWord" : "warlock", "manditoryChar" : 'a'})

    # file is removed
    os.remove(fileName)


# test if we save an empty game and a file is not already created with the same name a new one is created and empty
def testSaveCurrent1():
    fileName = makeRandomJsonName()
    StateStorage.saveCurrent(fileName, {})
    checkIfExists(fileName)
    checkContents(fileName, {})

    print ("testSaveCurrent1: Passed")

    # file is removed
    os.remove(fileName)

#test if we save  all the state remains and a file is created
def testSaveCurrent2():
    dict = {'health' : 29, 'name' : 'Gaige'}
    fileName = makeRandomJsonName()
    StateStorage.saveCurrent(fileName, dict)

    checkIfExists(fileName)
    checkContents(fileName,dict)
    print("testSaveCurrent2: PASSED")
    
    # file is removed
    os.remove(fileName)

# test if we can overrite a save
def testSaveCurrent3():
    fileName = makeRandomJsonName()
    dict = {'health' : 29, 'name' : 'Gaige'}

    StateStorage.saveCurrent(fileName, {})

    checkIfExists(fileName)
    checkContents(fileName, {})

    StateStorage.saveCurrent(fileName, dict)

    checkIfExists(fileName)
    checkContents(fileName, dict)
    print("testSaveCurrent3: PASSED")

    # file is removed
    os.remove(fileName)

# tests to see if when a puzzle is loaded that doest exist and exception is thrown
def testLoadPuzzle():
    fileName = makeRandomJsonName()

    with StateStorage.assetRaises(Exception) as result:
        StateStorage.loadPuzzle(fileName)
    
    assert(result == ".")
    print("testLoadPuzzle1: PASSED")

    os.remove(fileName)

# test if when we load a puzzle we get the correct information back if the file exists
def testLoadPuzzle2():
    fileName = makeRandomJsonName()
    dict = dict = { "baseWord" : "warlock", "maditoryChar" : 'a', "foundWords" : ["lock", "clock", "warlock"], "level" : 10}
    StateStorage.saveCurrent(fileName, dict)

    checkContents(fileName, dict)
    print("testLoadPuzzle2: Passed")

    os.remove(fileName)




