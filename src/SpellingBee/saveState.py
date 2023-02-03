# Authors: Yah'hymbey Baruti-Bey, Jacob Lovegren
# Course : CSCI 420
# Modified Date: 2/2/2023
# State structure for puzzles

import sqlite3
import generateSubset

class Puzzle:
    
    def __init__(self, keyLett, pangram):
        self.keyLett = keyLett
        self.pangram = pangram
        self.score = 0
        self.maxScore = 0
        self.foundWordList = []
        self.rank = ' '
        
    def showKeyLetter(self):
        return self.keyLett
    
    def showUniqueLetters(self):
        return set(self.pangram)
    
    # Word List generated when given key letter and word
    # All words for current puzzle
    def wordListStorage(self):
       return generateSubset.getAllWordsFromPuzzle(self.pangram, self.keylett)
    
    sdfd
    # Returns a number
    def showMaxScore(self):
        return self.maxScore

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
    
    # Updates the list of found words
    def updateFoundWords(self, word):
        self.foundWordList.append(word)
    
    def updateScore(self, pointIncrease):
        self.score += pointIncrease
    
    def updateRank(self):
        pass
    
    #findMaxScore - this functions takes a list of words 
    #for a game, quereies the DB for all words in the game,
    #and adds together the total possible points for the given pangram
    #@PARAM listList, a list of strings containing all words in DB
    #   for given pangram 
    #@RETURN maxScore, the total possible score for a starting word
    def updateMaxScore(self, listList):
        #connect to DB
        conn = sqlite3.connect('src/SpellingBee/wordDict.db')
        cursor = conn.cursor()
    
        ctr = 0
        #loop through list, querey DB for each word, aggregate values
        for a in listList:
            query = """select wordScore
            from dictionary
            where fullWord = '""" + listList[ctr] + "';"
            cursor.execute(query)
            self.maxScore += cursor.fetchone()[0]
            ctr += 1

        #close DB
        conn.commit()
        conn.close()
    
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
    
    