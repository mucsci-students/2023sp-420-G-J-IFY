################################################################################
# hint.py
# Author: Francesco Spagnolo,
# Date of Creation: 3-20-2023
#
# Makes a hint object to use within the gui and the cli
#
#
################################################################################
import sqlite3
import puzzle
import dbFixer

# import pytest


class hint:
    def __init__(self, obj: puzzle):
        rows, cols = (8, 12)
        self.hint = [[0 for i in range(cols)] for j in range(rows)]
        obj

    def printHint(self):
        for rows in self.hint:
            print(rows)

    def countWords(self, obj) -> int:
        numWords = 0
        for i in obj.getAllWords():
            numWords += 1
            # i += 1?
        return numWords

    def makeHintGrid(self, obj):
        for i in range(len(obj.getUniqueLetters())):
            self.hint[i][0] = obj.uniqueLett[i]

        self.hint[7][0] = "Σ"

        for word in obj.getAllWords():
            pass

    #        fchar = words.charAt(0)
    #      find array that matches fchar
    #      len = word.len
    #      find comlumn that matches this length
    #      array[fchar][len]++

    def numPangrams() -> int:
        pass

    def numPerfectPangram() -> int:
        pass

    def twoLetterList():
        # needs return type
        pass


newPuzzle = puzzle.Puzzle("a", "acklorw")
hints = hint(newPuzzle)
hints.makeHintGrid(newPuzzle)
hints.printHint()


#
#
# TWO LETTER CLASS (derived from hints class)
# calcTwoLetters()
#
#
#
# TEMP TESTS
#
# new instance with puzzle object
# testConstructor():
#
def testCountWords():
    newPuzzle = puzzle.Puzzle("a", "acklorw")
    test = hint(newPuzzle).countWords()
    assert test == 108


#
#
def testMakeHintGrid():
    newPuzzle = puzzle.Puzzle("a", "acklorw")
    hints = hint(newPuzzle)
    hints.makeHintGrid(newPuzzle)
    hints.printHint()
    assert ()  # todo


#
# testNumPangrams(): Puzzle warlock center letter _ will have _ pangrams
#   if pangrams == 0 then fail
#    elif (query num pangrams) != pangrams then fail
#    else pass
#
