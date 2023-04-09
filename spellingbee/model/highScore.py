"""
check if game goes in high score
update highscore to inlcude new highscore
display highscore

"""

import sqlite3
from operator import itemgetter


def sort_tuples(tuples):
    return sorted(tuples, key=itemgetter(3), reverse=True)


def qualify(name, rank, score, uniqueLetters, keyLetter):
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


def updateHighScore(name, rank, score, uniqueLetters, keyLetter):
    # need to prompt the user for a name they want to insert
    conn = sqlite3.connect("spellingbee/model/highScore.db")
    cursor = conn.cursor()

    que = 'Insert into highscore (name, rank, score, uniqueLetters, keyLetter)'
    que += (f' values ("{name}", "{rank}", "{score}", ')
    que += (f'"{uniqueLetters}", "{keyLetter}")')

    cursor.execute(que)

    conn.commit()
    conn.close()


def removeHighScore(idNum):
    conn = sqlite3.connect("spellingbee/model/highScore.db")
    cursor = conn.cursor()

    que = "delete from highScore where id = " + str(idNum) + ";"

    cursor.execute(que)

    conn.commit()
    conn.close()


def getHighScore(uniqueLetters, keyLetter):
    conn = sqlite3.connect("spellingbee/model/highScore.db")
    cursor = conn.cursor()

    que = "select * from highScore where uniqueLetters like '" + uniqueLetters
    que += "' and keyLetter like '" + keyLetter + "' order by score;"

    cursor.execute(que)

    highScores = sort_tuples(cursor.fetchall())

    conn.commit()
    conn.close()

    return highScores
