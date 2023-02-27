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
    pass

class NotInDBException(Exception):
    pass

class PointsMismatchException(Exception):
    pass

class BadGuessesException(Exception):
    pass

class WrongCurrentScoreException(Exception):
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

        ourScore = cursor.fetchone()[0]

        if ourScore == None:
            ourScore = 0
        if ourScore != currentPoints:
            raise WrongCurrentScoreException

        print("If we made it here, this save is valid")

    except LettersMismatchException:
        print("Keyletter not in UniqueLetters")
        #from here, we need determine if those uniqueLetters even make a word, 
        #or just rejec the save entirely. I'm leaning towards reject the save

    except NotInDBException:
        print("That combo of letters is not in our DB")
        #again, without this funtionality, probably better to reject the save
        #entirely
    
    except PointsMismatchException:
        print("Points don't match up, remake wordlist")
        #this is easy enough, just regenerate that word list

    except BadGuessesException:
        print("There are guessed words that are not part of the wordList")
        #prune them from the list

    except WrongCurrentScoreException:
        print("The score is not correct. Needs to be recalced")
        #update score

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
#check if game is scored incorrectly
checkLoad(['waxworks'], ['waxwork', 'waxworks'], 'waxorks', 'x', 8, 22)
