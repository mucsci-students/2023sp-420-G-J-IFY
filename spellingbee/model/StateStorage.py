################################################################################
# StateStorage.py
# Author: Gaige Zakroski, Yah'hymbey Baruti Ali-Bey, Jacob Lovegren
# Date of Creation: 2-8-2023
#
# A Module that contains many functions that will be capable of saving 
# and loading the state of a game from a json file
#
# (Global, public) functions:
#   savePuzzle(saveStateObj: Obj, fileName : str)
#       - saves a blank puzzle state
#   loadPuzzle(fileName : str) -> Puzzle Obj
#       - loads a saved puzzle
#   saveCurrent(puzzle: Obj, fileName : str)
#       - saves a current state of a puzzle
################################################################################
import sys
from model import dbFixer
import os
import sqlite3 #for saveGameChecker
from model import MakePuzzle #for saveGameChecker
import model.output as output
import platform

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import json
import string
import os.path
from os import path
import model
from pathlib import Path
import shutil


################################################################################
# class NotInDBException(Exception)
# Description:
#   An exception for when a unique/key combo does not exist in our DB
#
# Arguments:
#   EXCEPTION : EXCEPTION
################################################################################
class NotInDBException(Exception):

    pass


################################################################################
# class BadJSONException(Exception)
# Description:
#   An exception for when a critical error occured in a json load format
#
# Arguments:
#   EXCEPTION : EXCEPTION
################################################################################
class BadJSONException(Exception):
    pass

################################################################################
# __Save(dict: dict, fileName: str)
#
# DESCRIPTION:
#   Stores a dictionary to a json file under the name fileName.
#
# PARAMETERS:
#  dict : dict
#   dictionary that will be saved to a json
#  filename: str
#   string that contains the file name that will be saved.
################################################################################
def __Save(dict, fileName):
    with open(fileName, 'w') as file:
        json.dump(dict, file)
    cwd = Path.cwd()
    saveCur = cwd  /  fileName
    if path.exists(saveCur):
        os.replace(saveCur, saveCur)
    else:
        saveNew = cwd  / 'spellingbee'  / 'data' / 'saves' / fileName
        os.replace(str(saveCur) , str(saveNew))


        
################################################################################
# __SearchDict(dict: dict, fileName: str) -> Element
#
# DESCRIPTION:
#   Searches a dictionary to find a specific element and returns true if it is 
#   found and false if it is not.
#
# PARAMETERS:
#  dict : dict
#   dictionary to search
#  element: E generic
#   element to search for in dict
# RETURNS:
#  element
#   Returns a searched for element in the dictionary
################################################################################
def __SearchDict(dict, element):
    dictionaryKeys = dict.keys()
    return element in dictionaryKeys

################################################################################
# __makeDict(saveStateObj: obj) -> dict
#
# DESCRIPTION:
#   takes a saveState objects fields and puts them into a dictionary to make 
#   saving easier
#
# PARAMETERS:
#  saveStateObj: obj
#   a saveState object
#
# RETURNS:
#  dict
#   Returns a dictionary of all fields of a saveState object
################################################################################
def __makeDict(saveStateObj):
    dict = {'RequiredLetter': saveStateObj.getKeyLetter(), 
            'PuzzleLetters': saveStateObj.getUniqueLetters(), 
            'CurrentPoints': saveStateObj.getScore(), 
            'MaxPoints' : saveStateObj.getMaxScore(), 
            'GuessedWords' : saveStateObj.getFoundWords(), 
            'WordList': saveStateObj.getAllWords()}
    return dict

################################################################################
# __setFields(dict: dict) -> obj
#
# DESCRIPTION:
#   sets the fields of the saveState object to the corisponing value in the dictionary
#
# PARAMETERS:
#  dict: dict
#   a dictionary that contains the values of each feild of a saveState Object
#
# RETURNS:
#  obj
#   returns a saveState Object with all its fields set
################################################################################
def __setFields(dict):
    obj = model.Puzzle(dict['RequiredLetter'], dict['PuzzleLetters'])
    obj.shuffleChars()
    obj.setScore(dict['CurrentPoints'])
    obj.setMaxScore(dict['MaxPoints'])
    obj.setFoundWords(dict['GuessedWords'])
    obj.setAllWordList(dict['WordList'])
    obj.setRank = obj.updateRank()
    return obj
    
