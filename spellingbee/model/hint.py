################################################################################
# hint.py
# Author: Francesco Spagnolo,
# Date of Creation: 3-20-2023
#
# Makes a hint object to use within the gui and the cli.
# Main functionality includes a 2D list that contains all calculated words
# with specific starting letters and lengths (with sums of each). Additionally,
# a two letter list is provided for all counted instances of words with two
# specific starting characters.
#
################################################################################
import puzzle
import MakePuzzle

# import sqlite3


class hint:
    def __init__(self, obj: puzzle.Puzzle):
        rows, cols = (8, 14)
        self.hint = [[0 for i in range(cols)] for j in range(rows)]
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
    # countWordsCheck(obj: puzzle.Puzzle) -> int
    #
    # Description:
    #   Used as an assurance for countWords() for correctness
    #
    # Parameters:
    #   obj
    #      Object to be lengthed
    ############################################################################
    def countWordsCheck(obj: puzzle.Puzzle) -> int:
        return len(
            MakePuzzle.getAllWordsFromPangram(
                obj.getUniqueLetters(), obj.getKeyLetter()
            )
        )

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
            self.hint[i][0] = obj.uniqueLett[i]

        # Set fields appropriately
        self.hint[7][0] = "Σ"
        self.hint[7][13] = self.countWords(obj)

        # Prepare for keeping track of many values in the loop
        allWords = obj.getAllWords()
        wordLen = 4
        counter = 0
        lett = 0
        total = 0

        # For each letter
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
                    self.hint[lett][wordLen - 3] = counter
                else:
                    # New word of next length up
                    counter = 0
                    wordLen += 1
                    if len(i) != wordLen:
                        for i in range((wordLen - len(i)) - 1):
                            wordLen += 1

                    if len(i) == wordLen:
                        if i[0] == obj.uniqueLett[lett]:
                            # Count the word and add to the total
                            counter += 1
                            total += 1
                            if allWords[len(allWords) - 1 : len(allWords)] != []:
                                self.hint[lett][wordLen - 3] = counter

                # Record total since all words have been counted of a starting letter
                self.hint[lett][13] = total
            # Reset variables to count the next words with a new starting letter
            wordLen = 4
            counter = 0
            total = 0
            lett += 1

        # Now we calculate the total of each column
        lenTotal = 0
        # The -1 in both loops for the ranges omits the last column and last row to avoid double counting
        for i in range(len(self.hint[0]) - 1):
            for j in range(len(self.hint) - 1):
                # The -2 here checks if the i is at column 12, which is the last column
                if i == len(self.hint[0]) - 2:
                    # If it is, -1 to be at column 11
                    # i -= 1
                    pass
                # Add total in this column (i+1 is to skip the first column entirely)
                lenTotal += self.hint[j][i + 1]
            # Record total for this column then set column total to 0
            self.hint[7][i + 1] = lenTotal
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
    def numPangrams() -> int:
        pass

    ############################################################################
    # numPerfectPangram()
    #
    # Description:
    #   Gives the number of perfect pangrams for a given puzzle
    #
    # Parameters:
    #   None
    ############################################################################
    def numPerfectPangram() -> int:
        pass

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
# newPuzzle = puzzle.Puzzle("a", "acklrow")
# newPuzzle = puzzle.Puzzle("s", "eflnpsu")
# newPuzzle = puzzle.Puzzle("n", "cenorsu")
# newPuzzle = puzzle.Puzzle("p", "cenopt")
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
