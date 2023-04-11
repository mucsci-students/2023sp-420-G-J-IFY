###############################################################################
# highScore.py
# Author: Jacob Lovegren
# Date of Creation: 04-09-2023
#
# This is a collection of backend functions to track, update, and return
# a local high score for each game
#
# (Global, public) functions:
#
#   qualify(name: str, rank: str, score: int, uniqueLetters: str,
#          keyLetter: str) -> None
#
#   updateHighScore(name: str, rank: str, score: int, uniqueLetters: str,
#          keyLetter: str) -> None:
#
#   removeHighScore(idNum: int) -> None:
#
#   getHighScore(uniqueLetters: str, keyLetter: str) -> None:
#
#   sort_tuples(list of tuples) -> none
###############################################################################

import sqlite3
from operator import itemgetter


###############################################################################
# qualify(name: str, rank: str, score: int, uniqueLetters: str,
#          keyLetter: str) -> None
#
# DESCRIPTION:
#   Checks to see if a user's score is good enough to be on the highscore
#   board.
#   If there are fewer than 10, automatically pass it to update
#   otherwise, check if the user scored high enough, and if so, update
#
# PARAMETERS:
#   name : str
#     - the name of the player
#   rank : str
#     - the attained rank for the game
#   score : int
#     - the score for the game
#   uniqueLetters : str
#     - the unique letters for the game
#   keyLetter : str
#     - the key letter for the game
###############################################################################
def qualify(name: str, rank: str, score: int, uniqueLetters: str,
            keyLetter: str) -> None:
    current = sort_tuples(getHighScore(uniqueLetters, keyLetter))

    if len(current) < 10:
        updateHighScore(name, rank, score, uniqueLetters, keyLetter)
    # otherwise, need to figure out if they qualify for leaderboard
    else:
        if score <= current[9][3]:
            # does not qualify
            pass
        else:
            # here is where we can prompt for an input from user for name
            removeHighScore(current[9][0])
            updateHighScore(name, rank, score, uniqueLetters, keyLetter)


###############################################################################
# updateHighScore(name: str, rank: str, score: int, uniqueLetters:str,
#          keyLetter:str) -> None:
#
# DESCRIPTION:
#   Connect to the DB and insert the information for the given game
#
# PARAMETERS:
#   name : str
#     - the name of the player
#   rank : str
#     - the attained rank for the game
#   score : int
#     - the score for the game
#   uniqueLetters : str
#     - the unique letters for the game
#   keyLetter : str
#     - the key letter for the game
###############################################################################
def updateHighScore(name: str, rank: str, score: int, uniqueLetters: str,
                    keyLetter: str) -> None:
    # need to prompt the user for a name they want to insert
    conn = sqlite3.connect("spellingbee/model/highScore.db")
    cursor = conn.cursor()

    que = 'Insert into highscore (name, rank, score, uniqueLetters, keyLetter)'
    que += (f' values ("{name}", "{rank}", "{score}", ')
    que += (f'"{uniqueLetters}", "{keyLetter}")')

    cursor.execute(que)

    conn.commit()
    conn.close()


###############################################################################
# removeHighScore(idNum: int) -> None:
#
# DESCRIPTION:
#   Connect to DB and remove lowest score for given game
#
# PARAMETERS:
#   idNum : int
#     - the primary key of the game to be removed
###############################################################################
def removeHighScore(idNum: int) -> None:
    conn = sqlite3.connect("spellingbee/model/highScore.db")
    cursor = conn.cursor()

    que = "delete from highScore where id = " + str(idNum) + ";"

    cursor.execute(que)

    conn.commit()
    conn.close()


###############################################################################
# getHighScore(uniqueLetters: str, keyLetter: str) -> None:
#
# DESCRIPTION:
#   Finds the highscores for a given game in the DB
#
# PARAMETERS:
#   uniqueLetters : str
#     - the unique letters for the game
#   keyLetter : str
#     - the key letter for the game
#
# RETURNS:
#   list of tuples
#     - the highscores for the given game as a list of tuples
#       (id : int, name : str, rank : str, score : int,
#           uniqueLetters : str, keyLetter : str)
###############################################################################
def getHighScore(uniqueLetters: str, keyLetter: str) -> None:
    conn = sqlite3.connect("spellingbee/model/highScore.db")
    cursor = conn.cursor()

    que = "select * from highScore where uniqueLetters like '" + uniqueLetters
    que += "' and keyLetter like '" + keyLetter + "' order by score;"

    cursor.execute(que)

    highScores = sort_tuples(cursor.fetchall())

    conn.commit()
    conn.close()

    return highScores


###############################################################################
# sort_tuples(list of tuples) -> none
#
# DESCRIPTION:
#   Helper function to sort a list of tuples by the 3rd element
#   geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/#
#
# PARAMETERS:
#   tuples : list
#     - a list of tuples to be sorted
#
# RETURNS:
#   list
#     - a sorted list of tuples
###############################################################################
def sort_tuples(tuples: list):
    return sorted(tuples, key=itemgetter(3), reverse=True)
