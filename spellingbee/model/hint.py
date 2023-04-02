################################################################################
# hint.py
# Author: Francesco Spagnolo, Yah'hymbey Baruti Ali-Bey
# Date of Creation: 3-20-2023
#
# Makes a hint object to use within the gui and the cli.
# Main functionality includes a 2D list that contains all calculated words
# with specific starting letters and lengths (with sums of each). Additionally,
# a two letter list is provided as a 2D list for all counted instances of words with two
# specific starting characters.
#
# (Global, public) functions:
#   hint() -> hint object
#
# Imports:
#   puzzle
#   sqlite3
#
################################################################################

import puzzle
import sqlite3

################################################################################
# class hint()
# Description:
#   This module is meant to create and store a hint to the puzzle object
#   and have ready to use within the CLI and the GUI.
#
# Arguments:
#   obj: puzzle.Puzzle
#
# <public> Attributes:
#   rows, cols : int tuple
#   hint : list[list[int]]
#   obj.findAllWords : None
#   twoLettList : list[list[int]]
#
# <public> Functions:
#   countWords(self, obj: puzzle.Puzzle) -> int
#     - Counts all of the words in a puzzle
#   
#   makeHintGrid(self, obj: puzzle.Puzzle) -> None
#     - Creates and stores the hint grid with the correct information
#   
#   getHintGrid(self) -> list[list[int]]
#     - Returns the hint grid to the user to use
#   
#   printHint(self)-> None
#     - Prints the hint grid
#   
#   numPangrams(self, obj: puzzle.Puzzle) -> int
#     - Finds the number of total pangrams for a puzzle
#   
#   numPerfectPangram(self, obj: puzzle.Puzzle) -> int
#     - Finds the number of perfect pangrams for a puzzle
#   
#   numTwoLettCombo(self, obj: puzzle.Puzzle) -> int
#     - Calculates the number of two letter combinations for a puzzle
#   
#   twoLetterList(self, obj: puzzle.Puzzle) -> None
#     - Creates and stores the information for the two letter list for a puzzle
#   
#   getTwoLetterList(self) -> list[list[int]]
#     - Returns the two letter list for the user to use
#   
#   printTwoLetterList(self)-> None
#     - Prints the two letter list
#   
################################################################################
class hint:
    def __init__(self, obj: puzzle.Puzzle):
        self.rows, self.cols = (9, 14)
        self.hint = [[0 for i in range(self.cols)] for j in range(self.rows)]
        obj.findAllWords()
        self.twoLettList = [
            [0 for i in range(2)] for j in range(self.numTwoLettCombo(obj))
        ]
        # self.bingo = obj.bingo()

    ############################################################################
    # countWords(obj: puzzle.Puzzle) -> int
    #
    # Description:
    #   Counts the number of words in the entire Puzzle.allWordList
    #
    # Parameters:
    #   obj
    #      The puzzle object to be counted
    ############################################################################
    def countWords(self, obj: puzzle.Puzzle) -> int:
        numWords = len(obj.getAllWords())
        return numWords

    ############################################################################
    # makeHintGrid(obj: puzzle.Puzzle)
    #
    # Description:
    #   Creates the entire 2D list in a nice format
    #
    # Parameters:
    #   obj
    #      The puzzle that needs to be calculated and stored
    ############################################################################
    def makeHintGrid(self, obj: puzzle.Puzzle):
        # Store the letters in their own row
        for i in range(len(obj.getUniqueLetters())):
            self.hint[i + 1][0] = obj.uniqueLett[i]

        # Set fields appropriately
        self.hint[0][0] = ""
        self.hint[8][0] = "Σ"
        self.hint[0][13] = "Σ"
        self.hint[8][13] = self.countWords(obj)

        wordLen = 4
        for x in range(len(self.hint[0]) - 2):
            self.hint[0][x + 1] = wordLen
            wordLen += 1

        # Prepare for keeping track of many values in the loop
        allWords = obj.getAllWords()
        wordLen = 4
        counter = 0
        lett = 0
        total = 0

        # For each letter in uniqueLetters
        for x in range(len(obj.getUniqueLetters())):
            # Check each word in the list of all words
            for i in allWords:
                if len(i) == wordLen:
                    # Word is of correct length so check if it starts with the specific letter
                    for j in range(len(obj.getUniqueLetters())):
                        if i[0] == obj.uniqueLett[lett]:
                            # Count the word and add to the total
                            counter += 1
                            total += 1
                            break
                    # All words of a length counted so record that value
                    self.hint[lett + 1][wordLen - 3] = counter
                else:
                    # New word of next length up
                    counter = 0
                    wordLen += 1
                    # Increment wordLen until it is at the next word of the
                    # correct length
                    if len(i) != wordLen:
                        for z in range(len(i) - wordLen):
                            wordLen += 1

                    if len(i) == wordLen:
                        if i[0] == obj.uniqueLett[lett]:
                            # Count the word and add to the total
                            counter += 1
                            total += 1
                            self.hint[lett + 1][wordLen - 3] = counter

                # Record total since all words have been counted of a starting letter
                self.hint[lett + 1][13] = total
            # Reset variables to count the next words with a new starting letter
            wordLen = 4
            counter = 0
            total = 0
            lett += 1

        # Now we calculate the total of each column
        lenTotal = 0
        # The -1 in both loops for the ranges omits the last column and last row to avoid double counting
        for i in range(len(self.hint[0]) - 1):
            for j in range(len(self.hint) - 2):
                # Add total in this column (i+1 is to skip the first column entirely)
                lenTotal += self.hint[j + 1][i + 1]
            # Record total for this column then set column total to 0
            self.hint[8][i + 1] = lenTotal
            lenTotal = 0

    ############################################################################
    # getHintGrid()
    #
    # Description:
    #   Creates the entire 2D list in a nice format
    #
    # Parameters:
    #   None
    ############################################################################
    def getHintGrid(self) -> list[list[int]]:
        return self.hint

    ############################################################################
    # printHint()
    #
    # Description:
    #   Prints the entire 2D list
    #
    # Parameters:
    #   None
    ############################################################################
    def printHint(self):
        for rows in self.hint:
            print(rows)

    ############################################################################
    # numPangrams()
    #
    # Description:
    #   Gives the number of pangrams for a given puzzle
    #
    # Parameters:
    #   None
    ############################################################################
    def numPangrams(self, obj: puzzle.Puzzle) -> int:
        ulString = obj.getUniqueLetters()
        # SQLite Connections
        wordDict = sqlite3.connect("spellingbee/model/wordDict.db")

        # Used to execute SQL commands
        wordDictC = wordDict.cursor()
        # Grabs a random baseword from the list
        wordDictC.execute(
            """ SELECT COUNT(fullWord)
                        FROM pangrams
                        WHERE uniqueLetters LIKE
                        '"""
            + ulString
            + "';"
        )
        # catch return from querey
        resultResult = wordDictC.fetchone()
        (num,) = resultResult

        # close DB
        wordDict.commit()
        wordDict.close()
        return num

    ############################################################################
    # numPerfectPangram()
    #
    # Description:
    #   Gives the number of perfect pangrams for a given puzzle
    #
    # Parameters:
    #   None
    ############################################################################
    def numPerfectPangram(self, obj: puzzle.Puzzle) -> int:
        ulString = obj.getUniqueLetters()
        # SQLite Connections
        wordDict = sqlite3.connect("spellingbee/model/wordDict.db")

        # Used to execute SQL commands
        wordDictC = wordDict.cursor()
        # Grabs a random baseword from the list
        wordDictC.execute(
            """ SELECT COUNT(pangrams.fullWord)
                        FROM pangrams inner join dictionary ON pangrams.fullWord=dictionary.fullWord
                        WHERE pangrams.uniqueLetters like
                        '"""
            + ulString
            + "' AND wordScore = 14;"
        )
        # catch return from querey
        resultResult = wordDictC.fetchone()
        (num,) = resultResult

        # close DB
        wordDict.commit()
        wordDict.close()
        return num

    ############################################################################
    # numTwoLettCombo(obj: puzzle.Puzzle)
    #
    # Description:
    #   A specific helper for list length to initialize the two letter list
    #   using each two letter combination.
    #
    # Parameters:
    #   obj
    #      puzzle object to create the list from the words in the puzzle
    ############################################################################
    def numTwoLettCombo(self, obj: puzzle.Puzzle) -> int:
        allWords = obj.getAllWords()
        letters = obj.getUniqueLetters()
        counter = 0

        # For each letter
        for i in range(len(obj.getUniqueLetters())):
            # Store that letter
            currLett = letters[i]

            # For each letter
            for j in range(len(obj.getUniqueLetters())):
                # String is first stored letter then second stored letter
                # which checks all two letter combinations
                check = currLett + letters[j]

                # Check each word for a new two letter combination
                for x in allWords:
                    # If it is a new combination, count it and loop back to
                    # check the next new combination.
                    if x.startswith(check):
                        counter += 1
                        break
        return counter

    ############################################################################
    # twoLetterList(obj: puzzle.Puzzle)
    #
    # Description:
    #   Creates the two letter list for a given puzzle
    #
    # Parameters:
    #   obj
    #      puzzle object to create the list from the words in the puzzle
    ############################################################################
    def twoLetterList(self, obj: puzzle.Puzzle):
        allWords = obj.getAllWords()
        letters = obj.getUniqueLetters()
        counter = 0

        # For each letter
        for i in range(len(obj.getUniqueLetters())):
            # Store that letter
            currLett = letters[i]

            # For each letter
            for j in range(len(obj.getUniqueLetters())):
                # String is first stored letter then second stored letter
                # which checks all two letter combinations
                check = currLett + letters[j]

                # Check each word for a new two letter combination
                for x in allWords:
                    # If it is a new combination, store that string in the list,
                    # then count it and loop back to check the next new combination.
                    if x.startswith(check):
                        self.twoLettList[counter][0] = check
                        counter += 1
                        break

        # Now count all the words starting with the set of two letters
        for y in allWords:
            for k in range(len(self.twoLettList)):
                if y.startswith(self.twoLettList[k][0]):
                    self.twoLettList[k][1] += 1

    ############################################################################
    # getTwoLetterList() -> list[list[int]]
    #
    # Description:
    #   Gives the caller the two letter list for a given puzzle
    #
    # Parameters:
    #   None
    ############################################################################
    def getTwoLetterList(self) -> list[list[int]]:
        return self.twoLettList

    ############################################################################
    # printTwoLetterList()
    #
    # Description:
    #   Prints the two letter list for a given puzzle
    #
    # Parameters:
    #   None
    ############################################################################
    def printTwoLetterList(self):
        for rows in self.twoLettList:
            print(rows)


# For displaying and testing functionality, remove comments here
# and play around with any puzzle

# PUZZLES
# newPuzzle = puzzle.Puzzle("a", "acklorw")  # base test puzzle
# newPuzzle = puzzle.Puzzle("s", "eflnpsu")
# newPuzzle = puzzle.Puzzle("n", "cenorsu")
# newPuzzle = puzzle.Puzzle("p", "cenopty")
# newPuzzle = puzzle.Puzzle("e", "aeinrst")  # longest puzzle
# newPuzzle = puzzle.Puzzle("j", "aeijklm")  # shortest puzzle
# newPuzzle = puzzle.Puzzle("i", "einortv")
# hints = hint(newPuzzle)

# HINT GRID
# hints.makeHintGrid(newPuzzle)
# get = hints.getHintGrid()
# hints.printHint()
# print(hints.countWords(newPuzzle))

# TWO LETTER LIST:
# hints.twoLetterList(newPuzzle)
# print(hints.getTwoLetterList())
# hints.printTwoLetterList()
# print(hints.numTwoLettCombo(newPuzzle))

# PANGRAMS
# print(hints.numPangrams(newPuzzle))
# print(hints.numPerfectPangram(newPuzzle))
