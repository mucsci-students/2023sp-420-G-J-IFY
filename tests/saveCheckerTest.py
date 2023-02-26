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
#   function1(param1 : int) -> bool
#
#   function2(param1='default' : str, param2 : bool) -> int
#
#   function3() -> None
#
#   function4() -> None
#
################################################################################

import sqlite3

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

# define Python user-defined exceptions
class LettersMismatchException(Exception):
    "Raised when key letter not in uniqueLetters"
    pass

class NotInDBException(Exception):
    pass

class PointsMismatchException(Exception):
    pass

class BadGuessesException(Exception):
    pass

def checkLoad(guessedWords : list, wordList : list, puzzleLetters : str, 
               requiredLetter : str, currentPoints: int, 
               maxPoints: int):
    # SQLite Connections
    wordDict = sqlite3.connect('wordDict.db')
    # Used to execute SQL commands
    cursor = wordDict.cursor()

    puzzleLetters = puzzleLetters.lower()
    requiredLetter = requiredLetter.lower()

    try:
        #first, check if keyLetter is in uniqueLetters
        if requiredLetter not in puzzleLetters:
            raise LettersMismatchException
        #next, check for if uniqueletters are good
        uniqueLetters = ''.join(sorted(set(puzzleLetters)))
        cursor.execute("select score from allGames where uniqueLetters = '" +
                       uniqueLetters + "' and keyLetter = '" + requiredLetter +
                       "';")
        score = cursor.fetchone()
        if score == None:
            raise NotInDBException
        
        if score[0] != maxPoints:
            raise PointsMismatchException
        
        if not set(guessedWords).issubset(set(wordList)):
            raise BadGuessesException
        

        print("If we made it here, this save is valid")

    except LettersMismatchException:
        print("Keyletter not in UniqueLetters")

    except NotInDBException:
        print("That combo of letters is not in our DB")
    
    except PointsMismatchException:
        print("Points don't match up, remake wordlist")

    except BadGuessesException:
        print("There are guessed words that are not part of the wordList")

    finally:
        #close DB
        wordDict.commit()
        wordDict.close()

#check if all is good
checkLoad([], ['kamotiq'], 'aikmoqt', 'q', 0, 14)
#check for badGuess
checkLoad(['bearfucker'], ['kamotiq'], 'aikmoqt', 'q', 0, 14)
#check for point mismatch
checkLoad([], ['kamotiq'], 'aikmoqt', 'q', 0, 7)
#check if keyLetter is mached
checkLoad([], ['kamotiq'], 'aikmoqt', 'z', 0, 7)