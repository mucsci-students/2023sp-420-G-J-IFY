# Authors: Yah'hymbey Baruti-Bey, Jacob Lovegren, Francesco Spagnolo, Gaige Zakroski
# Course : CSCI 420
# Modified Date: 2/2/2023
# State structure for puzzles

import sqlite3
import generateSubset

class Puzzle:
    
    def __init__(self, keyLett, uniqueLett):
        self.keyLett = keyLett
        self.uniqueLett = uniqueLett
        self.score = 0
        self.maxScore = 0
        self.foundWordList = []
        self.allWordList = []
        self.rank = ' '
        
    def showKeyLetter(self):
        return self.keyLett
    
    # Returns the set of unique letters
    def showUniqueLetters(self):
        return self.uniqueLett
    
    # Word List generated when given key letter and word
    # All words for current puzzle
    def wordListStorage(self):
       self.allWordList = generateSubset.getAllWordsFromPangram(self)
    
    # Returns a number
    def showMaxScore(self):
        return self.maxScore

    # Returns a string of all the words
    def showFoundWords(self):
        outStr = " "
        return outStr.join(self.foundWordList)

    # Returns a string of all the valid words for a puzzle
    def showAllWords(self):
        outStr = " "
        return outStr.join(self.allWordList)
    
    # Current User Score
    def showScore(self):
        return self.score
    
    # Display the current rank
    def showRank(self):
        return self.rank
    
    # Updates the list of found words
    def updateFoundWords(self, word):
        self.foundWordList.append(word)
    
    def updateScore(self, pointIncrease):
        self.score += pointIncrease

    # params: letter - the manditory character
    # sets the key letter of the puzzle
    def setKeyLetter(self, letter):
        self.keyLett = letter
    
    # params: uniqueLetters - the set of unique letters
    # sets the unique letters to a set of unique letters
    def setUniqueLetters(self, uniqueLetters):
        self.uniqueLett = uniqueLetters
    
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
    
    # params : newRank - string of the rank
    # sets the rank to the new rank
    def setRank(self, newRank):
        self.rank = newRank


    

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
            self.rank ==  "Good Start"
        elif currentPercent < 0.08:
            self.rank == "Moving Up"
        elif currentPercent < 0.15:
            self.rank == "Good"
        elif currentPercent < 0.25:
            self.rank == "Solid"
        elif self.rank < 0.4:
            self.rank == "Nice"
        elif self.rank < 0.51:
            self.rank == "Great"
        elif self.rank < 0.71:
            self.rank == "Amazing"
        elif self.rank < 1:
            self.rank == "Genius"
        else: #all words found
            self.rank == "Queen Bee"
        
    
    #findMaxScore - this functions takes a list of words 
    #for a game, quereies the DB for all words in the game,
    #and adds together the total possible points for the given pangram
    #@PARAM listList, a list of strings containing all words in DB
    #   for given pangram 
    #@RETURN maxScore, the total possible score for a starting word
    def updateMaxScore(self):
        #connect to DB
        conn = sqlite3.connect('src/SpellingBee/wordDict.db')
        cursor = conn.cursor()
    
        ctr = 0

        print(type(self.allWordList))

        #loop through list, querey DB for each word, aggregate values
        for a in self.allWordList:
            query = """select wordScore
            from dictionary
            where fullWord = '""" + self.allWordList[ctr] + "';"
            cursor.execute(query)
            self.maxScore += cursor.fetchone()[0]
            ctr += 1

        #close DB
        conn.commit()
        conn.close()


#test Code
#warlock = acklorw
#newPuzz = Puzzle('a', 'acklorw')
#newPuzz.wordListStorage()
#print(newPuzz.showAllWords())