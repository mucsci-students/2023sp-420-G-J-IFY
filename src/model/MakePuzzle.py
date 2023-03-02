################################################################################
# MakePuzzle.py
# Author: Jacob Lovegren, Yah'hymbey Baruti-Bey, Francesco Spagnolo
# Date of Creation: 2-2-2023
#
# Makes a basic puzzle game object after being given a baseword
#
# (Global, public) functions:
#   newPuzzle(baseWord : str) -> Puzzle Obj
#       - Makes a basic puzzle
################################################################################


import sqlite3
from random import randrange
import model.puzzle as saveState
from model import dbFixer
from controller.cController import CommandHandler
import itertools
import model.output as output

class LetterMismatchException(Exception):
    pass

class EmptyKeyLetterException(Exception):
    pass


################################################################################
# newPuzzle(baseWord: str) -> Puzzle Obj
#
# DESCRIPTION:
#   Finds legitimate base word and creates a puzzle based on that 
#
# PARAMETERS:
#  baseWord : str
#   takes a baseword that is either an empty string or a pangram and makes a 
#   puzzle from it
#  outty : object
#     - output object storing output strings
#  flag : bool
#    flag to check if we are using cli or gui (True for Gui False for Cli)
#
#
# RETURNS:
#  puzzle
#   empty game object
# 
# RAISES:
#  BadQueryException
#   if check is baseword contains nonalphas
#   if word is in the database
################################################################################
def newPuzzle(baseWord: str, keyLetter:str, outty: output, flag: bool) -> object:    
    try:
        uniqueLetters = {}
        if baseWord == '':
            # Finds baseword and its unique letters and puts them in a tuple
            baseTuple = findBaseWord()
            #baseWord = baseTuple[0]
            uniqueLetters = baseTuple[0]
            keyLetter = baseTuple[1]
            maxScore = baseTuple[2]
        
        # Checks if word from user is in database
        # and gets the unique letters if so
        else:
            #catch if nonalphas before query is made to prevent SQL injection
            if not baseWord.isalpha():
                raise BadQueryException
            #validate the key letter
            if keyLetter == '':
                raise EmptyKeyLetterException 
            if keyLetter not in baseWord:
                raise LetterMismatchException

            #query DB for word
            returnTuple = checkDataBase(baseWord.lower())
            #returnTuple will be None if query returns emptyy
            if returnTuple == None:
                raise BadQueryException
            uniqueLetters = returnTuple[1]

            #now that the input has been validated, go find the max score for this game
            dbFixer.goToDB()
            conn = sqlite3.connect('wordDict.db')
            cursor = conn.cursor()
            cursor.execute("select score from allGames where uniqueLetters = '" +
                           uniqueLetters + "' and keyLetter = '" + keyLetter + "';")
            maxScore = cursor.fetchone()[0]
            #close DB
            conn.commit()
            conn.close()
            dbFixer.leaveDB()
                    
        # Creates the puzzle for users to solve
        puzzle = saveState.Puzzle(keyLetter, uniqueLetters)
        # Populates the puzzles wordlist
        puzzle.findAllWords()
        # Generates a max score
        puzzle.setMaxScore(maxScore)
        # Generates rank
        puzzle.updateRank()
        
        return puzzle
    #Raise exception for bad puzzle seed
    except BadQueryException:
        if flag == False:
            outty.setField(baseWord.upper() + " is not a valid word")
        else:
            # TODO
            pass
        return CommandHandler.newPuzzle(outty)
    except LetterMismatchException:
        outty.setField(keyLetter.upper() + " is not a valid key letter")
        return CommandHandler.newPuzzle(outty)
    except EmptyKeyLetterException:
        outty.setField("Key letter cannot be empty")
        return CommandHandler.newPuzzle(outty)
    

#Exception used for newPuzzle to catch bad starting words
class BadQueryException(Exception):
    #raised when user has a bad starting word
    pass
    

