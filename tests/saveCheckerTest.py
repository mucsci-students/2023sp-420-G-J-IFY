################################################################################
# saveCheckerTest.py
# Author: Jacob Lovegren
# Date of Creation: 02-24-2023
#
# This module is the test code for save game checker. With the user being able
# to load in saves from other games, those files need to be checked to ensure 
# that some difference in our systems doesn't crash our game. 
#
# (Global, public) functions:
#   checkLoad(fileName:str) -> dict
#
#   load(fileName:str) -> dict
#
#   allLoser(my_list:list(str)) -> list(str)
#
################################################################################

import sqlite3
import json
from model import StateStorage
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import os.path
from os import path
from model import MakePuzzle
from pathlib import Path


#for my own sanity, this is the example json save format we need to check
#against
"""{
    "GuessedWords": [
        "fire",
        "flop",
        "file"
    ],  "WordList": [
      "profile", 
      "fire", 
      "flop", 
      "file", 
      "other words that make sense"
    ],
    "PuzzleLetters": "profile",
    "RequiredLetter": "f",
    "CurrentPoints": 3,
    "MaxPoints": 647
}"""

################################################################################
# class NotInDBException(Exception)
# Description:
#   An exception for when a unique/key combo does not exist in our DB
#
# Arguments:
#   EXCEOTION : EXCEPTION
################################################################################
class NotInDBException(Exception):
    pass

################################################################################
# checkLoad(loadFields)
#
# DESCRIPTION:
#   This fucntion checks all the possible reasons why our app could faile from
#   a foreign load
#
# PARAMETERS:
#   fileName - the string of the beginning of a .json file storing save data
#
# RETURNS:
#   valid dictionary for game
#
# RAISES:
#   Exception
#    
################################################################################
def checkLoad(fileName):   
    # SQLite Connections
    wordDict = sqlite3.connect('wordDict.db')
    cursor = wordDict.cursor()

    try:
        #Parse the json for a dict
        dictDict = Load(fileName)

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
            raise NotInDBException
        
        #if score mismatch, remake word list from our DB
        if score[0] != maxPoints:
            print("Points mismatch, fixing now")
            maxPoints = score[0]
            #generateWordList
            wordList = MakePuzzle.getAllWordsFromPangram(puzzleLetters, 
                                                         requiredLetter)
        
        #check to make sure all guesses are valid
        if not set(guessedWords).issubset(set(wordList)):
            for word in guessedWords:
                #prune any bad guesses from list
                if word not in wordList:
                    print(word + " Is not a valid for this puzzle")
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
            print("Looks like those points aren't accureate. Let's get "
                  + "that corrected ")
            currentPoints = ourScore

        #at this point, all fields are validates in our game, remake dictionary
        print("If we made it here, this save is valid")
        dictDict["GuessedWords"] = guessedWords
        dictDict["WordList"] = wordList
        dictDict["PuzzleLetters"] = puzzleLetters
        dictDict["RequiredLetter"] = requiredLetter
        dictDict["CurrentPoints"] = currentPoints 
        dictDict["MaxPoints"] = maxPoints 



    #KeyError is raised IF the fields in the .json do not match the standard
    except KeyError:
        print("BAD KEYS")
        #this is a critical error and needs to be dumped
        dictDict = None

    #NotinDBException is raised IF the game doesn't exist in our DB
    except NotInDBException:
        print("That combo of letters is not in our DB")
        #REJECT THE LOAD
        dictDict = None

    #regardless of end, close connection to DB
    finally:
        #close DB
        wordDict.commit()
        wordDict.close()
        print('In the finally block')
        #return validated dictionary
        return dictDict

################################################################################
# This is an exact ripoff of StateStorage.__load()
################################################################################
def Load(fileName):
    # checks if file exists
    try:
        os.chdir('./src/data/saves')
        newFileName = fileName + '.json'
        # create a path to the current directory
        path1 = Path(Path.cwd())
        # append the file in question to the path
        a = path1 / newFileName
        StateStorage.__checkFileExists(a)

        # opens file
        file = open(newFileName)

        # puts elements in the file in a dictionary
        dict = json.load(file)
        move3dirBack()
        return dict
    except FileNotFoundError:

        # if fileName does not exist then a FileNotFoundError is 
        # raised saying the file does not exist
       print ("The file " + newFileName + " does not exist in this directory\n"
              "Returning to game...")
       move3dirBack()
       
def move3dirBack():
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')

############################################################################
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
############################################################################
def allLower(my_list):
    return[x.lower() for x in my_list]


#Test cases

print("\nkamotiqGood")
checkLoad('kamotiqGood')
print('\nwarlockGood')
checkLoad('warlockGood')
print('\nwaxworkGood')
checkLoad('waxworkGood')
ret = print('\nbadFields')
if ret == None:
    print("REJECT THE LOAD!!!")
checkLoad('badFields')
print('\nbadGameSeed')
checkLoad('badGameSeed')
print('\nbadMaxScore')
checkLoad('badMaxScore')
print('\nbadGuess')
checkLoad('badGuess')
print('\nBADEVERYTHING')
checkLoad('BADEVERYTHING')

