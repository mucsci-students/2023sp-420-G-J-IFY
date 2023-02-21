################################################################################
# StateStorage.py
# Author: Yah'hymbey Baruti-Bey, Jacob Lovegren, Francesco Spagnolo, Gaige Zakroski
# Date of Creation: 2-2-2023
################################################################################


import sqlite3
import model.generateSubset as generateSubset
import random

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
        
    def showKeyLetter(self):
        return self.keyLett
    
    # Returns the string of unique letters
    def showUniqueLetters(self):
        return self.uniqueLett

    # returns a string of the letters to shuffle freely
    def showShuffleLetters(self):
        return self.shuffleLett
    
    # Returns a number
    def showMaxScore(self):
        return self.maxScore

    # Returns a list of all the found words
    def showFoundWords(self):
        return self.foundWordList

    #returns a list of all the words for a given puzzle
    def showAllWords(self):
        return self.allWordList

    # Current User Score int
    def showScore(self):
        return self.score
    
    # Display the current rank
    def showRank(self):
        return self.rank
    
    #display the finished flag
    def showFinishedFlag(self):
        return self.finishedFlag

    # params: letter - the manditory character
    # sets the key letter of the puzzle
    def setKeyLetter(self, letter):
        self.keyLett = letter
    
    # params: uniqueLetters - the string of unique letters
    # string the unique letters to a set of unique letters
    def setUniqueLetters(self, uniqueLetters):
        self.uniqueLett = uniqueLetters
    
    #params: shuffle letters - the string of shuffled letters
    #to be messed with freely, with shuffleLetters[0] being the key
    def setShuffleLetters(self, shuffleLetters):
        self.shuffleLett = shuffleLetters

    # params: gameScore - score of a game
    # sets the score to a specified score
    def setScore(self, gameScore):
        self.score = gameScore
    
    # params: maxGameScore -  max score of a game
    # sets the max score of a game
    def setMaxScore(self, maxGameScore):
        self.maxScore = maxGameScore

    # params : foundWords - list of found words
    # sets the foundWordList to another list of found words
    def setFoundWords(self, foundWords):
        self.foundWordList = foundWords
    
    # Params: wordList - list of all posible words for puzzle
    # sets the allWordList to a given word list
    def setAllWordList(self, wordList):
        self.allWordList = wordList
    
    # params : newRank - string of the rank
    # sets the rank to the new rank
    def setRank(self, newRank):
        self.rank = newRank

    # Params : update - the new status of the flag
    # sets the finished flag to the update
    def setFinishedFlag(self, update):
        self.finishedFlag = update

    # Word List generated when given key letter and word
    # All words for current puzzle
    def findAllWords(self):
       self.allWordList = generateSubset.getAllWordsFromPangram(self)

    # Updates the list of found words
    def updateFoundWords(self, word):
        self.foundWordList.append(word)
    
    def updateScore(self, pointIncrease):
        self.score += pointIncrease

    # updateRank takes a puzzle object, checks its
    # current score against the max score for the puzzle,
    # and sets the rank field to the appropriate
    # level
    # @PRARM self - A puzzle object
    # @RETURN string with appropriate rank
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
        

    #shuffleChars reshuffles the string of letters to display to the user
    #set shuffleLetters
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



