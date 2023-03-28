# Author: Francesco Spagnolo
import sys
import os
import model.output
outty = model.output.Output()
current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import unittest

#import spellingbee
from random import randrange
import MakePuzzle as spellingbee
import pytest

@pytest.fixture
def puzzleFixture():
    return spellingbee.newPuzzle('friends', 'i', outty, False)

@pytest.fixture
def guessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, 'friend', False, outty)
    return puzzleFixture



    
    # testing if make puzzle correctly produces a new game
def testKeyLett(puzzleFixture):
    assert(puzzleFixture.keyLett == 'i')

def testUniqueLett(puzzleFixture):
    assert(puzzleFixture.uniqueLett == 'definrs')

def testShuffleLett(puzzleFixture):
    assert(puzzleFixture.shuffleLett == 'definrs')

def testScore(puzzleFixture):
    assert(puzzleFixture.score == 0)

def testMaxScore(puzzleFixture):
    assert(puzzleFixture.maxScore == puzzleFixture.getMaxScore())

def testFoundWordList(puzzleFixture):
    assert(puzzleFixture.foundWordList == [])

def testAllWordList(puzzleFixture):
    assert(puzzleFixture.allWordList == puzzleFixture.getAllWords())

def testRank(puzzleFixture):
    assert(puzzleFixture.rank == 'Beginner')
    
    # test findBaseWord
def testFindBaseWord():
    assert(spellingbee.findBaseWord() != None)

def testFindBaseWord2():
    assert(spellingbee.findBaseWord() != ('', ''))
    
    #test checkDataBase
def testCheckDB(puzzleFixture):
    assert(spellingbee.checkDataBase(puzzleFixture.uniqueLett) != False)
    

    #test guess
    
def testGuessIsInFoundWords(guessFixture):
    assert(guessFixture.getFoundWords() == ['friend'])

def testGuessScoreUpdated(guessFixture):
    assert(guessFixture.getScore() == 6)

def testGuessRankUpdated(guessFixture):
    assert(guessFixture.getRank() == 'Good Start')
    