################################################################################
# findBaseWord() -> tuple
#
# DESCRIPTION:
#   Finds a legitimate baseword to start puzzle with from the database
#
# PARAMETERS:
#  none
#
# RETURNS:
#  resultResult
#   tuple of (uniqueLetters, keyLetter, score)
################################################################################
def findBaseWord():
    # SQLite Connections
    dbFixer.goToDB()
    wordDict = sqlite3.connect('wordDict.db')

    # Used to execute SQL commands
    wordDictC = wordDict.cursor()
    # Grabs a random baseword from the list
    wordDictC.execute(""" SELECT *
                        FROM allGames 
                        ORDER BY RANDOM() 
                        Limit 1;
                        """)
    #catch return from querey
    resultResult = (wordDictC.fetchone())

    #close DB
    wordDict.commit()
    wordDict.close()
    dbFixer.leaveDB()

    #return tuple of result
    return resultResult


################################################################################
# checkDataBase(baseWord: str) -> tuple
#
# DESCRIPTION:
#  Checks if the given baseword is in the database
#
# PARAMETERS:
#  baseWord : str
#   an example integer parameter
#
# RETURNS:
#  returnResult
#   tuple with query results or false if word not in DB
################################################################################
def checkDataBase(baseWord: str):
    # SQLite Connections
    dbFixer.goToDB()
    wordDict = sqlite3.connect('wordDict.db')
    
    # Used to execute SQL commands
    cursor = wordDict.cursor()
    
    cursor.execute("SELECT *FROM pangrams WHERE fullWord = '" + baseWord + "';")
    #grab tuple returned from querey
    returnResult = cursor.fetchone()

    #after result is caught, disconenct from DB
    wordDict.commit()
    wordDict.close()
    dbFixer.leaveDB()

    return returnResult




################################################################################
# guess(puzzle, input: str, flag : bool, outty : object)
#
# DESCRIPTION:
#   checks the database for valid words, already found words and 
#   words that do not exist
#
# PARAMETERS:
#  puzzle : Obj
#   puzzle object of current played game space
#  input : str
#   user input 
#  flag : bool
#  outty : object
#    - output object storing output strings
#
################################################################################
def guess(puzzle, input: str, flag : bool, outty : object):
    
    if not flag:
        input = input.lower()
    else:
        #TODO
        #input = pull from gui
        pass
    dbFixer.goToDB()
    conn = sqlite3.connect('wordDict.db')
    cursor = conn.cursor()
        
    #check for every case in the user's guess to give points or output error
    #check for only containing alphabetical characters
    if not input.isalpha():
        if not flag:
            outty.setField(input + " contains non alphabet characters")
        else:
            # TODO
            # pop up window
            pass
        
    # checks words in the word list to see if it is valid for the puzzle
    elif input in puzzle.getAllWords(): 
        #check if it is already found
        if input in puzzle.getFoundWords():
            if not flag:
                outty.setField(input.upper() + " was already found!")
            else:
                #TODO
                #Pop up window
                pass
        else:
            #query the database to see how many points to give
            query = "select wordScore from dictionary where fullWord = '" + input + "';"
            cursor.execute(query)
            puzzle.updateScore(cursor.fetchone()[0])
            puzzle.updateRank()
            puzzle.updateFoundWords(input)
            outty.setField(input.upper() + ' is one of the words!')
    elif len(input) < 4: #if the word is not in the list check the size
        if not flag:
            outty.setField(input.upper() + " is too short!\nGuess need to be at least 4 letters long")
        else:
            #TODO
            #POPUP WINDOW
            pass
    else:
        #query the database to see if it is a word at all
        query1 = "select uniqueLetters from dictionary where fullWord = '" + input + "';"
        cursor.execute(query1)
        response = cursor.fetchone()
        if response == None:
            if not flag:
                outty.setField(input.upper() + " isn't a word in the dictionary")
            else:
                #TODO
                #Popup window
                pass
        #check if the letters contain the center letter
        elif set(response[0]).issubset(set(puzzle.getUniqueLetters())): 
            if not flag:
                outty.setField(input.upper() + " is missing center letter, " + puzzle.getKeyLetter().upper())
            else:
                #TODO
                #popup Window
                pass
        else:
            #must be letters not in the puzzle in this case
            if not flag:
                outty.setField(input.upper() + " contains letters not in " + puzzle.getShuffleLetters().upper())
            else:
                #TODO
                #popup window
                pass
            
    conn.commit()
    conn.close()
    dbFixer.leaveDB()

