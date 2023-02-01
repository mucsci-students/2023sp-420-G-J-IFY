# Authors: Yah'hymbey Baruti-Bey, 
# Course : CSCI 420
# Modified Date: 1/30/2023
# A module for making a new puzzle 


#Imports
import json

# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def newPuzzle(baseWord):
    if baseWord == "":
        baseWord = findBaseWord()
    uniqueLetters = set(baseWord)
    # Call function to determine key letter
    # Call Word List Generator
    # Shuffle the set
    # Call Show Puzzle
    # Show Status

# Params: userWord: takes a word from the user and makes a puzzle
# Takes a base word from the user and generates a new puzzle from that
def newPuzzleFromBase(userWord):
    # Check if the word is a pangram
    if isProperBaseWord(userWord):
    # Call new puzzle
        newPuzzle(userWord)


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
            
    
# Finds a legitimate baseword to start puzzle with from a json file
def findBaseWord():
    # Gets list of from json file
    # Finds length of the list
    # picks a random word within the range
    # returns that word
    pass