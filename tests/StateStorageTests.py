# author: Gaige Zakroski
# tests for various parts of a StateStorage module

import os.path 
from os import path
import string
import random
import sys
import os
import model.output as output

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)


import src
import json
import unittest
outty = output.Output()
list =[]
class StateStorageTests(unittest.TestCase):
    # Creates a random string of length 10 
    
    def makeRandomJsonName():
        letters = string.ascii_lowercase
        result = ""
        for i in range(10):
            result += random.choice(letters)

        return result
    
    def makeShortestGame():
       obj = src.Puzzle('q', 'kamotiq')
       obj.allWordList = ['kamotiq']
       obj.maxScore = 14
       return obj
        

# Params: fileName    - name of the file to check
#       : dictToCheck -  the dictionary to comapre to the dictionary in the file
# Checks the contents of a file and ensures the file has the correct data in it.
# If the file does not have the correct data in it then an asserionError will be 
# raised
    def checkContents(fileName, dictToCheck):
        os.chdir('./src/data/saves')
        file = open(fileName)
        dict = json.load(file)
        assert(dict == dictToCheck)
        src.move3dirBack()

# Params: fileName - Name of the file 
# Checks to see if the file exists in the current directory
# If the file specified does not exist in the directory then an assertionError 
# will be raised
    def checkIfExists(fileName):
        os.chdir('./src/data/saves')
        assert(path.isfile(fileName))
        src.move3dirBack()
    
    def __makeDict(saveStateObj):
        dict = {'RequiredLetter': saveStateObj.getKeyLetter(), 
                'PuzzleLetters': saveStateObj.getUniqueLetters(), 
                'CurrentPoints': saveStateObj.getScore(), 
                'MaxPoints' : saveStateObj.getMaxScore(), 
                'GuessedWords' : saveStateObj.getFoundWords(), 
                'WordList': saveStateObj.getAllWords()}
        return dict


    

# test if we save an empty game and a file is not already created with the same
# name a new one is created and empty

    fileName = "TESTFILE1"
    fileNameJson = fileName + ".json"
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
    obj = src.Puzzle('a','warlock')
    obj.uniqueLett = dict["PuzzleLetters"]
    obj.allWordList = dict["WordList"]
    obj.maxScore = dict["MaxPoints"]
    src.saveCurrent(obj, fileName)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict)
    print ("testSaveCurrent1: PASSED")

#test if we save  all the state remains and a file is created
    fileName = 'TESTFILE2'
    fileNameJson = fileName + ".json"
    obj = src.newPuzzle("warlock",'a', outty, False)
    src.guess(obj, "warlock", False, outty)
    src.guess(obj, "warlock",False, outty)
    src.guess(obj, "wrack", False, outty)
    src.guess(obj, "alcool", False, outty)
    src.saveCurrent(obj, fileName)
    #dictionary representing obj
    os.chdir('./src/data/saves')

    file = open(fileNameJson)
    dict = json.load(file)

    src.move3dirBack()
    checkContents(fileNameJson,dict)
    print("testSaveCurrent2: PASSED")
    
    
    # tests the savePuzzle function to see if the information saved is saved correctly
    # meaning that only the baseWord and rhe manditory character is saved no other part of the game
    fileName = 'TESTFILE3'
    fileNameJson = fileName + ".json"
    obj = makeShortestGame()
    src.guess(obj, 'kamotiq', False, outty)
    dict1 = {'RequiredLetter': 'q', 'PuzzleLetters': 'kamotiq', 
                 'CurrentPoints': 0, 'MaxPoints': 14, 'GuessedWords': [], 
                 'WordList': ['kamotiq']} 
    src.savePuzzle(obj,fileName)
    obj1 = src.loadPuzzle(fileName, outty)
    assert(obj1.foundWordList != ["kamotiq"])
    assert(obj1.score == 0)
    assert(obj1.rank == "Beginner")
      
    print("testSavePuzzle1: PASSED")   
 
  

# test if we can overrite a save

    fileName = 'TESTFILE4'
    fileNameJson = fileName + ".json"
        

    src.saveCurrent(obj, fileName)
    os.chdir('./src/data/saves')
    file = open(fileNameJson)
    dict1 = json.load(file)
    src.move3dirBack()
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict1)
    src.guess(obj, 'acock', False, outty)
    src.saveCurrent(obj, fileName)
    os.chdir('./src/data/saves')
    file = open(fileNameJson)
    dict2 = json.load(file)
    src.move3dirBack()
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict2)
    print("testSaveCurrent3: PASSED")
    list.append(fileNameJson)
    #load a game and make sure the feilds are set correctly
    fileName = "TESTFILE5"
    fileNameJson = fileName + ".json"
    
    src.guess(obj, 'wall', False, outty)
    src.saveCurrent(obj, fileName)
    obj2 = src.loadPuzzle(fileName, outty)
    dict1 = __makeDict(obj)
    
    dict2 = __makeDict(obj2)
    assert(dict1 == dict2)
    print("testLoadPuzzle1: PASSED")
    



if __name__ == '__main__':
    unittest.main()