################################################################################
# savePuzzle(saveStateObj: obj, fileName: str)
#
# DESCRIPTION:
#   Saves a blank game no matter if ther was progress already established, 
#   the function only saves the puzzle no other game state. 
#   If the file does not exist with the specified fileName then a new file 
#   will be created using that name.
#   If the file does exist with the specified fileName then the old file 
#   will be overwritten
#   If dict has a length that is not 1 and doesnt contain the element 
#   'puzzleLetters' an error is raised
#
# PRECONDITION: 
#   dict the puzzle of x amount of letters. dict must not include any found words, rank.
#
# PARAMETERS:
#  saveStateObj: obj
#   a saveState object
#  fileName: str
#   string that contains the file name that will be saved
################################################################################
def savePuzzle(saveStateObj, fileName):
    # creates dict to be saved
    newObj = model.Puzzle(saveStateObj.getKeyLetter(), saveStateObj.getUniqueLetters())
    newObj.setMaxScore(saveStateObj.getMaxScore())
    newObj.setAllWordList(saveStateObj.getAllWords())
    newObj.updateRank()

    dict = __makeDict(newObj)
    __Save(dict, fileName + ".json")
    
################################################################################
# loadPuzzle(fileName: str, outty : object) -> obj
#
# DESCRIPTION:
#   loads the puzzle given a file name
#
# PARAMETERS:
#  fileName: str
#   name of the file you are loading  
#
# RETURNS:
#  __Load(fileName)
#   Loaded puzzle obj
#   outty : object
#     - output object storing output strings
################################################################################
def loadPuzzle(fileName, outty):
    return __Load(fileName, outty)

################################################################################
# saveCurrent(puzzle: obj, fileName: str)
#
# DESCRIPTION:
#   saves a current iteration of the puzzle
#
# PARAMETERS:
#  puzzle: obj
#   object you want to be saved
#  fileName: str
#   name of the file you are loading 
################################################################################
def saveCurrent(puzzle, fileName):
    __Save(__makeDict(puzzle), fileName + ".json")
    
################################################################################
# __checkFileExists(pathToFile: str) -> bool
#
# DESCRIPTION:
#   checks to see if a file exists in the current directory
#
# PARAMETERS:
#  pathToFIle : str
#   path to a specified file
#
# RETURNS:
#  p.exists()
#   true if file does exist and false otherwise
#
# RAISES:
#  FileNotFoundError
#   if path to file does not exist
################################################################################
def __checkFileExists(pathToFile):
    p = pathToFile
    if(not p.exists()):
        raise FileNotFoundError('file not Found')
    else:
        return p.exists()

################################################################################
# __Load(fileName: str, outty : object) -> Obj
#
# DESCRIPTION:
#   loads the file and creates a dictionary that will be returned
#
# PARAMETERS:
#  fileName : str
#   the name of the file ex 'help'
#   outty : object
#     - output object storing output strings
#
# RETURNS:
#  obj
#   a dictionary that contains all the game data
#
# RAISES:
#  FileNotFoundError
#   file that is trying to be loaded does not exist
################################################################################
def __Load(fileName, outty):
    # checks if file exists
    try:
        os.chdir('./spellingbee/data/saves')
        # check if user ended their save with the .json filename
        if fileName.endswith('.json'):
            fileName = fileName
        else:
            fileName = fileName + '.json'
        # create a path to the current directory
        path1 = Path(Path.cwd())
        # append the file in question to the path
        a = path1 / fileName
        __checkFileExists(a)

        # opens file
        file = open(fileName)

        # puts elements in the file in a dictionary
        dict = json.load(file)
        move3dirBack()
    
        # check that dict contains valid save data
        dict = checkLoad(dict)
        # if corrupt file happens, throw exception
        if dict == None:
            raise BadJSONException

        obj = __setFields(dict)
        
        return obj
    except FileNotFoundError:
        # if fileName does not exist then a FileNotFoundError is 
        # raised saying the file does not exist
       outty.setField("The file " + fileName + " does not exist in this directory\n"
              "Returning to game...")
       move3dirBack()
    except BadJSONException:
        outty.setField("The file " + fileName + " contains critical errors that \n"
              "prevent the game from functioning properly\n"
              "Returning to game...")
       
