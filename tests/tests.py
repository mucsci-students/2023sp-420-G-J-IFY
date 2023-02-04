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
def testSavePuzzle1():
    fileName = makeRandomJsonName()
    fileNameJson = fileName + '.json'

    dict = {'baseWord' : 'warlock', 'manditoryChar' : 'a'}
    StateStorage.savePuzzle(dict, fileName)

    checkIfExists(fileNameJson)
    checkContents(fileNameJson, {"baseWord" : "warlock", "manditoryChar" : 'a'})
    print("testSavePuzzle1: PASSED")


# tests the savePuzzle function to see if the information saved is saved correctly
# meaning that only the baseWord and rhe manditory character is saved no other part of the game
def testSavePuzzle2():
    fileName = makeRandomJsonName()
    fileNameJson = fileName + '.json'
    dict = { "baseWord" : "warlock", "manditoryChar" : 'a', "foundWords" : ["lock", "clock", "warlock"], "level" : 10}
    StateStorage.savePuzzle(dict, fileName)

    checkIfExists(fileNameJson)
    checkContents(fileNameJson, {"baseWord" : "warlock", "manditoryChar" : 'a'})

    # file is removed
    os.remove(fileNameJson)
    print("testSavePuzzle2: PASSED")


# test if we save an empty game and a file is not already created with the same name a new one is created and empty
def testSaveCurrent1():
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    StateStorage.saveCurrent({}, fileName)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, {})

    print ("testSaveCurrent1: PASSED")

    # file is removed
    os.remove(fileNameJson)

#test if we save  all the state remains and a file is created
def testSaveCurrent2():
    dict = {'health' : 29, 'name' : 'Gaige'}
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    StateStorage.saveCurrent(dict, fileName)

    checkIfExists(fileNameJson)
    checkContents(fileNameJson,dict)
    print("testSaveCurrent2: PASSED")
    
    # file is removed
    os.remove(fileNameJson)

# test if we can overrite a save
def testSaveCurrent3():
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

    # file is removed
    os.remove(fileNameJson)

# tests to see if when a puzzle is loaded that doest exist and exception is thrown
def test__Load1():
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    dict = {'baseWord' : "warlock", 'manditoryChar' : 'a' }
    StateStorage.savePuzzle(dict, fileName)
    loadedDict = StateStorage.__Load(fileName)
    assert(dict == loadedDict)
    print("testLoadPuzzle1: PASSED")

    os.remove(fileNameJson)

# test if when we load a puzzle we get the correct information back if the file exists
def test__Load2():
    fileName = makeRandomJsonName()
    fileNameJson = fileName + ".json"
    dict = dict = { 'baseWord' : "warlock", 'manditoryChar' : 'a', "foundWords" : ["lock", "clock", "warlock"], "level" : 10}
    StateStorage.savePuzzle(dict, fileName)

    loadedDict = StateStorage.__Load(fileName)
    checkContents(fileNameJson, {'baseWord' : "warlock", 'manditoryChar' : 'a'})
    print("testLoadPuzzle2: PASSED")

    os.remove(fileNameJson)




