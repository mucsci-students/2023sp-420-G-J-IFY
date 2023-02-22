################################################################################
# StateStorage.py
# Author: Yah'hymbey Baruti-Bey, Jacob Lovegren, Francesco Spagnolo, Gaige Zakroski
# Date of Creation: 2-2-2023
################################################################################


import sqlite3
#import model.generateSubset as generateSubset
import random
import model.MakePuzzle as makePuzzle

################################################################################
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
#
# <public> Functions:
#   getKeyLetter() -> str
#     - returns the key letter of the puzzle
#   getUniqueLetters() -> set
#     - returns the set of unique letters
#   getShuffleLetters() -> set
#     - returns the set of uniques letters that can be shuffled
#   getMaxScore() -> int
#     - returns the max possible score for the puzzle
#   getFoundWords() -> list
#     - returns a list of the found words
#   getAllWords() -> list
#     - returns a list of all possible words for the puzzle
#   getScore() -> int
#     - returns the current score of the game
#   getRank() -> str
#     - returns the a current rank of the player
#   getFinishedFlag() -> bool
#     - returns whether the game is finished or not
#   setKeyLetter(letter: str)
#     - takes a given key letter and set to a key letter in the puzzle
#   setUniqueLetters(uniqueLetters: set)
#     - takes a set of uniques letters and set to unique letters in puzzle
#   setShuffleLetters(shuffleLetters: set)
#     - sets given shuffleLetters set to shuffleLettes in puzzle
#   setScore(gameScore: int)
#     - takes a score and sets it to the score in puzzle 
#   setMaxScore(maxGameScore: int)
#     - sets max score of the game
#   setFoundWords(foundWords: list)
#     - sets the found words list
#   setAllWordList(wordList: list)
#     - sets the availiable word list
#   setRank(newRank: str)
#     - sets the rank of the puzzle
#   setFinishedFlag(update: bool)
#     - sets the finished flag in puzzle
#   findAllWords()
#     - generates a list of valid guessable words
#   updateFoundWords(word: str)
#     - adds a word to the found word list
#   updateScore(pointIncrease: int)
#     - adds pointIncrease to the score
#   updateRank()
#     - updates puzzle rank based off score
#   shuffleChars()
#     - shuffles the order or shuffle letter list
################################################################################
class Puzzle:
    
    def __init__(self, keyLett, uniqueLett):
        self.keyLett = keyLett
        self.uniqueLett = uniqueLett
        self.shuffleLett = uniqueLett
        self.score = 0
        self.maxScore = 0
        self.foundWordList = []
        self.allWordList = []
        self.rank = ' '
        self.finishedFlag = False
    
    ############################################################################
    # showKeyLetter() -> str
    #
    # Description:
    #   displays the key letter of the puzzle
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.keyLett
    #       the puzzles key letter
    ############################################################################
    def showKeyLetter(self):
        return self.keyLett
    
    ############################################################################
    # showUniqueLetters() -> str
    #
    # Description:
    #   Returns the string of unique letters
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.uniqueLett
    #       string of unique letters in the puzzle
    ############################################################################
    def showUniqueLetters(self):
        return self.uniqueLett

    ############################################################################
    # showShuffleLetters() -> str
    #
    # Description:
    #   returns a string of the unique letters to shuffle freely
    #
    # Parameters:
    #   none 
    #
    # Returns:
    #   self.shuffleLett
    #       string of unique letters
    ############################################################################
    def showShuffleLetters(self):
        return self.shuffleLett

    ############################################################################
    # showMaxScore() -> int
    #
    # Description:
    #   returns max score for the puzzle
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.maxScore
    #       integer
    ############################################################################
    def showMaxScore(self):
        return self.maxScore

    ############################################################################
    # showFoundWords() -> list
    #
    # Description:
    #   Returns a list of all the found words guessed by user
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.foundWordList
    #       list of found words
    ############################################################################
    def showFoundWords(self):
        return self.foundWordList

    #
    ############################################################################
    # showAllWords() -> list
    #
    # Description:
    #   returns a list of all the words for a given puzzle
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.allWordList
    #       list of all available guessable words
    ############################################################################
    def showAllWords(self):
        return self.allWordList

    ############################################################################
    # showScore() -> int
    #
    # Description:
    #   current user scores
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.score
    #       user score
    ############################################################################
    def showScore(self):
        return self.score

    ############################################################################
    # showRank() -> str
    #
    # Description:
    #   returns a string with the current rank
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.rank
    #       current rank
    ############################################################################
    def showRank(self):
        return self.rank
    
    ############################################################################
    # getFinishedFlag() - bool
    #
    # Description:
    #   display the finished flag
    #
    # Parameters:
    #   none
    #
    # Returns:
    #   self.finishedFlag
    #       bool value
    ############################################################################
    def showFinishedFlag(self):
        return self.finishedFlag

    ############################################################################
    # setKeyLetter(letter: str)
    #
    # Description:
    #   sets the key letter of the puzzle
    #
    # Parameters:
    #   letter
    #       the manditory character
    ############################################################################
    def setKeyLetter(self, letter):
        self.keyLett = letter
    
    ############################################################################
    # setUniqueLetters(uniqueLetters: str)
    #
    # Description:
    #   string the unique letters to a set of unique letters
    #
    # Parameters:
    #   uniqueLetters
    #       the string of unique letters
    ############################################################################
    def setUniqueLetters(self, uniqueLetters):
        self.uniqueLett = uniqueLetters

    ############################################################################
    # setShuffleLetters(shuffleLetters: str)
    #
    # Description:
    #   to be messed with freely, with shuffleLetters[0] being the key
    #
    # Parameters:
    #   shuffleLetters
    #       the string of shuffled letters
    ############################################################################
    def setShuffleLetters(self, shuffleLetters):
        self.shuffleLett = shuffleLetters

    ############################################################################
    # setScore(gameScore: int)
    #
    # Description:
    #   sets the score to a specified score
    #
    # Parameters:
    #   gameScore
    #       score of a game
    ############################################################################
    def setScore(self, gameScore):
        self.score = gameScore
    
    ############################################################################
    # setMaxScore(maxGameScore: int)
    #
    # Description:
    #   sets the max score of a game
    #
    # Parameters:
    #   maxGameScore
    #       max score of a game
    ############################################################################
    def setMaxScore(self, maxGameScore):
        self.maxScore = maxGameScore

    ############################################################################
    # setFoundWords(foundWords: list)
    #
    # Description:
    #   sets the foundWordList to another list of found words
    #
    # Parameters:
    #   foundWords
    #       list of found words
    ############################################################################
    def setFoundWords(self, foundWords):
        self.foundWordList = foundWords
    
    ############################################################################
    # setAllWordList(wordList: list)
    #
    # Description:
    #  sets the allWordList to a given word list
    #
    # Parameters:
    #   wordList
    #       list of all posible words for puzzle
    ############################################################################
    def setAllWordList(self, wordList):
        self.allWordList = wordList
    
    ############################################################################
    # setRank(newRank: str)
    #
    # Description:
    #   sets the rank to the new rank
    #
    # Parameters:
    #   newRank
    #       string of the rank
    ############################################################################
    def setRank(self, newRank):
        self.rank = newRank

    ############################################################################
    # setFinishedFlag(update)
    #
    # Description:
    #   sets the finished flag to the update
    #
    # Parameters:
    #   update
    #       the new status of the flag
    ############################################################################
    def setFinishedFlag(self, update):
        self.finishedFlag = update

    ############################################################################
    # findAllWords(self)
    #
    # Description:
    #   Word List generated when given key letter and word
    #   All words for current puzzle
    #
    # Parameters:
    #   none
    ############################################################################
    def findAllWords(self):
       self.allWordList = makePuzzle.getAllWordsFromPangram(self)

    ############################################################################
    # updateFoundWords(word)
    #
    # Description:
    #   Updates the list of found words
    #
    # Parameters:
    #   word
    #     new found word
    ############################################################################
    def updateFoundWords(self, word):
        self.foundWordList.append(word)
    
    ############################################################################
    # updateScore(pointIncrease: int)
    #
    # Description:
    #   increases the score of the puzzle
    #
    # Parameters:
    #   pointIncrease
    #       number of points to increase by
    ############################################################################
    def updateScore(self, pointIncrease):
        self.score += pointIncrease

    ############################################################################
    # updateRank()
    #
    # Description:
    #   updateRank takes a puzzle object, checks its
    #   current score against the max score for the puzzle,
    #   and sets the rank field to the appropriate level
    #
    # Parameters:
    #   none
    ############################################################################
    def updateRank(self):
        currentPercent = self.score / self.maxScore
        if currentPercent == 0:
            self.rank = "Beginner"
        elif currentPercent < 0.05:
            self.rank =  "Good Start"
        elif currentPercent < 0.08:
            self.rank = "Moving Up"
        elif currentPercent < 0.15:
            self.rank = "Good"
        elif currentPercent < 0.25:
            self.rank = "Solid"
        elif currentPercent < 0.4:
            self.rank = "Nice"
        elif currentPercent < 0.51:
            self.rank = "Great"
        elif currentPercent < 0.71:
            self.rank = "Amazing"
        elif currentPercent < 1:
            self.rank = "Genius"
        else: #all words found
            self.rank = "Queen Bee"
            #set final flag
            self.setFinishedFlag(True)
        
    ############################################################################
    # shuffleChars()
    #
    # Description:
    #   shuffleChars reshuffles the string of letters to display to the user
    #
    # Parameters:
    #   none
    ############################################################################
    def shuffleChars(self):
        #strings are imutable, need a place to temporarily hold new shuffle pattern
        #explode into list
        letters = random.sample(self.showUniqueLetters(), len(self.showUniqueLetters()))

        #looping through to find the main letter in shuffled list
        ctr = 0    
        while ctr < 7: 
            if self.showKeyLetter() == letters[ctr]:
                #copy whatever is in front of the line to later
                letters[ctr] = letters[0]
                #repalce first char with key letter
                letters[0] = self.showKeyLetter() 
                break
            ctr += 1
        #set the shuffleLetters field to the list rejoined to string
        self.setShuffleLetters(''.join(letters))



