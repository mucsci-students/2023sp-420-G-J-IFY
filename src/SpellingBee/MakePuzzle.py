# Authors: Yah'hymbey Baruti-Bey, 
# Course : CSCI 420
# Modified Date: 2/2/2023
# A module for making a new puzzle 


#Imports
import sqlite3
import random
import saveState


# SQLite Connections
wordDict = sqlite3.connect('wordDict.db')

# Used to execute SQL commands
wordDictC = wordDict.cursor()



# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def newPuzzle(baseWord):
    # Add check if baseWord is in the database
    
    uniqueLetters = {}
    if baseWord == '':
        # Finds baseword and its unique letters and puts them in a tuple
        baseTuple = findBaseWord()
        baseWord = baseTuple[0]
        uniqueLetters = set(baseTuple[1])
    keyLetter = choseKeyLetter(uniqueLetters)
    NewPuzzle = saveState.Puzzle(keyLetter, uniqueLetters)
    # Call Word List Generator
    NewPuzzle.wordListStorage()
    # Gets Proper max score
    NewPuzzle.updateMaxScore(NewPuzzle.wordListStorage())
    
    # Call Show Puzzle
    # Show Status
    
    
    
# Finds a legitimate baseword to start puzzle with from the database
# Returns a list
def findBaseWord():
    # Grabs a random baseword from the list
    wordDictC.execute(""" SELECT fullWord, uniqueLetters 
                        FROM pangrams 
                        ORDER BY RANDOM() 
                        Limit 1
                        """)

    return wordDictC.fetchone()

# Params: uniqueLetters: set of uniqueLetters from a baseword
# Takes a SET of letters and picks a letter from to make key letter
def choseKeyLetter(uniqueLetters):
    return random.choice(uniqueLetters)

