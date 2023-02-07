# Authors: Yah'hymbey Baruti-Bey, Francesco Spagnolo 
# Course : CSCI 420
# Modified Date: 2/2/2023
# A module for making a new puzzle 


#Imports
import sqlite3
import random
#import saveState


# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def newPuzzle(baseWord):    
    uniqueLetters = {}
    if baseWord == '':
        # Finds baseword and its unique letters and puts them in a tuple
        baseTuple = findBaseWord()
        baseWord = baseTuple[0]
        uniqueLetters = baseTuple[1]
        keyLetter = choseKeyLetter(uniqueLetters)
    
    # Checks if word from user is in database
    # and getts the unique letters if so
    else:
        returnTuple = checkDataBase(baseWord)
        #returnTuple will be None if querey returns emptyy
        if returnTuple == None:
            raise Exception("Word not in database.")
        uniqueLetters = returnTuple[1]
        keyLetter = input("Enter a letter from your word to use as the key letter: ")
        while keyLetter not in uniqueLetters:
            keyLetter = input(keyLetter + " is not part of " + baseWord + " - Please enter a letter from your word: ")
    
        # If not an empty string
        # and not in databasee raise and exception
        #else:
        #    raise Exception("Word not in database.")

    
    
# Finds a legitimate baseword to start puzzle with from the database
# Returns a list
def findBaseWord():
    # SQLite Connections
    wordDict = sqlite3.connect('src/SpellingBee/wordDict.db')

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
    wordDict = sqlite3.connect('src/SpellingBee/wordDict.db')
    
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
    from random import randrange
    return uniqueLetters[randrange(7)]


#params: puzzle object, input that the user gave
#checks the database for valid words, already found words and words that do not exist
def guess(puzzle, input):
    
    conn = sqlite3.connect('src/SpellingBee/wordDict.db')
    cursor = conn.cursor()
        
    #check for every case in the user's guess to give points or output error
    if input in puzzle.showAllWords(): #checks words in the word list to see if it is valid for the puzzle
        if input in puzzle.showFoundWords(): #check if it is already found
            print("Already Found")
        else:
            #query the database to see how many points to give
            query = "select wordScore from dictionary where fullWord = '" + input + "';"
            cursor.execute(query)
            puzzle.updateScore(cursor.fetchone()[0])
            #
            #
            # this is where python is giving me guff. For whatever reason, 
            # it doesn't like that we're passing in a string to append it
            # to a list. 
            #
            #
            puzzle.updateFoundWords(input)
            print(input + ' is one of the words!')
    elif len(input) < 4: #if the word is not in the list check the size
        print("Too short")
    else:
        #query the database to see if it is a word at all
        query1 = "select uniqueLetters from dictionary where fullWord = '" + input + "';"
        cursor.execute(query1)
        response = cursor.fetchone()
        if response == None:
            print("Not a word in word list")
        elif set(response[0]).issubset(set(puzzle.showUniqueLetters())): #check if the letters contain the center letter
            print("Missing center letter")
        else:
            #must be letters not in the puzzle in this case
            print("Bad letters")
            
    conn.commit()
    conn.close()
