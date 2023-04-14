# Author: Francesco Spagnolo
import sys
import os
import model.output
import MakePuzzle as spellingbee
import pytest

outty = model.output.Output()

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)


@pytest.fixture
def puzzleFixture():
    return spellingbee.newPuzzle('friends', 'i', False)


@pytest.fixture
def blankPuzzleFixture():
    return spellingbee.newPuzzle('', '', False)


@pytest.fixture
def nonAlphaPuzzleFixture():
    return spellingbee.newPuzzle(':123@#$', '2', False)


@pytest.fixture
def badPuzzleFixture():
    return spellingbee.newPuzzle('grimer', 'g', False)


@pytest.fixture
def badKeyLettPuzzleFixture():
    return spellingbee.newPuzzle('warlock', '', False)


@pytest.fixture
def extraKeyLettPuzzleFixture():
    return spellingbee.newPuzzle('warlock', 'wa', False)


@pytest.fixture
def wrongKeyLettPuzzleFixture():
    return spellingbee.newPuzzle('warlock', 'e', False)


@pytest.fixture
def guessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, 'friend', False)
    return puzzleFixture


@pytest.fixture
def shortGuessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, "end", False)


@pytest.fixture
def longGuessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, "thisguessistoolongforourgame", False)


@pytest.fixture
def nonalphaGuessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, ":123", False)


@pytest.fixture
def nonsenseGuessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, "notaword", False)


@pytest.fixture
def missingCenterGuessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, "fenders", False)


@pytest.fixture
def wrongLettersGuessFixture(puzzleFixture):
    spellingbee.guess(puzzleFixture, "benders", False)


# test to see if blank puzzle is generated correctly
def testBlankNewPuzzle(blankPuzzleFixture):
    assert (len(blankPuzzleFixture.uniqueLett) == 7)


def testNonAlphaNewPuzzle(nonAlphaPuzzleFixture):
    pytest.raises(spellingbee.BadQueryException)


def testBadNewPuzzle(badPuzzleFixture):
    pytest.raises(spellingbee.BadQueryException)


def testBadKeyLettNewPuzzle(badKeyLettPuzzleFixture):
    pytest.raises(spellingbee.EmptyKeyLetterException)


def testExtraKeyLettNewPuzzle(extraKeyLettPuzzleFixture):
    pytest.raises(spellingbee.TooManyKeyLettersException)


def testWrongKeyLettNewPuzzle(wrongKeyLettPuzzleFixture):
    pytest.raises(spellingbee.LetterMismatchException)


# testing if make puzzle correctly produces a new game
def testKeyLett(puzzleFixture):
    assert (puzzleFixture.keyLett == 'i')


def testUniqueLett(puzzleFixture):
    assert (puzzleFixture.uniqueLett == 'definrs')


def testShuffleLett(puzzleFixture):
    assert (puzzleFixture.shuffleLett == 'definrs')


def testScore(puzzleFixture):
    assert (puzzleFixture.score == 0)


def testMaxScore(puzzleFixture):
    assert (puzzleFixture.maxScore == puzzleFixture.getMaxScore())


def testFoundWordList(puzzleFixture):
    assert (puzzleFixture.foundWordList == [])


def testAllWordList(puzzleFixture):
    assert (puzzleFixture.allWordList == puzzleFixture.getAllWords())


def testRank(puzzleFixture):
    assert (puzzleFixture.rank == 'Beginner')


# test findBaseWord
def testFindBaseWord():
    assert (spellingbee.findBaseWord() is not None)


def testFindBaseWord2():
    assert (spellingbee.findBaseWord() != ('', ''))


# test checkDataBase
def testCheckDB(puzzleFixture):
    assert (spellingbee.checkDataBase(puzzleFixture.uniqueLett) is not False)


# test guess
def testGuessIsInFoundWords(guessFixture):
    assert (guessFixture.getFoundWords() == ['friend'])


def testGuessScoreUpdated(guessFixture):
    assert (guessFixture.getScore() == 6)


def testGuessRankUpdated(guessFixture):
    assert (guessFixture.getRank() == 'Good Start')


def testShortGuess(shortGuessFixture):
    assert (outty.getField() == "END is too short...")


def testLongGuess(longGuessFixture):
    assert (outty.getField() == "Guess is too long...")


def testNonAlphaGuess(nonalphaGuessFixture):
    assert (outty.getField() == ":123 contains non alphabet characters")


def testNonsenseGuess(nonsenseGuessFixture):
    assert (outty.getField() == "NOTAWORD isn't a word...")


def testMissingCenterGuess(missingCenterGuessFixture):
    assert (outty.getField() == "FENDERS is missing center letter, I")


def testWrongLettersGuessFixture(wrongLettersGuessFixture):
    assert (outty.getField() == "BENDERS contains letters not in DEFINRS")
