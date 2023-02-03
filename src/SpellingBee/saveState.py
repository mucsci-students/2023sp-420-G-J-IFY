# Authors: Yah'hymbey Baruti-Bey, Jacob Lovegren
# Course : CSCI 420
# Modified Date: 2/2/2023
# State structure for puzzles

import sqlite3

# SQLite Connections
wordDict = sqlite3.connect('wordDict.db')

# Used to execute SQL commands
wordDictC = wordDict.cursor()

class Puzzle:

    # Tuple list for point threshold Ex. [('Beginner', 0), ('Novice', 11)]
    
    def __init__(self, keyLett, pangram):
        self.keyLett = keyLett
        self.pangram = pangram
        self.score = 0
        self.foundWordList = []
        self.rank = ' '
    
    def showKeyLetter(self):
        return self.keyLett
    
    def showUniqueLetters(self):
        return set(self.pangram)
    
    # Word List generated when given key letter and word
    # All words for current puzzle
    def wordListStorage():
        pass
    
    # Returns a number
    def showMaxScore(self):
        # Aggregate the point list in the database
        return 0
    
    # Returns a string of all the words
    def showFoundWords(self):
        outStr = " "
        return outStr.join(self.foundWordList)
    
    # Current User Score
    def showScore(self):
        return self.score
    
    # Display the current rank
    def showRank(self):
        return self.rank
    
    # list of pangrams that goto current puzzle
    def pangramList():
        pass
    
    # Updates the list of found words
    def updateFoundWords(self, word):
        self.foundWordList.append(word)
    
    def updateScore(self, pointIncrease):
        self.score += pointIncrease
    
    def updateRank():
        pass
    
    # Params: pangram: takes a suggested pangram and checks if it is a valid base word
    # Checks if a word is a pangram
    # Returns a boolean
    def isProperBaseWord(pangram):
        if len(pangram) < 7:
            return False
        
        # Checking for anything that is not a letter
        if not pangram.isalpha():
            return False
        
        # Puts each unique letter in a set
        # Checks if the number of unique letters is bigger than 7
        uniqueLetters = set(pangram)
        if len(uniqueLetters) < 7:
            return False
    
        return True
    
    