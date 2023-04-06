###############################################################################
# StateStorage.py
# Author: Yah'hymbey Baruti-Bey, Jacob Lovegren,
#    Francesco Spagnolo, Gaige Zakroski
# Date of Creation: 2-2-2023
###############################################################################

import random
import MakePuzzle


###############################################################################
# class Puzzle()
# Description:
#   A description of the class
#
# Arguments:
#   keyLett : str
#   uniqueLett : set
#
# <public> Attributes:
#   keyLett : str
#   uniqueLett : set
#   shuffleLett : set
#   score : int
#   maxScore : int
#   foundWordList: list
#   allWordList: list
#   rank: str
#   finishedFlag: bool
#   pointsTilRank: int
#
# <public> Functions:
#   getKeyLetter() -> str
#     - Returns the key letter of the puzzle
#   getUniqueLetters() -> set
#     - Returns the set of unique letters
#   getShuffleLetters() -> set
#     - Returns the set of uniques letters that can be shuffled
#   getMaxScore() -> int
#     - Returns the max possible score for the puzzle
#   getFoundWords() -> list
#     - Returns a list of the found words
#   getAllWords() -> list
#     - Returns a list of all possible words for the puzzle
#   getScore() -> int
#     - Returns the current score of the game
#   getRank() -> str
#     - Returns the a current rank of the player
#   getFinishedFlag() -> bool
#     - Returns whether the game is finished or not
#   getPointsTilRank() -> int
#     - Returns the points needed until the next rank
#   setKeyLetter(letter: str)
#     - Takes a given key letter and set to a key letter in the puzzle
#   setUniqueLetters(uniqueLetters: set)
#     - Takes a set of uniques letters and set to unique letters in puzzle
#   setShuffleLetters(shuffleLetters: set)
#     - Sets given shuffleLetters set to shuffleLettes in puzzle
#   setScore(gameScore: int)
#     - Takes a score and sets it to the score in puzzle
#   setMaxScore(maxGameScore: int)
#     - Sets max score of the game
#   setFoundWords(foundWords: list)
#     - Sets the found words list
#   setAllWordList(wordList: list)
#     - Sets the availiable word list
#   setRank(newRank: str)
#     - Sets the rank of the puzzle
#   setFinishedFlag(update: bool)
#     - Sets the finished flag in puzzle
#   setPointsTilRank(points: int)
#     - Sets the points til rank
#   checkBingo() -> bool
#     - Parses the words list to determine if the game has a bingo
#   findAllWords()
#     - Generates a list of valid guessable words
#   updateFoundWords(word: str)
#     - Adds a word to the found word list
#   updateScore(pointIncrease: int)
#     - Adds pointIncrease to the score
#   updateRank()
#     - Updates puzzle rank based off score
#   calcPointsTilRank(rankPer : double)
#     - Updates the points til rank based on current max and level
#   shuffleChars()
#     - Shuffles the order or shuffle letter list
###############################################################################

