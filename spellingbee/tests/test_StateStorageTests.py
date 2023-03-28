# author: Gaige Zakroski
# tests for various parts of a StateStorage module
import pytest
import os.path 
from os import path
import string
import random
import sys
import os
import model.output
from pathlib import Path
current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)
import StateStorage as spellingbee
#import spellingbee
import json
import unittest
import puzzle
import MakePuzzle

#Globals
outty = model.output.Output()
list =[]


    # Creates a random string of length 10 
def makeRandomJsonName():
        letters = string.ascii_lowercase
        result = ""
        for i in range(10):
            result += random.choice(letters)

        return result
    
def makeShortestGame():
       obj = puzzle.Puzzle('q', 'kamotiq')
       obj.allWordList = ['kamotiq']
       obj.maxScore = 14
       return obj
        

# Params: fileName    - name of the file to check
#       : dictToCheck -  the dictionary to comapre to the dictionary in the file
# Checks the contents of a file and ensures the file has the correct data in it.
# If the file does not have the correct data in it then an asserionError will be 
# raised
def checkContents(fileName, dictToCheck):
    #os.chdir('./saves')
    with open(fileName) as file:
        dict = json.load(file)
    return  dict == dictToCheck
        #spellingbee.move3dirBack()

# Params: fileName - Name of the file 
# Checks to see if the file exists in the current directory
# If the file specified does not exist in the directory then an assertionError 
# will be raised
def checkIfExists(fileName):
    return path.isfile(fileName)
    
def __makeDict(saveStateObj):
        dict = {'RequiredLetter': saveStateObj.getKeyLetter(), 
                'PuzzleLetters': saveStateObj.getUniqueLetters(), 
                'CurrentPoints': saveStateObj.getScore(), 
                'MaxPoints' : saveStateObj.getMaxScore(), 
                'GuessedWords' : saveStateObj.getFoundWords(), 
                'WordList': saveStateObj.getAllWords()}
        return dict
def removeSave(fileName):
    path = str(Path.cwd()) + '/' + fileName
    os.remove(path)
    

# test if we save an empty game and a file is not already created with the same
# name a new one is created and empty
@pytest.fixture
def puzzleFixture():
    dict = {"RequiredLetter": "a", "PuzzleLetters": "acklorw", 
            "CurrentPoints": 0, "MaxPoints": 323, "GuessedWords": [], 
            "WordList": ["acro", "alar", "alow", "arak", "arco", "awol", "caca",
                          "calk", "call", "calo", "cark", "carl", "carr",
                          "claw", "coal", "coca", "cola", "craw", "kaka", 
                          "kola","kora", "lack", "lall", "lark", "loca", "okra", 
                          "olla", "oral", "orca", "orra", "rack", "roar", 
                          "wack", "walk", "wall", "wark", "wawl", "acock", 
                          "alack", "allow", "arrow", "cacao", "calla", "carol",
                          "clack", "claro", "cloak", "coala", "cocoa", 
                          "coral", "craal", "crack", "crawl", "croak", "karoo",
                          "koala", "kraal", "local", "loral", "wacko", "walla", 
                          "wrack", "alcool", "arrack", "calcar", "callow", 
                          "carack", "cloaca", "coccal", "collar", "corral", 
                          "karroo", "wallow", "caracal", "caracol", "carrack", 
                          "cloacal", "corolla", "oarlock", "warlock", "warwork", 
                          "callaloo", "caracara", "rackwork", "wallaroo"]}    

    obj = puzzle.Puzzle('a','warlock')

    obj.uniqueLett = dict["PuzzleLetters"]
    obj.allWordList = dict["WordList"]
    obj.maxScore = dict["MaxPoints"]
    return (obj, dict)

@pytest.fixture
def playedPuzzle(puzzleFixture):
    obj = puzzleFixture[0]
    MakePuzzle.guess(obj, "warlock", False, outty)
    MakePuzzle.guess(obj, "warlock",False, outty)
    MakePuzzle.guess(obj, "wrack", False, outty)
    MakePuzzle.guess(obj, "alcool", False, outty)
    return obj

