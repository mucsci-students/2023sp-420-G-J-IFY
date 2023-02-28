# Author: Francesco Spagnolo
import sys
import os


current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import unittest

import src
import sqlite3
from random import randrange

class MakePuzzleTests(unittest.TestCase):
    
    # testing if make puzzle correctly produces a new game
    print("for the following prompt enter the letter i for testing purposes")
    obj = src.newPuzzle('friends', False)
    assert(obj.keyLett == 'i')
    assert(obj.uniqueLett == 'definrs')
    assert(obj.shuffleLett == 'definrs')
    assert(obj.score == 0)
    assert(obj.maxScore == obj.getMaxScore())
    assert(obj.foundWordList == [])
    assert(obj.allWordList == obj.getAllWords())
    assert(obj.rank == 'Beginner')
    print("MakePuzzle: PASSED")
    
    # test findBaseWord
    assert(src.findBaseWord() != None)
    assert(src.findBaseWord() != ('', ''))
    print("findBaseWord: PASSED")
    
    #test checkDataBase
    assert(src.checkDataBase(obj.uniqueLett) != False)
    print("checkDataBase: PASSED")
    

    #test guess
    src.guess(obj, 'friend', False)
    assert(obj.getFoundWords() == ['friend'])
    assert(obj.getScore() == 6)
    assert(obj.getRank() == 'Good Start')
    print("guess: PASSED")
    
    
if __name__ == '__main__':
    unittest.main()
