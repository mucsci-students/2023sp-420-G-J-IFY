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
import pytest
import model.output
outty = model.output.Output()
from model.puzzle import Puzzle
import MakePuzzle

################################################################################
# TESTS

# new instance with puzzle object
# testConstructor():

@pytest.fixture
def puzzleFixture():
    return MakePuzzle.newPuzzle('warlock', 'a', outty, False)
# countWords() should give proper number of words for a puzzle
def testCountWords(puzzleFixture):
    hints = hint.hint(puzzleFixture)
    test = hints.countWords(puzzleFixture)
    assert(test == hints.countWordsCheck(puzzleFixture))

# TEMPORARY WILL NEED LOTS OF REWORKING
def testMakeHintGrid(puzzleFixture):
    hints = hint.hint(puzzleFixture)
    hints.makeHintGrid(puzzleFixture)
    assert (hints.hint[1][1] == 6)
    assert (hints.hint[2][1] == 12)
    assert (hints.hint[3][1] == 3)
    assert (hints.hint[4][1] == 4)
    assert (hints.hint[8][1] == 37)


#
# testNumPangrams(): Puzzle warlock center letter _ will have _ pangrams
#   if pangrams == 0 then fail
#    elif (query num pangrams) != pangrams then fail
#    else pass
#
