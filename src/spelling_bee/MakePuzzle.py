# Authors: Yah'hymbey Baruti-Bey, 
# Course : CSCI 420
# Modified Date: 1/30/2023
# A module for making a new puzzle 


# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def __NewPuzzle(baseWord):
    if baseWord == "":
        baseWord = findBaseWord()
    # Call Word List Generator
    # Call Show Puzzle
    # Show Status

# Params: userWord: takes a word from the user and makes a puzzle
# Takes a base word from the user and generates a new puzzle from that
def __NewPuzzleFromBase(userWord):
    # Check if the word is a pangram
    if isProperBaseWord(userWord):
    # Call new puzzle
        __NewPuzzle(userWord)


# Params: pangram: takes a suggested pangram and checks if it is a valid base word
# Checks if a word is a pangram
def isProperBaseWord(pangram):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    if len(pangram) < 7:
        raise ValueError("Pangrams must 7 letters or more")
        
    # Checking for anything that is not a letter
    if not pangram.isalpha():
        raise ValueError("Pangrams can only contain letters")
        
    # Puts each unique letter in a list
    uniqueLetters = [i for i in alphabet if i in pangram]
    
    if len(uniqueLetters) < 7:
        raise ValueError("Pangrams contain 7 unique letters")
    
    return True
            
    
# Finds a legitimate baseword to start puzzle with from a json file
def findBaseWord():
    pass