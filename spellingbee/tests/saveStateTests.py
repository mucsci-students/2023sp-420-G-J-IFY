# authors: Gaige Zakroski
import sys
import os
import pytest

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)
#import spellingbee
import unittest
import model.puzzle as Puzzle



@pytest.fixture
def puzzleFixture():
    return Puzzle.Puzzle('a', 'warlock')

def testEmptyPuzzleKeyLett(puzzleFixture):
    assert(puzzleFixture.keyLett == 'a')

def testEmptyPuzzleUniqueLett(puzzleFixture):
    assert(puzzleFixture.uniqueLett == 'warlock')

def testEmptyPuzzleShuffleLett(puzzleFixture):
    assert(puzzleFixture.shuffleLett == 'warlock')

def testEmptyPuzzleScore(puzzleFixture):
    assert(puzzleFixture.score == 0)

def testEmptyPuzzleMaxScore(puzzleFixture):
    assert(puzzleFixture.maxScore == 0)

def testEmptyPuzzlefoundWords(puzzleFixture):
    assert(puzzleFixture.foundWordList == [])

def testEmptyPuzzleAllWords(puzzleFixture):
    assert(puzzleFixture.allWordList == [])

def testEmptyPuzzleRank(puzzleFixture):
    assert(puzzleFixture.rank == ' ')
puzzleFixture
def testGetKeyLetter(puzzleFixture):
    assert(puzzleFixture.getKeyLetter() == puzzleFixture.keyLett)
        
    # test getUniqueLetters
def testGetUniqueLetters(puzzleFixture):
    assert(puzzleFixture.getUniqueLetters() == puzzleFixture.uniqueLett)
        
    # test getShuffleLetters
def testGetShuffleLetters(puzzleFixture):
    assert(puzzleFixture.getShuffleLetters() == puzzleFixture.shuffleLett)

    # test getMaxScore
def testGetMaxScore(puzzleFixture):
    assert(puzzleFixture.getMaxScore() == puzzleFixture.maxScore )
        
    # testgetFoundWords
def testGetFoundWords(puzzleFixture):
    assert(puzzleFixture.getFoundWords() == puzzleFixture.foundWordList)

    # test getAllWords
def testGetAllWords(puzzleFixture):
    assert(puzzleFixture.getAllWords() == puzzleFixture.allWordList)
    
    # testgetScore
def testGetScore(puzzleFixture):
    assert(puzzleFixture.getScore() == puzzleFixture.score)
    
    # test getRank
def testGetRank(puzzleFixture):
    assert(puzzleFixture.getRank() == puzzleFixture.rank)

    # testUpdateFoundWords
def testUpdateFoundWordsGood()
    puzzleFixture.updateFoundWords('warlock')
    puzzleFixture.updateFoundWords('wrack')
    puzzleFixture.updateFoundWords('wallaroo')
    assert(puzzleFixture.foundWordList == ['warlock', 'wrack', 'wallaroo'])
       

    #test UpdateScore
    puzzleFixture.updateScore(10)
    assert(puzzleFixture.score == 10)
    puzzleFixture.updateScore(30)
    assert(puzzleFixture.score == 40)

    # test SetKeyLetter
    puzzleFixture.setKeyLetter('b')
    assert(puzzleFixture.keyLett == 'b')

    # test SetUniqueLetters
    puzzleFixture.setUniqueLetters('barnical')
    assert(puzzleFixture.uniqueLett == 'barnical')
        
    # test SetShuffleLetters
    puzzleFixture.setShuffleLetters('barnical')
    assert(puzzleFixture.shuffleLett == 'barnical')
        
    # test SetScore
    puzzleFixture.setScore(100)
    assert(puzzleFixture.score == 100)

    # test SetMaxScore
    puzzleFixture.setMaxScore(200)
    assert(puzzleFixture.maxScore == 200)

    # test SetFoundWords
    list = ["warlock", "wrack", "alcool", "arrack", "wallaroo"]
    puzzleFixture.setFoundWords(list)
    assert(puzzleFixture.getFoundWords() == ["warlock", "wrack", "alcool", "arrack", "wallaroo"])
       
    # test SetAllWordList
    puzzleFixture.setAllWordList(["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
    assert(puzzleFixture.allWordList == ["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
       
    # test  SetRank
    puzzleFixture.setRank('Queen Bee')
    assert(puzzleFixture.rank == 'Queen Bee')
      
    # test UpdateRank
    puzzleFixture.updateRank()
    assert(puzzleFixture.rank == "Great")
       
    # test ShuffleChars 
    puzzleFixture.shuffleChars()
    assert( not puzzleFixture.shuffleLett == puzzleFixture.uniqueLett)
       

if __name__ == '__main__':
    unittest.main()
    