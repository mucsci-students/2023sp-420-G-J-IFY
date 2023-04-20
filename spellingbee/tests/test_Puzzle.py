# authors: Gaige Zakroski
import sys
import os
import pytest
from model.puzzle import Puzzle

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)


@pytest.fixture
def puzzleFixture():
    return Puzzle('a', 'warlock')


@pytest.fixture
def puzzleFixtureHundredScore():
    puzzle = Puzzle('a', 'warlock')
    puzzle.maxScore = 100
    return puzzle


def testEmptyPuzzleKeyLett(puzzleFixture):
    assert (puzzleFixture.keyLett == 'a')


def testEmptyPuzzleUniqueLett(puzzleFixture):
    assert (puzzleFixture.uniqueLett == 'warlock')


def testEmptyPuzzleShuffleLett(puzzleFixture):
    assert (puzzleFixture.shuffleLett == 'warlock')


def testEmptyPuzzleScore(puzzleFixture):
    assert (puzzleFixture.score == 0)


def testEmptyPuzzleMaxScore(puzzleFixture):
    assert (puzzleFixture.maxScore == 0)


def testEmptyPuzzlefoundWords(puzzleFixture):
    assert (puzzleFixture.foundWordList == [])


def testEmptyPuzzleAllWords(puzzleFixture):
    assert (puzzleFixture.allWordList == [])


def testEmptyPuzzleRank(puzzleFixture):
    assert (puzzleFixture.rank == ' ')


def testGetKeyLetter(puzzleFixture):
    assert (puzzleFixture.getKeyLetter() == puzzleFixture.keyLett)


# test getUniqueLetters
def testGetUniqueLetters(puzzleFixture):
    assert (puzzleFixture.getUniqueLetters() == puzzleFixture.uniqueLett)


# test getShuffleLetters
def testGetShuffleLetters(puzzleFixture):
    assert (puzzleFixture.getShuffleLetters() == puzzleFixture.shuffleLett)


# test getMaxScore
def testGetMaxScore(puzzleFixture):
    assert (puzzleFixture.getMaxScore() == puzzleFixture.maxScore)


# testgetFoundWords
def testGetFoundWords(puzzleFixture):
    assert (puzzleFixture.getFoundWords() == puzzleFixture.foundWordList)


# test getAllWords
def testGetAllWords(puzzleFixture):
    assert (puzzleFixture.getAllWords() == puzzleFixture.allWordList)


# testgetScore
def testGetScore(puzzleFixture):
    assert (puzzleFixture.getScore() == puzzleFixture.score)


# test getRank
def testGetRank(puzzleFixture):
    assert (puzzleFixture.getRank() == puzzleFixture.rank)


# testUpdateFoundWords
def testUpdateFoundWordsGood(puzzleFixture):
    puzzleFixture.updateFoundWords('warlock')
    puzzleFixture.updateFoundWords('wrack')
    puzzleFixture.updateFoundWords('wallaroo')
    assert (puzzleFixture.foundWordList == ['warlock', 'wrack', 'wallaroo'])


# test UpdateScore
def testUpdateScore(puzzleFixture):
    puzzleFixture.updateScore(10)
    assert (puzzleFixture.score == 10)


def testUpdateScore2(puzzleFixture):
    puzzleFixture.updateScore(10)
    puzzleFixture.updateScore(30)
    assert (puzzleFixture.score == 40)


# test SetKeyLetter
def testSetKeyLetter(puzzleFixture):
    puzzleFixture.setKeyLetter('b')
    assert (puzzleFixture.keyLett == 'b')


# test SetUniqueLetters
def testSetKeyLetter2(puzzleFixture):
    puzzleFixture.setUniqueLetters('barnical')
    assert (puzzleFixture.uniqueLett == 'barnical')


# test SetShuffleLetters
def testShuffleLetters(puzzleFixture):
    puzzleFixture.setShuffleLetters('barnical')
    assert (puzzleFixture.shuffleLett == 'barnical')


# test SetScore
def testSetScore(puzzleFixture):
    puzzleFixture.setScore(100)
    assert (puzzleFixture.score == 100)


# test SetMaxScore
def testSetScore2(puzzleFixture):
    puzzleFixture.setMaxScore(200)
    assert (puzzleFixture.maxScore == 200)


