################################################################################
# StateStorage.py
# Author: Yah'hymbey Baruti-Bey, Jacob Lovegren, Francesco Spagnolo, Gaige Zakroski
# Date of Creation: 2-2-2023
################################################################################


import sqlite3
#import model.generateSubset as generateSubset
import random
import sqlite3
import itertools
from model import dbFixer
from itertools import chain, combinations

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
#   pointsTilRank: int
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
#   getPointsTilRank() -> int
#     - returns the points needed until the next rank
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
#   setPointsTilRank(points: int)
#     - sets the points til rank 
#   findAllWords()
#     - generates a list of valid guessable words
#   updateFoundWords(word: str)
#     - adds a word to the found word list
#   updateScore(pointIncrease: int)
#     - adds pointIncrease to the score
#   updateRank()
#     - updates puzzle rank based off score
#   calcPointsTilRank(rankPer : double)
#     - updates the points til rank based on current max and level
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
        self.pointsTilRank = 1
    
    ############################################################################
    # getKeyLetter() -> str
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
    def getKeyLetter(self):
        return self.keyLett
    
    ############################################################################
    # getUniqueLetters() -> str
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
    def getUniqueLetters(self):
        return self.uniqueLett

    ############################################################################
    # getShuffleLetters() -> str
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
    def getShuffleLetters(self):
        return self.shuffleLett

    ############################################################################
    # getMaxScore() -> int
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
    def getMaxScore(self):
        return self.maxScore

    ############################################################################
    # getFoundWords() -> list
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
    def getFoundWords(self):
        return self.foundWordList

    #
    ############################################################################
    # getAllWords() -> list
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
    def getAllWords(self):
        return self.allWordList

    ############################################################################
    # getScore() -> int
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
    def getScore(self):
        return self.score

    ############################################################################
    # getRank() -> str
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
    def getRank(self):
        return self.rank
    
    ############################################################################
    # getFinishedFlag() - bool
    #
    # Description:
    #   display the finished flag
    #
    # Returns:
    #   self.finishedFlag
    #       bool value
    ############################################################################
    def getFinishedFlag(self):
        return self.finishedFlag
    

    ############################################################################
    # getPointsTilRank() - int
    #
    # Description:
    #   returns the points needed until next level
    #
    # Returns:
    #   self.pointsTilRank
    #       int value
    ############################################################################
    def getPointsTilRank(self):
        return self.pointsTilRank

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
    # setPointsTilRank(points)
    #
    # Description:
    #   sets the points til rank up
    #
    # Parameters:
    #   points
    #       points needed to rank up
    ############################################################################
    def setPointsTilRank(self, points):
        self.pointsTilRank = round(points)

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
       self.allWordList = self.getAllWordsFromPangram(self.uniqueLett, self.keyLett)

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
            self.setPointsTilRank(1)
        elif currentPercent < 0.05:
            self.rank =  "Good Start"
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
        else: #all words found
            self.rank = "Queen Bee"
            #set final flag
            self.setFinishedFlag(True)
            self.setPointsTilRank(0)

    ############################################################################
    # calcPointsTilRank(rankPer)
    #
    # Description:
    #   calcPointsTilRank takes a decimal for the next rank up and determines
    #   how many points are needed to hit that rank
    #
    # Parameters:
    #   rankPer
    #       a floating point number for the next rank to hit
    ############################################################################
    def calcPointsTilRank(self, rankPer):
        self.setPointsTilRank(self.maxScore * rankPer - self.score)

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
        letters = random.sample(self.getUniqueLetters(), len(self.getUniqueLetters()))

        #looping through to find the main letter in shuffled list
        ctr = 0    
        while ctr < 7: 
            if self.getKeyLetter() == letters[ctr]:
                #copy whatever is in front of the line to later
                letters[ctr] = letters[0]
                #repalce first char with key letter
                letters[0] = self.getKeyLetter() 
                break
            ctr += 1
        #set the shuffleLetters field to the list rejoined to string
        self.setShuffleLetters(''.join(letters))


    ################################################################################
    # getAllWordsFromPangram(puzz : Puzzle Object) -> list
    # DESCRIPTION:
    #   This function generates all the words for a given puzzle.
    #
    # PARAMETERS:
    #   puzz : Puzzle
    #       - the Puzzle object where the needed letters are pulled from
    #
    # RETURNS:
    #   list
    #       - a list of all the possible words for the given puzzle
    ################################################################################
    def getAllWordsFromPangram(self, unique, key) -> list: #unclear how to add the puzzle type to this line
        #create powerset of letters from baseword
        pSet = list(self.powerset(unique))
        cleanSet = []

        #remove sets from powerset to produce subset with keyletter
        for a in pSet:
            if key in a:
                cleanSet.append(self.sortStrToAlphabetical(''.join(a)))
        
        #Time to querey the DB   
        dbFixer.goToDB()
        conn = sqlite3.connect('wordDict.db')
        cursor = conn.cursor()

        #create temp table to use for natural joins soon
        tempTable = "create temporary table validLetters (uniLetts);"
        cursor.execute(tempTable)
    
        #Build out tempTable for join later
        querey = "insert into validLetters (uniLetts) values ('"
        for a in cleanSet:
            querey += a + "'), ('"
        querey += "');"
        cursor.execute(querey)
        
        #build out query using joins
        join = """
                select fullWord from dictionary join validLetters 
                on dictionary.uniqueLetters is validLetters.uniLetts;
                """
        cursor.execute(join)
        
        #catch return form query
        tuples = (cursor.fetchall())
        #turn list of tuples into list of strings
        listList = list(itertools.chain(*tuples))
        #close DB
        conn.commit()
        conn.close()
        dbFixer.leaveDB()

        #return list of valid words
        return listList


    ################################################################################
    # powerset(iterable) -> set
    #
    # DESCRIPTION:
    #   This is a helper funciton for generateAllWordsFromPangram()
    #
    #   This function takes an iterable object and returns a powerset of that
    #   iterable object. 
    #   
    #   A power set is all the possible subset combinations of the set.
    #       i.e. powerst (abc) -> a, b, c, ab, ac, bc, abc
    #
    # PARAMETERS: 
    #   iterable : ITERABLE OBJECT
    #       - any iterable object, in this case, a string of unique letters
    #       - 'abcdefg'
    #
    # RETURNS:
    #   Set
    #       - a powerset of the iterable object
    ################################################################################
    
    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


    ################################################################################
    # sortStrToAlphabetical(unsorted : str) -> str
    #
    # DESCRIPTION:
    #   This function takes a string and alphabetizes the letters within
    #
    # PARAMETERS:
    #   unsorted : str
    #       - "warlock"
    #
    # RETURNS:
    #   str
    #       -"acklorw"
    ################################################################################
    def sortStrToAlphabetical(self, unsorted : str) -> str:
        uniqueLettersList = sorted(set(unsorted))
        #convert list to string
        return ''.join(uniqueLettersList)

