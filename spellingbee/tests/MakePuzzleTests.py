# Author: Francesco Spagnolo
import sys
import os
import model.output as output
outty = output.Output()
current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import unittest

#import spellingbee
import sqlite3
from random import randrange
import model.MakePuzzle as spellingbee

class MakePuzzleTests(unittest.TestCase):
    
    # testing if make puzzle correctly produces a new game
    obj = spellingbee.newPuzzle('friends', 'i', outty, False)
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
    assert(spellingbee.findBaseWord() != None)
    assert(spellingbee.findBaseWord() != ('', ''))
    print("findBaseWord: PASSED")
    
    #test checkDataBase
    assert(spellingbee.checkDataBase(obj.uniqueLett) != False)
    print("checkDataBase: PASSED")
    

    #test guess
    spellingbee.guess(obj, 'friend', False, outty)
    assert(obj.getFoundWords() == ['friend'])
    assert(obj.getScore() == 6)
    assert(obj.getRank() == 'Good Start')
    print("guess: PASSED")
    
    #huge
if __name__ == '__main__':
    unittest.main()
