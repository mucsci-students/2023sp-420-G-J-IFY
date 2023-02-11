# Authors: Yah'hymbey Baruti-Bey, Francesco Spagnolo 
# Course : CSCI 420
# Modified Date: 2/2/2023
# A module for making a new puzzle 


#Imports
import sqlite3
from random import randrange
import saveState
import CommandHandler


# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def newPuzzle(baseWord):    
    try:
        uniqueLetters = {}
        if baseWord == '':
            # Finds baseword and its unique letters and puts them in a tuple
            baseTuple = findBaseWord()
            baseWord = baseTuple[0]
            uniqueLetters = baseTuple[1]
            keyLetter = choseKeyLetter(uniqueLetters)
        
        # Checks if word from user is in database
        # and gets the unique letters if so
        else:
            #catch if nonalphas before querey is made to prevent SQL injection
            if not baseWord.isalpha():
                raise BadQueryException
            #querey DB for word
            returnTuple = checkDataBase(baseWord)
            #returnTuple will be None if querey returns emptyy
            if returnTuple == None:
                #Need to catch this exception, this is a known problem that will be addressed before end of sprint 1
                raise BadQueryException
            uniqueLetters = returnTuple[1]
            #need to catch if user enters more than one letter. This is a known probnlem that will be addressed before end of sprint 1
            keyLetter = input("Enter a letter from your word to use as the key letter\n> ")
            keyLetter = keyLetter.lower()
            while keyLetter not in uniqueLetters:
                keyLetter = input(keyLetter + " is not part of " + baseWord + " - Please enter a letter from your word: ")
            
        # Creates the puzzle for users to solve
        puzzle = saveState.Puzzle(keyLetter, uniqueLetters)
        # Populates the puzzles wordlist
        puzzle.wordListStorage()
        # Generates a max score
        puzzle.updateMaxScore()
        # Generates rank
        puzzle.updateRank()
        
        return puzzle
    #Raise exception for bad puzzle seed
    except BadQueryException:
        print(baseWord.upper() + " is not a valid word")
        return CommandHandler.newPuzzle()
    

#Exception used for newPuzzle to catch bad starting words
class BadQueryException(Exception):
    #raised when user has a bad starting word
    pass
    
    
# Finds a legitimate baseword to start puzzle with from the database
# Returns a list
def findBaseWord():
    # SQLite Connections
    wordDict = sqlite3.connect('wordDict.db')

    # Used to execute SQL commands
    wordDictC = wordDict.cursor()
    # Grabs a random baseword from the list
    wordDictC.execute(""" SELECT fullWord, uniqueLetters 
                        FROM pangrams 
                        ORDER BY RANDOM() 
                        Limit 1;
                        """)
    #catch return from querey
    resultResult = (wordDictC.fetchone())

    #close DB
    wordDict.commit()
    wordDict.close()

    #return tuple of result
    return resultResult

# Checks if the given baseword is in the database
# @PARAM baseWord: The user entered word to check the database for
# @RETURN returnResult: a tuple with the query results OR
# @RETURN false if word not in DB
def checkDataBase(baseWord):
    # SQLite Connections
    wordDict = sqlite3.connect('wordDict.db')
    
    # Used to execute SQL commands
    cursor = wordDict.cursor()
    
    cursor.execute("SELECT *FROM pangrams WHERE fullWord = '" + baseWord + "';")
    #grab tuple returned from querey
    returnResult = cursor.fetchone()

    #after result is caught, disconenct from DB
    wordDict.commit()
    wordDict.close()

    #check if none
    #if returnResult != None:
    return returnResult
    #else:
    #    return False

# Params: uniqueLetters: string of unique letters from base word
# Takes a STRING of letters and picks a letter from to make key letter
# Note from Jacob Loveren 2/4/23: Miscommunication on how unqique letters were stored.
# easiest to just pick a random character from the string using RNG instead of trying
# to treat this like a set
def choseKeyLetter(uniqueLetters):    
    return uniqueLetters[randrange(7)]


#params: puzzle object, input that the user gave
#checks the database for valid words, already found words and words that do not exist
def guess(puzzle, input):
    
    input = input.lower()

    conn = sqlite3.connect('wordDict.db')
    cursor = conn.cursor()
        
    #check for every case in the user's guess to give points or output error
    #check for only containing alphabetical characters
    if not input.isalpha():
        print(input + " contains non alphabet characters")
    elif input in puzzle.showAllWords(): #checks words in the word list to see if it is valid for the puzzle
        if input in puzzle.showFoundWords(): #check if it is already found
            print(input.upper() + " was already found!")
        else:
            #query the database to see how many points to give
            query = "select wordScore from dictionary where fullWord = '" + input + "';"
            cursor.execute(query)
            puzzle.updateScore(cursor.fetchone()[0])
            puzzle.updateRank()
            puzzle.updateFoundWords(input)
            print(input.upper() + ' is one of the words!')
    elif len(input) < 4: #if the word is not in the list check the size
        print(input.upper() + " is too short!\nGuess need to be at least 4 letters long")
    else:
        #query the database to see if it is a word at all
        query1 = "select uniqueLetters from dictionary where fullWord = '" + input + "';"
        cursor.execute(query1)
        response = cursor.fetchone()
        if response == None:
            print(input.upper() + " isn't a word in the dictionary")
        elif set(response[0]).issubset(set(puzzle.showUniqueLetters())): #check if the letters contain the center letter
            print(input.upper() + " is missing center letter, " + puzzle.showKeyLetter().upper())
        else:
            #must be letters not in the puzzle in this case
            print(input.upper() + " contains letters not in " + puzzle.showShuffleLetters().upper())
            
    conn.commit()
    conn.close()
