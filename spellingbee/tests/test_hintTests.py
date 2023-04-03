###############################################################################
# hintTests.py
# Author: Francesco Spagnolo
# Date of Creation: 03-27-2023
#
# This module is the test code for hint and the hint object to ensure
# functionality across all files and objects.
#
###############################################################################

import hint
import pytest
import model.output
import MakePuzzle


outty = model.output.Output()


###############################################################################
# TESTS


@pytest.fixture
def puzzleFixture():
    return MakePuzzle.newPuzzle('stainer', 'e', outty, False)


def testConstructor(puzzleFixture: object):
    hint.hint(puzzleFixture)


# countWords() should give proper number of words for a puzzle
def testCountWords(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    hints.countWords(puzzleFixture)


def testMakeHintGrid(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    hints.makeHintGrid(puzzleFixture)
    assert (hints.makeHintGrid(puzzleFixture) is None)

    rowTotal = 0
    colTotal = 0
    for row in range(hints.rows - 1):
        for i in range(hints.cols - 2):
            rowTotal += hints.hint[row + 1][i + 1]
        assert (rowTotal == hints.hint[row + 1][13])
        row += 1
        rowTotal = 0

    for col in range(hints.cols - 2):
        for j in range(hints.rows - 2):
            colTotal += hints.hint[j + 1][col + 1]
        assert (colTotal == hints.hint[8][col + 1])
        col += 1
        colTotal = 0


def testGetHintGrid(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    hints.getHintGrid()
    assert (hints.getHintGrid() is not None)


def testPrintHint(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    hints.printHint()
    assert (hints.printHint() is None)


def testNumPangrams(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    assert (hints.numPangrams(puzzleFixture) == 88)


def testNumPerfectPangram(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    assert (hints.numPerfectPangram(puzzleFixture) == 9)


def testTwoLetterList(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    hints.twoLetterList(puzzleFixture)


def testGetTwoLetterList(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    hints.getTwoLetterList()
    assert (hints.getTwoLetterList is not None)


def testPrintTwoLetterList(puzzleFixture: object):
    hints = hint.hint(puzzleFixture)
    hints.printTwoLetterList()
    assert (hints.printTwoLetterList() is None)
