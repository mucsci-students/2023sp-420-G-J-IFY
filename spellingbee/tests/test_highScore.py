import sqlite3
import highScore


def testGetHighscoresNone():
    ret = highScore.getHighScore('abcdefg', 'a')
    assert (ret == [])


def testQualifyFill():
    highScore.qualify('TEST101', 'Good Start', 1, 'abcdefg', 'a')
    highScore.qualify('TEST102', 'Good Start', 2, 'abcdefg', 'a')
    highScore.qualify('TEST103', 'Good Start', 3, 'abcdefg', 'a')
    highScore.qualify('TEST104', 'Good Start', 4, 'abcdefg', 'a')
    highScore.qualify('TEST105', 'Good Start', 5, 'abcdefg', 'a')
    highScore.qualify('TEST106', 'Good Start', 6, 'abcdefg', 'a')
    highScore.qualify('TEST107', 'Good Start', 7, 'abcdefg', 'a')
    highScore.qualify('TEST108', 'Good Start', 8, 'abcdefg', 'a')
    highScore.qualify('TEST109', 'Good Start', 9, 'abcdefg', 'a')
    highScore.qualify('TEST110', 'Moving Up', 23, 'abcdefg', 'a')
    assert (highScore.getHighScore('abcdefg', 'a')[0][1] == 'TEST110')


def testQualifyFirst():
    highScore.qualify('TEST201', 'Queen Bee', 14, 'abcdefz', 'z')
    assert (highScore.getHighScore('abcdefz', 'z')[0][1] == 'TEST201')


def testNewHighScore():
    highScore.qualify('TEST111', 'Moving Up', 24, 'abcdefg', 'a')
    assert (highScore.getHighScore('abcdefg', 'a')[0][1] == 'TEST111')


def testDoesNotQualify():
    highScore.qualify('TEST111', 'Good Start', 1, 'abcdefg', 'a')
    assert (highScore.getHighScore('abcdefg', 'a')[9][1] == 'TEST102')


def testCleanup():
    conn = sqlite3.connect("spellingbee/model/highScore.db")
    cursor = conn.cursor()

    que = 'delete from highScore where name like "TEST%";'

    cursor.execute(que)

    conn.commit()
    conn.close()
