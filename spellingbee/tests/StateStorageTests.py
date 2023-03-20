# author: Gaige Zakroski
# tests for various parts of a StateStorage module

import os.path 
from os import path
import string
import random
import sys
import os
import model.output as output
from pathlib import Path
current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)
import model.StateStorage as spellingbee
#import spellingbee
import json
import unittest
import model.puzzle as Puzzle
import model.MakePuzzle as MakePuzzle
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
       obj = Puzzle.Puzzle('q', 'kamotiq')
       obj.allWordList = ['kamotiq']
       obj.maxScore = 14
       return obj
        

# Params: fileName    - name of the file to check
#       : dictToCheck -  the dictionary to comapre to the dictionary in the file
# Checks the contents of a file and ensures the file has the correct data in it.
# If the file does not have the correct data in it then an asserionError will be 
# raised
    def checkContents(fileName, dictToCheck):
        #os.chdir('./spellingbee/data/saves')
        file = open(fileName)
        dict = json.load(file)
        assert(dict == dictToCheck)
        #spellingbee.move3dirBack()

# Params: fileName - Name of the file 
# Checks to see if the file exists in the current directory
# If the file specified does not exist in the directory then an assertionError 
# will be raised
    def checkIfExists(fileName):
        #os.chdir('./spellingbee/data/saves')
        assert(path.isfile(fileName))
        #spellingbee.move3dirBack()
    
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
    obj = Puzzle.Puzzle('a','warlock')
    obj.uniqueLett = dict["PuzzleLetters"]
    obj.allWordList = dict["WordList"]
    obj.maxScore = dict["MaxPoints"]
    spellingbee.saveCurrent(obj, fileName)
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict)
    print ("testSaveCurrent1: PASSED")

#test if we save  all the state remains and a file is created
    fileName = 'TESTFILE2'
    fileNameJson = fileName + ".json"
    obj = MakePuzzle.newPuzzle("warlock",'a', outty, False)
    MakePuzzle.guess(obj, "warlock", False, outty)
    MakePuzzle.guess(obj, "warlock",False, outty)
    MakePuzzle.guess(obj, "wrack", False, outty)
    MakePuzzle.guess(obj, "alcool", False, outty)
    spellingbee.saveCurrent(obj, fileName)
    #dictionary representing obj
    #os.chdir('./spellingbee/data/saves')

    file = open(fileNameJson)
    dict = json.load(file)

    #spellingbee.move3dirBack()
    checkContents(fileNameJson,dict)
    print("testSaveCurrent2: PASSED")
    
    
    # tests the savePuzzle function to see if the information saved is saved correctly
    # meaning that only the baseWord and rhe manditory character is saved no other part of the game
    fileName = 'TESTFILE3'
    fileNameJson = fileName + ".json"
    obj = makeShortestGame()
    MakePuzzle.guess(obj, 'kamotiq', False, outty)
    dict1 = {'RequiredLetter': 'q', 'PuzzleLetters': 'kamotiq', 
                 'CurrentPoints': 0, 'MaxPoints': 14, 'GuessedWords': [], 
                 'WordList': ['kamotiq']} 
    spellingbee.savePuzzle(obj,fileName)
    os.replace('./TESTFILE3.json', './spellingbee/data/saves/TESTFILE3.json')
    obj1 = spellingbee.loadPuzzle(fileName, outty)
    assert(obj1.foundWordList != ["kamotiq"])
    assert(obj1.score == 0)
    assert(obj1.rank == "Beginner")
    os.remove('./spellingbee/data/saves/TESTFILE3.json')
      
    print("testSavePuzzle1: PASSED")   
 
  

# test if we can overrite a save

    fileName = 'TESTFILE4'
    fileNameJson = fileName + ".json"
        

    spellingbee.saveCurrent(obj, fileName)
    #os.chdir('./spellingbee/data/saves')
    file = open(fileNameJson)
    dict1 = json.load(file)
    #spellingbee.move3dirBack()
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict1)
    MakePuzzle.guess(obj, 'acock', False, outty)
    spellingbee.saveCurrent(obj, fileName)
    #os.chdir('./spellingbee/data/saves')
    file = open(fileNameJson)
    dict2 = json.load(file)
    #spellingbee.move3dirBack()
    checkIfExists(fileNameJson)
    checkContents(fileNameJson, dict2)
    print("testSaveCurrent3: PASSED")
    list.append(fileNameJson)
    #load a game and make sure the feilds are set correctly
    fileName = "TESTFILE5"
    fileNameJson = fileName + ".json"
    
    MakePuzzle.guess(obj, 'wall', False, outty)
    spellingbee.saveCurrent(obj, fileName)
    os.replace('./TESTFILE5.json', './spellingbee/data/saves/TESTFILE5.json')

    obj2 = spellingbee.loadPuzzle(fileName, outty)

    dict1 = __makeDict(obj)
    
    dict2 = __makeDict(obj2)
    assert(dict1 == dict2)
    os.remove( './spellingbee/data/saves/TESTFILE5.json')
    print("testLoadPuzzle1: PASSED")
    



if __name__ == '__main__':
    unittest.main()