@pytest.fixture
def completedPuzzle():
    obj = makeShortestGame()
    MakePuzzle.guess(obj, 'kamotiq', False, outty) 
    return obj

def testSaveCurrent1(puzzleFixture):
    spellingbee.saveCurrent(puzzleFixture[0], 'test1')
    assert(True == checkIfExists('test1.json'))
def testCheckContentsOfTest1(puzzleFixture):
    assert(checkContents('test1.json', puzzleFixture[1]))
    removeSave('test1.json')


#test if we save  all the state remains and a file is created
def testSaveCurrentPlayed(playedPuzzle):
    spellingbee.saveCurrent(playedPuzzle, "TESTFILE2")
    dict = __makeDict(playedPuzzle)
    #os.chdir('./saves')
    with open("TESTFILE2.json") as file:
        dict = json.load(file)
    #spellingbee.move3dirBack()
    assert(checkContents('TESTFILE2.json',dict))
    removeSave('TESTFILE2.json')
    
    
    # tests the savePuzzle function to see if the information saved is saved correctly
    # meaning that only the baseWord and rhe manditory character is saved no other part of the game
def testSavePuzzleWordList(completedPuzzle):
    fileName = 'TESTFILE3'
    fileNameJson = fileName + ".json"
    spellingbee.savePuzzle(completedPuzzle,fileName)
    with open("TESTFILE3.json") as file:
        dict = json.load(file)    
    assert(dict['GuessedWords'] != ["kamotiq"])
    removeSave(fileNameJson)

def testSavePuzzleScore(completedPuzzle):
    fileName = 'TESTFILE3'
    fileNameJson = fileName + ".json"
    spellingbee.savePuzzle(completedPuzzle,fileName)
    with open("TESTFILE3.json") as file:
        dict = json.load(file)      
    assert(dict['CurrentPoints'] == 0)
    removeSave(fileNameJson)

# test if we can overrite a save
def testOverwriteSave(playedPuzzle):
    fileName = 'TESTFILE4'
    fileNameJson = fileName + ".json"
    spellingbee.saveCurrent(playedPuzzle, fileName)
    assert(checkIfExists(fileNameJson))

def testOverwriteSave2():
    fileName = 'TESTFILE4'
    fileNameJson = fileName + ".json"
    with open(fileNameJson) as file:
        dict1 = json.load(file)
    assert(checkContents(fileNameJson, dict1))

def testOverwriteSave3(playedPuzzle):
    fileName = 'TESTFILE4'
    fileNameJson = fileName + ".json"
    MakePuzzle.guess(playedPuzzle, 'acock', False, outty)
    spellingbee.saveCurrent(playedPuzzle, fileName)
    with open(fileNameJson) as file:
        dict2 = json.load(file)
    assert(checkIfExists(fileNameJson))


def testOverwriteSave4(playedPuzzle):
    fileName = 'TESTFILE4'
    fileNameJson = fileName + ".json"
    with open(fileNameJson) as file:
        dict2 = json.load(file)
    assert(checkContents(fileNameJson, dict2))
    removeSave(fileNameJson)
    #load a game and make sure the feilds are set correctly

def testLoad(playedPuzzle):
    fileName = "TESTFILE5"
    fileNameJson = fileName + ".json"
    
    MakePuzzle.guess(playedPuzzle, 'wall', False, outty)
    spellingbee.saveCurrent(playedPuzzle, fileName)
    os.replace('./TESTFILE5.json', './saves/TESTFILE5.json')

    obj2 = spellingbee.loadPuzzle(fileName, outty)

    dict1 = __makeDict(playedPuzzle)
    
    dict2 = __makeDict(obj2)
    assert(dict1 == dict2)
    os.remove( './saves/TESTFILE5.json')
    print("testLoadPuzzle1: PASSED")
    



if __name__ == '__main__':
    unittest.main()