################################################################################
# getAllWordsFromPangram(puzz : Puzzle Object) -> list
# DESCRIPTION:
#   This function generates all the words for a given puzzle.
#
# PARAMETERS:
#   puzz : Puzzle
#       - the Puzzle object where the needed letters are pulled from
#
# RETURNS:
#   list
#       - a list of all the possible words for the given puzzle
################################################################################
def getAllWordsFromPangram(unique, key) -> list: #unclear how to add the puzzle type to this line
    #create powerset of letters from baseword
    pSet = list(powerset(unique))
    cleanSet = []

    #remove sets from powerset to produce subset with keyletter
    for a in pSet:
        if key in a:
            cleanSet.append(sortStrToAlphabetical(''.join(a)))
      
    #Time to querey the DB   
    dbFixer.goToDB()
    conn = sqlite3.connect('wordDict.db')
    cursor = conn.cursor()

    #create temp table to use for natural joins soon
    tempTable = "create temporary table validLetters (uniLetts);"
    cursor.execute(tempTable)
   
    #Build out tempTable for join later
    querey = "insert into validLetters (uniLetts) values ('"
    for a in cleanSet:
        querey += a + "'), ('"
    querey += "');"
    cursor.execute(querey)
    
    #build out query using joins
    join = """
            select fullWord from dictionary join validLetters 
            on dictionary.uniqueLetters is validLetters.uniLetts;
            """
    cursor.execute(join)
    
    #catch return form query
    tuples = (cursor.fetchall())
    #turn list of tuples into list of strings
    listList = list(itertools.chain(*tuples))
    #close DB
    conn.commit()
    conn.close()
    dbFixer.leaveDB()

    #return list of valid words
    return listList


################################################################################
# powerset(iterable) -> set
#
# DESCRIPTION:
#   This is a helper funciton for generateAllWordsFromPangram()
#
#   This function takes an iterable object and returns a powerset of that
#   iterable object. 
#   
#   A power set is all the possible subset combinations of the set.
#       i.e. powerst (abc) -> a, b, c, ab, ac, bc, abc
#
# PARAMETERS: 
#   iterable : ITERABLE OBJECT
#       - any iterable object, in this case, a string of unique letters
#       - 'abcdefg'
#
# RETURNS:
#   Set
#       - a powerset of the iterable object
################################################################################
from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


################################################################################
# sortStrToAlphabetical(unsorted : str) -> str
#
# DESCRIPTION:
#   This function takes a string and alphabetizes the letters within
#
# PARAMETERS:
#   unsorted : str
#       - "warlock"
#
# RETURNS:
#   str
#       -"acklorw"
################################################################################
def sortStrToAlphabetical(unsorted : str) -> str:
    uniqueLettersList = sorted(set(unsorted))
    #convert list to string
    return ''.join(uniqueLettersList)



################################################################################
# newPuzzCli(baseWord: str, uniqueLetters: dict) -> str
#
# DESCRIPTION:
#   This function takes a string and a dictionary and handles input to determine
#   the key Letter for CLI
#
# PARAMETERS:
#   baseWord: str
#       base word of a puzzle 
#
#   uniqueLetters: dict
#       dict of unique letters    
# 
# RETURNS:
#   keyLetter: str
#       key letter for the game  
#
################################################################################
def newPuzzCli(baseWord: str, uniqueLetters: dict) -> str:
    keyLetter = input("Enter a letter from your word to use as the key letter\n> ")     #####i believe these are fully depricated now Jacob Lovegren 3/1/23
    keyLetter = keyLetter.lower()
    #test to see if keyletter is valid
    while keyLetter not in uniqueLetters or keyLetter == "":
    #catch if they enter nothing
        if keyLetter == "":
            keyLetter = input("Must enter character from " 
                                        + baseWord + ": ")
        else:
            keyLetter = input(keyLetter + " is not part of " 
                                    + baseWord + 
                                    " - Please enter a letter from your word: ")
    return keyLetter
            
def newPuzzGui(baseWord: str):
    # TODO
    pass