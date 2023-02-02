# Authors: Yah'hymbey Baruti-Bey, 
# Course : CSCI 420
# Modified Date: 1/30/2023
# A module for making a new puzzle 


#Imports
import sqlite3
import random


# SQLite Connections
wordDict = sqlite3.connect('wordDict.db')

# Used to execute SQL commands
wordDictC = wordDict.cursor()



# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def newPuzzle(baseWord):
    if baseWord == '':
        baseWord = findBaseWord()
        # Query unique letters from database
        uniqueLetters = grabUniquesFromBase(baseWord)
    elif isProperBaseWord(baseWord):
        uniqueLetters = set(baseWord)
    # Call function to determine key letter
    keyLetter = choseKeyLetter(uniqueLetters)
    # Call Word List Generator
    # Shuffle the set
    # Call Show Puzzle
    # Show Status


# Params: pangram: takes a suggested pangram and checks if it is a valid base word
# Checks if a word is a pangram
# Returns a boolean
def isProperBaseWord(pangram):
    
    if len(pangram) < 7:
        raise Exception("Pangrams must 7 letters or more")
        
    # Checking for anything that is not a letter
    if not pangram.isalpha():
        raise Exception("Pangrams can only contain letters")
        
    # Puts each unique letter in a set
    # Checks if the number of unique letters is bigger than 7
    uniqueLetters = set(pangram)
    if len(uniqueLetters) < 7:
        raise Exception("Pangrams contain 7 unique letters")
    
    return True
            
    
# Finds a legitimate baseword to start puzzle with from the database
# Returns a list
def findBaseWord():
    # Grabs a random baseword from the list
    wordDictC.execute("""
                        SELECT fullWord
                        FROM wordDict
                        ORDER BY RANDOM()
                        Limit 1
                      """)
    return wordDictC.fetchone()

# Grabs the unique characters given a baseword
def grabUniquesFromBase(baseWord):
    # Search Database for baseWord
    # If found then grab unqiue letters
    wordDictC.execute("""
                        SELECT uniqueLetters
                        FROM wordDict
                        where fullWord = {baseWord}
                      """)
    print(wordDictC.fetchone())
    return wordDictC.fetchone()

# Takes a set of letters and picks a letter from to make key letter
def choseKeyLetter(uniqueLetters):
    return random.choice(uniqueLetters)


base = findBaseWord()
print(base)
print(grabUniquesFromBase(base))
