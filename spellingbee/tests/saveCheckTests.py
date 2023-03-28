################################################################################
# saveCheckTest.py
# Author: Jacob Lovegren, Gaige Zakroski
# Date of Creation: 03-4-2023
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

import unittest
import json
import StateStorage
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import os.path
from os import path
from pathlib import Path
import model.output

def Load(fileName):
    # checks if file exists
    try:
        print(Path.cwd())
        os.chdir('spellingbee/tests/saves')
        print(Path.cwd())
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
        os.chdir('..')
        os.chdir('..')
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


class saveCheckTests(unittest.TestCase):
        # tests if the bad field names in json file return a None object
        try:
            # check id a totaly corrupt file returns a None Obj
            dict = Load('badFields')
            dict2 = StateStorage.checkLoad(dict)
            assert(dict2 == None)
            print("SaveCheck TestCase1: PASSED")
        except:
            print("SaveCheck TestCase1: FAILED")
            print()
    
        # tests if a good save remains the same
        try:
            dict = Load('kamotiqGood')
            dict2 = StateStorage.checkLoad(dict)
            assert(dict2 != None)
            print("SaveCheck TestCase2: PASSED")
        except:
            print("SaveCheck TestCase2: FAILED")

        # tests if a good save remains the same
        try:
            dict = Load('warlockGood')
            dict2 = StateStorage.checkLoad(dict)
            assert(dict2 != None)
            print("SaveCheck TestCase3: PASSED")
        except:
            print("SaveCheck TestCase3: FAILED")

        # tests if a good save remains the same
        try:
            dict = Load('waxworkGood')
            dict2 = StateStorage.checkLoad(dict)
            assert(dict2 != None)
            print("SaveCheck TestCase4: PASSED")
        except:
            print("SaveCheck TestCase4: FAILED")

        # tests if a save has bad guesses and are they removed
        try:
            dict = Load('badGuess')
            dict2 = StateStorage.checkLoad(dict)
            assert(dict2['GuessedWords'] == [])
            print("SaveCheck TestCase5: PASSED")
        except:
            print("SaveCheck TestCase5: FAILED")
            print(str(dict['GuessedWords']) + ' != []')

        # tests to see if the max score is correct and if not is it converted correctly
        try:
            dict = Load('badMaxScore')
            dict2 = StateStorage.checkLoad(dict)
            assert(dict2['MaxPoints'] == 323)
            print("SaveCheck TestCase3: PASSED")
        except:

            print("SaveCheck testBadMaxScore: FAILED")
            print(str(dict2['MaxPoints']) + '!= 323')
        # tests if a game doesnt exist does a None Object get returned
        try:
            dict = Load('badGameSeed')
            dict2 = StateStorage.checkLoad(dict)
            assert(dict2 == None)
            print("SaveCheck testBadGameSeed: PASSED")
        except:
            print("SaveCheck testBadGameSeed: FAILED")


        
        dict = Load('BADEVERYTHING')
        dict2 = StateStorage.checkLoad(dict)

        # Tests if the max score is converte correctly
        try:
            assert(dict2['MaxPoints'] == 323)
            print("SaveCheck BADEVERYTHING MaxScore: PASSED")

        except:
            print("SaveCheck BADEVERYTHING MaxScore: FAILED")
            print(str(dict2['MaxPoints']) +' != 323')

        # tests if the current points is correctly converted
        try:
            assert(dict2['CurrentPoints'] == 0)
            print("SaveCheck BADEVERYTHING CurrentScore: PASSED")

        except:
            print("SaveCheck BADEVERYTHING CurrentScore: FAILED")
            print(str(dict2['CurrentPoints']) +' != 0')
        
        # tests if the guessed words list is correctly converted
        try:
            assert(dict2['GuessedWords'] == [])
            print("SaveCheck BADEVERYTHING GuessedWords: PASSED")

        except:
            print("SaveCheck BADEVERYTHING GuessedWords: FAILED")
            print(str(dict2['GuessedWords']) +' != []')

        # tests to see if the wordlist is correctly converted
        try:
            outty = model.output.Output()
            dict = Load('warlock')
            dictlen = len(dict['WordList'])
            assert(len(dict2['WordList']) == dictlen)
            print("SaveCheck BADEVERYTHING WordList: PASSED")
        except:
            print("SaveCheck BADEVERYTHING WordList: FAILED")
            print('dict2 word list length: ' +  str(len(dict2['WordList'])) +'!= ' + str(dictlen))

if __name__ == '__main__':
    unittest.main()    