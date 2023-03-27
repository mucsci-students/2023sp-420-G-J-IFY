################################################################################
# hintTests.py
# Author: Francesco Spagnolo
# Date of Creation: 03-27-2023
#
# This module is the test code for hint and the hint object to ensure
# functionality across all files and objects. 
#
################################################################################

import hint
import puzzle
#import pytest

################################################################################
# TESTS

# new instance with puzzle object
# testConstructor():

# countWords() should give proper number of words for a puzzle
def testCountWords():
    newPuzzle = puzzle.Puzzle("a", "acklorw")
    test = hint(newPuzzle).countWords()
    assert(test == hint.countWordsCheck(newPuzzle))

# TEMPORARY WILL NEED LOTS OF REWORKING
def testMakeHintGrid():
    newPuzzle = puzzle.Puzzle("a", "acklorw")
    hints = hint(newPuzzle)
    hints.makeHintGrid(newPuzzle)
    hints.printHint()
    assert (hints[0][1] == 6)
    assert (hints[1][1] == 12)
    assert (hints[2][1] == 3)
    assert (hints[3][1] == 4)
    assert (hints[7][1] == 37)


#
# testNumPangrams(): Puzzle warlock center letter _ will have _ pangrams
#   if pangrams == 0 then fail
#    elif (query num pangrams) != pangrams then fail
#    else pass
#