################################################################################
# LoadFromExplorer(pathTOFile, outty)
#   
# DESCRIPTION:
#   will load a file using its path instead of its fileName
# PARAMETERS:
#   path : Path
#       the path to the file being loaded
#
################################################################################
def loadFromExploer(path : Path, outty):
    try:
        f = open(path)

        dict = json.load(f)
        dict = checkLoad(dict)
        if dict == None:
            raise BadJSONException
        obj = __setFields(dict)
        return obj
    except FileNotFoundError:
        # if fileName does not exist then a FileNotFoundError is 
        # raised saying the file does not exist
       outty.setField("The file " + path + " does not exist in this directory\n"
              "Returning to game...")
    except BadJSONException:
        outty.setField("The file " + path + " contains critical errors that \n"
              "prevent the game from functioning properly\n"
              "Returning to game...")

################################################################################
# move3dirBack()
#
# DESCRIPTION:
#   This helper function moves the directory up three levels
################################################################################
def move3dirBack():
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')


################################################################################
# allLower(my_list : list(str)) -> list(str)
#
# DESCRIPTION:
#   This helper function changes all strings in a list to lower case
#
# PARAMETERS:
#   my_list 
#       - a list of strings of unkown case
#
# RETURNS:
#   list(str)
#       - a list of strings in lower case
################################################################################
def allLower(my_list):
    return[x.lower() for x in my_list]


################################################################################
# checkLoad(loadFields)
#
# DESCRIPTION:
#   This fucntion checks all the possible reasons why our app could fail from
#   a foreign load
#
# PARAMETERS:
#   dictDict - a dictionary of the .json fields
#
# RETURNS:
#   valid dictionary for game or None if invalid save file
#
# RAISES:
#   Exception for any load that will crash our program
################################################################################
def checkLoad(dictDict):   
    # SQLite Connections
    wordDict = sqlite3.connect('spellingbee/model/wordDict.db')
    cursor = wordDict.cursor()

    try:
        #load specific dictionary fields into local variables
        #THROWS EXCEPTION IF KEY IS NOT IN DICT
        guessedWords = allLower(dictDict["GuessedWords"])
        wordList = allLower(dictDict["WordList"])
        puzzleLetters = dictDict["PuzzleLetters"].lower()
        requiredLetter = dictDict["RequiredLetter"].lower()
        currentPoints = dictDict["CurrentPoints"]
        maxPoints = dictDict["MaxPoints"]

        #check if the unique letters/keyletter combo is in our DB
        #append requiredLetter to puzzleLetters just in case they fucked
        #up how they store the required letters
        uniqueLetters = ''.join(sorted(set(puzzleLetters + requiredLetter)))
        cursor.execute("select score from allGames where uniqueLetters = '" +
                       uniqueLetters + "' and keyLetter = '" + requiredLetter +
                       "';")
        score = cursor.fetchone()
        #if the score isn't in our DB, then its not a valid game, 
        #reject the game
        if score == None:
            raise KeyError
        
        #if score mismatch, remake word list from our DB
        if score[0] != maxPoints:
            maxPoints = score[0]
            #generateWordList
            wordList = MakePuzzle.getAllWordsFromPangram(puzzleLetters, requiredLetter)
        
        #check to make sure all guesses are valid
        if not set(guessedWords).issubset(set(wordList)):
            for word in guessedWords:
                #prune any bad guesses from list
                if word not in wordList:
                    guessedWords.remove(word)
        
        #rescore the validated guess list
        tempTable = "create temporary table guessWords (guesses);"
        cursor.execute(tempTable)
        querey = "insert into guessWords (guesses) values ('"
        for a in guessedWords:
            querey += a + "'), ('"
        querey += "');"
        cursor.execute(querey)
        join = """
            select sum(wordScore) from dictionary join guessWords 
            on dictionary.fullWord is guessWords.guesses;
            """
        cursor.execute(join)
        #this is what our score should be
        ourScore = cursor.fetchone()[0]
        #if there's doesn't match, set it to ours
        if ourScore == None:
            ourScore = 0
        if ourScore != currentPoints:
            currentPoints = ourScore

        # at this point, all fields are validates in our game, remake dictionary
        dictDict["GuessedWords"] = guessedWords
        dictDict["WordList"] = wordList
        dictDict["PuzzleLetters"] = puzzleLetters
        dictDict["RequiredLetter"] = requiredLetter
        dictDict["CurrentPoints"] = currentPoints 
        dictDict["MaxPoints"] = maxPoints 


    #KeyError is raised IF the fields in the .json do not match the standard
    except KeyError:
        dictDict = None

    #NotinDBException is raised IF the game doesn't exist in our DB
    except NotInDBException:
        dictDict = None

    #regardless of end, close connection to DB
    finally:
        #close DB
        wordDict.commit()
        wordDict.close()

        #return validated dictionary or NONE if exception occured
        return dictDict