# test SetFoundWords
def testSetFoundWords(puzzleFixture):
    list = ["warlock", "wrack", "alcool", "arrack", "wallaroo"]
    puzzleFixture.setFoundWords(list)
    assert (puzzleFixture.getFoundWords() == ["warlock", "wrack", "alcool",
                                              "arrack", "wallaroo"])


# test SetAllWordList
def testSetAllWordList(puzzleFixture):
    puzzleFixture.setAllWordList(["warlock", "wrack", "alcool", "arrack",
                                  "wallaroo", "cloacal", "corolla", "wallow",
                                  "corral"])
    assert (puzzleFixture.allWordList == ["warlock", "wrack", "alcool",
                                          "arrack", "wallaroo", "cloacal",
                                          "corolla", "wallow", "corral"])


# test  SetRank
def testSetRank(puzzleFixture):
    puzzleFixture.setRank('Queen Bee')
    assert (puzzleFixture.rank == 'Queen Bee')


# test UpdateRank
def testUpdateRank(puzzleFixture):
    puzzleFixture.setMaxScore(200)
    puzzleFixture.setScore(100)
    puzzleFixture.updateRank()
    assert (puzzleFixture.rank == "Great")


# test ShuffleChars
def testShuffleChars(puzzleFixture):
    puzzleFixture.shuffleChars()
    assert (puzzleFixture.shuffleLett != puzzleFixture.uniqueLett)


def testGetFinishedFlag(puzzleFixture):
    puzzleFixture.finishedFlag = True
    assert (puzzleFixture.getFinishedFlag() is True)


def testSetFinishedFlag(puzzleFixture):
    puzzleFixture.setFinishedFlag(True)
    assert (puzzleFixture.finishedFlag is True)


def testGetPointsTilRank(puzzleFixture):
    assert (puzzleFixture.getPointsTilRank() == 1)


def testSetKeyLetter4(puzzleFixture):
    puzzleFixture.setKeyLetter('z')
    assert (puzzleFixture.getKeyLetter() == 'z')


def testSetUniqueLetters(puzzleFixture):
    puzzleFixture.setUniqueLetters('abcdefg')
    assert (puzzleFixture.uniqueLett == 'abcdefg')


def testCheckBingoNewGame(puzzleFixture):
    assert (puzzleFixture.checkBingo() is False)


def testCheckBingoGood(puzzleFixture):
    puzzleFixture.setFoundWords(['warlock', 'lock', 'crack', 'arco', 'kaka',
                                 'rack', 'orca'])
    assert (puzzleFixture.checkBingo() is True)


def testRank1(puzzleFixtureHundredScore):
    puzzleFixtureHundredScore.score = 24
    puzzleFixtureHundredScore.updateRank()
    assert (puzzleFixtureHundredScore.rank == 'Solid')


def testRank2(puzzleFixtureHundredScore):
    puzzleFixtureHundredScore.score = 33
    puzzleFixtureHundredScore.updateRank()
    assert (puzzleFixtureHundredScore.rank == 'Nice')


def testRank3(puzzleFixtureHundredScore):
    puzzleFixtureHundredScore.score = 59
    puzzleFixtureHundredScore.updateRank()
    assert (puzzleFixtureHundredScore.rank == 'Amazing')


def testRank4(puzzleFixtureHundredScore):
    puzzleFixtureHundredScore.score = 99
    puzzleFixtureHundredScore.updateRank()
    assert (puzzleFixtureHundredScore.rank == 'Genius')


def testConcatEmpty(puzzleFixture):
    assert (puzzleFixture.concatFound() == "Nothing yet...")


def testConcatFull(puzzleFixture):
    list = ["warlock", "wrack", "alcool"]
    puzzleFixture.setFoundWords(list)
    assert (puzzleFixture.concatFound() == "WARLOCK WRACK ALCOOL ")


def testUpdateScoreFinished(puzzleFixture):
    puzzleFixture.setMaxScore(100)
    puzzleFixture.setScore(puzzleFixture.getMaxScore())
    puzzleFixture.updateRank()
    assert (puzzleFixture.getRank() == "Queen Bee")


def testUpdateScore1(puzzleFixture):
    puzzleFixture.setMaxScore(100)
    puzzleFixture.setScore(11)
    puzzleFixture.updateRank()
    assert (puzzleFixture.getRank() == "Good")
