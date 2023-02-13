# Author: Francesco Spagnolo

import unittest
#import pytest
import MakePuzzle
import sqlite3
from random import randrange
import saveState
import CommandHandler

class MakePuzzleTests(unittest.TestCase):
    
    # testing if make puzzle correctly produces a new game
    print("for the following prompt enter the letter i for testing purposes")
    obj = MakePuzzle.newPuzzle('friends')
    assert(obj.keyLett == 'i')
    assert(obj.uniqueLett == 'definrs')
    assert(obj.shuffleLett == 'definrs')
    assert(obj.score == 0)
    assert(obj.maxScore == obj.showMaxScore())
    assert(obj.foundWordList == [])
    assert(obj.allWordList == obj.showAllWords())
    assert(obj.rank == 'Beginner')
    print("MakePuzzle: PASSED")
    
    # test findBaseWord
    assert(MakePuzzle.findBaseWord() != None)
    assert(MakePuzzle.findBaseWord() != ('', ''))
    print("findBaseWord: PASSED")
    
    #test checkDataBase
    assert(MakePuzzle.checkDataBase(obj.uniqueLett) != False)
    print("checkDataBase: PASSED")
    
    #test choseKeyLetter
    assert(MakePuzzle.choseKeyLetter(obj.uniqueLett).isalpha())
    assert(len(MakePuzzle.choseKeyLetter(obj.uniqueLett)) == 1)
    print("choseKeyLetter: PASSED")
    
    #test guess
    MakePuzzle.guess(obj, 'friend')
    assert(obj.showFoundWords() == ['friend'])
    assert(obj.showScore() == 6)
    assert(obj.showRank() == 'Good Start')
    print("guess: PASSED")
    
    
if __name__ == '__main__':
    unittest.main()
