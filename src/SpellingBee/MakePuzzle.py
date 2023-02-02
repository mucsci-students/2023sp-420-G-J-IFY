# Authors: Yah'hymbey Baruti-Bey, 
# Course : CSCI 420
# Modified Date: 1/30/2023
# A module for making a new puzzle 


#Imports
import json
import sqlite3

# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def newPuzzle(baseWord):
    if baseWord == '':
        baseWord = findBaseWord()
    else:
        if isProperBaseWord(baseWord):
            newPuzzle(baseWord)
    # Call the unique letters from the databese
    # Call function to determine key letter
    # Call Word List Generator
    # Shuffle the set
    # Call Show Puzzle
    # Show Status


# Params: pangram: takes a suggested pangram and checks if it is a valid base word
# Checks if a word is a pangram
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
def findBaseWord():
    pass

# Takes a set of letters and picks a letter from to make key letter
def choseKeyLetter(uniqueLetters):
    pass