class Puzzle:
    def __init__(self, keyLett, uniqueLett):
        self.keyLett = keyLett
        self.uniqueLett = uniqueLett
        self.shuffleLett = uniqueLett
        self.score = 0
        self.maxScore = 0
        self.foundWordList = []
        self.allWordList = []
        self.rank = " "
        self.finishedFlag = False
        self.pointsTilRank = 1

    ###########################################################################
    # getKeyLetter() -> str
    #
    # Description:
    #   Displays the key letter of the puzzle
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.keyLett
    #       The puzzles key letter
    ###########################################################################
    def getKeyLetter(self):
        return self.keyLett

    ###########################################################################
    # getUniqueLetters() -> str
    #
    # Description:
    #   Returns the string of unique letters
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.uniqueLett
    #       String of unique letters in the puzzle
    ###########################################################################
    def getUniqueLetters(self):
        return self.uniqueLett

    ###########################################################################
    # getShuffleLetters() -> str
    #
    # Description:
    #   Returns a string of the unique letters to shuffle freely
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.shuffleLett
    #       String of unique letters
    ###########################################################################
    def getShuffleLetters(self):
        return self.shuffleLett

    ###########################################################################
    # getMaxScore() -> int
    #
    # Description:
    #   Returns max score for the puzzle
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.maxScore
    #       Integer
    ###########################################################################
    def getMaxScore(self):
        return self.maxScore

    ###########################################################################
    # getFoundWords() -> list
    #
    # Description:
    #   Returns a list of all the found words guessed by user
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.foundWordList
    #       List of found words
    ###########################################################################
    def getFoundWords(self):
        return self.foundWordList

    #
    ###########################################################################
    # getAllWords() -> list
    #
    # Description:
    #   Returns a list of all the words for a given puzzle
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.allWordList
    #       List of all available guessable words
    ###########################################################################
    def getAllWords(self):
        return self.allWordList

    ###########################################################################
    # getScore() -> int
    #
    # Description:
    #   Current user scores
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.score
    #       User score
    ###########################################################################
    def getScore(self):
        return self.score

    ###########################################################################
    # getRank() -> str
    #
    # Description:
    #   Returns a string with the current rank
    #
    # Parameters:
    #   None
    #
    # Returns:
    #   self.rank
    #       Current rank
    ###########################################################################
    def getRank(self):
        return self.rank

    ###########################################################################
    # getFinishedFlag() - bool
    #
    # Description:
    #   Display the finished flag
    #
    # Returns:
    #   self.finishedFlag
    #       bool value
    ###########################################################################
    def getFinishedFlag(self):
        return self.finishedFlag

    ###########################################################################
    # getPointsTilRank() - int
    #
    # Description:
    #   Returns the points needed until next level
    #
    # Returns:
    #   self.pointsTilRank
    #       int value
    ###########################################################################
    def getPointsTilRank(self):
        return self.pointsTilRank

    ###########################################################################
    # setKeyLetter(letter: str)
    #
    # Description:
    #   Sets the key letter of the puzzle
    #
    # Parameters:
    #   letter
    #       The manditory character
    ###########################################################################
    def setKeyLetter(self, letter):
        self.keyLett = letter

    ###########################################################################
    # setUniqueLetters(uniqueLetters: str)
    #
    # Description:
    #   String the unique letters to a set of unique letters
    #
    # Parameters:
    #   uniqueLetters
    #       The string of unique letters
    ###########################################################################
    def setUniqueLetters(self, uniqueLetters):
        self.uniqueLett = uniqueLetters

    ###########################################################################
    # setShuffleLetters(shuffleLetters: str)
    #
    # Description:
    #   To be messed with freely, with shuffleLetters[0] being the key
    #
    # Parameters:
    #   shuffleLetters
    #       The string of shuffled letters
    ###########################################################################
    def setShuffleLetters(self, shuffleLetters):
        self.shuffleLett = shuffleLetters

    ###########################################################################
    # setScore(gameScore: int)
    #
    # Description:
    #   Sets the score to a specified score
    #
    # Parameters:
    #   gameScore
    #       Score of a game
    ###########################################################################
    def setScore(self, gameScore):
        self.score = gameScore

    ###########################################################################
    # setMaxScore(maxGameScore: int)
    #
    # Description:
    #   Sets the max score of a game
    #
    # Parameters:
    #   maxGameScore
    #       Max score of a game
    ###########################################################################
    def setMaxScore(self, maxGameScore):
        self.maxScore = maxGameScore

    ###########################################################################
    # setFoundWords(foundWords: list)
    #
    # Description:
    #   Sets the foundWordList to another list of found words
    #
    # Parameters:
    #   foundWords
    #       List of found words
    ###########################################################################
    def setFoundWords(self, foundWords):
        self.foundWordList = foundWords

    ###########################################################################
    # setAllWordList(wordList: list)
    #
    # Description:
    #  Sets the allWordList to a given word list
    #
    # Parameters:
    #   wordList
    #       List of all posible words for puzzle
    ###########################################################################
    def setAllWordList(self, wordList):
        self.allWordList = wordList

    ###########################################################################
    # setRank(newRank: str)
    #
    # Description:
    #   Sets the rank to the new rank
    #
    # Parameters:
    #   newRank
    #       String of the rank
    ###########################################################################
    def setRank(self, newRank):
        self.rank = newRank

    ###########################################################################
    # setFinishedFlag(update)
    #
    # Description:
    #   Sets the finished flag to the update
    #
    # Parameters:
    #   update
    #       The new status of the flag
    ###########################################################################
    def setFinishedFlag(self, update):
        self.finishedFlag = update

    ###########################################################################
    # setPointsTilRank(points)
    #
    # Description:
    #   Sets the points til rank up
    #
    # Parameters:
    #   points
    #       Points needed to rank up
    ###########################################################################
    def setPointsTilRank(self, points):
        self.pointsTilRank = round(points)

    ###########################################################################
    # checkBingo(self) -> bool
    #
    # Description:
    #   Makes of list of the first letter of all found words
    #   checks to see if length of list is 7
    #
    # Parameters:
    #   None
    ###########################################################################
    def checkBingo(self):
        if self.foundWordList == []:
            return False
        bingoList = []

        for each in self.foundWordList:
            if each[0] not in bingoList:
                bingoList.append(each[0])
            if len(bingoList) == 7:
                break
        return len(bingoList) == 7

    ###########################################################################
    # findAllWords(self)
    #
    # Description:
    #   Word List generated when given key letter and word
    #   All words for current puzzle
    #
    # Parameters:
    #   None
    ###########################################################################

    def findAllWords(self):
        self.allWordList = MakePuzzle.getAllWordsFromPangram(
            self.uniqueLett, self.keyLett
        )

    ###########################################################################
    # updateFoundWords(word)
    #
    # Description:
    #   Updates the list of found words
    #
    # Parameters:
    #   word
    #     New found word
    ###########################################################################
    def updateFoundWords(self, word):
        self.foundWordList.append(word)

    ###########################################################################
    # updateScore(pointIncrease: int)
    #
    # Description:
    #   Increases the score of the puzzle
    #
    # Parameters:
    #   pointIncrease
    #       Number of points to increase by
    ###########################################################################
    def updateScore(self, pointIncrease):
        self.score += pointIncrease

    ###########################################################################
    # updateRank()
    #
    # Description:
    #   updateRank takes a puzzle object, checks its
    #   current score against the max score for the puzzle,
    #   and sets the rank field to the appropriate level
    #
    # Parameters:
    #   None
    ###########################################################################
    def updateRank(self):
        currentPercent = self.score / self.maxScore
        if currentPercent == 0:
            self.rank = "Beginner"
            self.setPointsTilRank(1)
        elif currentPercent < 0.05:
            self.rank = "Good Start"
            self.calcPointsTilRank(0.05)
        elif currentPercent < 0.08:
            self.rank = "Moving Up"
            self.calcPointsTilRank(0.08)
        elif currentPercent < 0.15:
            self.rank = "Good"
            self.calcPointsTilRank(0.15)
        elif currentPercent < 0.25:
            self.rank = "Solid"
            self.calcPointsTilRank(0.25)
        elif currentPercent < 0.4:
            self.rank = "Nice"
            self.calcPointsTilRank(0.4)
        elif currentPercent < 0.51:
            self.rank = "Great"
            self.calcPointsTilRank(0.51)
        elif currentPercent < 0.71:
            self.rank = "Amazing"
            self.calcPointsTilRank(0.71)
        elif currentPercent < 1:
            self.rank = "Genius"
            self.calcPointsTilRank(1)
        else:  # All words found
            self.rank = "Queen Bee"
            # Set final flag
            self.setFinishedFlag(True)
            self.setPointsTilRank(0)

    ###########################################################################
    # calcPointsTilRank(rankPer)
    #
    # Description:
    #   calcPointsTilRank takes a decimal for the next rank up and determines
    #   how many points are needed to hit that rank
    #
    # Parameters:
    #   rankPer
    #       A floating point number for the next rank to hit
    ###########################################################################
    def calcPointsTilRank(self, rankPer):
        self.setPointsTilRank(self.maxScore * rankPer - self.score)

    ###########################################################################
    # shuffleChars()
    #
    # Description:
    #   ShuffleChars reshuffles the string of letters to display to the user
    #
    # Parameters:
    #   None
    ###########################################################################
    def shuffleChars(self):
        # Strings are imutable, need a place to temporarily hold
        #   new shuffle pattern
        # Explode into list
        letters = random.sample(self.getUniqueLetters(),
                                len(self.getUniqueLetters()))

        # Looping through to find the main letter in shuffled list
        ctr = 0
        while ctr < 7:
            if self.getKeyLetter() == letters[ctr]:
                # Copy whatever is in front of the line to later
                letters[ctr] = letters[0]
                # Repalce first char with key letter
                letters[0] = self.getKeyLetter()
                break
            ctr += 1
        # Set the shuffleLetters field to the list rejoined to string
        self.setShuffleLetters("".join(letters))
