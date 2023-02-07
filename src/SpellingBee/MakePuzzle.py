# Authors: Yah'hymbey Baruti-Bey, Francesco Spagnolo 
# Course : CSCI 420
# Modified Date: 2/2/2023
# A module for making a new puzzle 


#Imports
import sqlite3
import random
import saveState


# Params: baseWord: takes a baseword that is either an empty string or a pangram and makes a puzzle from it
# Finds legitimate base word and creates a puzzle based on that
def newPuzzle(baseWord):    
    uniqueLetters = {}
    if baseWord == '':
        # Finds baseword and its unique letters and puts them in a tuple
        baseTuple = findBaseWord()
        baseWord = baseTuple[0]
        uniqueLetters = set(baseTuple[1])
    
    # Checks if word from user is in database
    # and getts the unique letters if so
    elif checkDataBase(baseWord):
        uniqueLetters = set(baseWord)
    
    # If not an empty string
    # and not in databasee raise and exception
    else:
        raise Exception("Word not in database.")
    
    keyLetter = choseKeyLetter(uniqueLetters)
    
    # Below Code Subject to Change
    NewPuzzle = saveState.Puzzle(keyLetter, uniqueLetters)
    # Call Word List Generator
    NewPuzzle.wordListStorage()
    # Gets Proper max score
    NewPuzzle.updateMaxScore(NewPuzzle.wordListStorage())
    # Call Show Puzzle
    NewPuzzle.showUniqueLetters()
    # Show Status
    NewPuzzle.showRank()
    
    
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
                        Limit 1
                        """)
    wordDictC.commit()
    wordDictC.close()

    return wordDictC.fetchone()

# Checks if the given baseword is in the database
# Returns a boolean true if the word is found in the database
# False otherwise
def checkDataBase(baseWord):
    # SQLite Connections
    wordDict = sqlite3.connect('wordDict.db')
    
    # Used to execute SQL commands
    wordDictC = wordDict.cursor()
    
    wordDictC.execute(""" SELECT fullWord
                        FROM pangrams 
                        WHERE fullWord = 
                        """ + baseWord)
    wordDictC.commit()
    wordDictC.close()
    
    return wordDictC.fetchone() > 0

# Params: uniqueLetters: set of uniqueLetters from a baseword
# Takes a SET of letters and picks a letter from to make key letter
def choseKeyLetter(uniqueLetters):
    return random.choice(uniqueLetters)

def shuffle(letters):
        
    mainLetter = letters[0] #saving the main letter for before the shuffle
    random.shuffle(letters) 
        
    for main in letters: #looping through to find the main letter in shuffled list
        if mainLetter == letters[main]:
            #removing main letter and swapping positions of letters to put main letter in the front
            letters.remove(letters[main])
            letters[main] = letters[0]
            letters[0] = mainLetter 
                
    return letters

def guess(wordList):
    
    conn = sqlite3.connect('src/SpellingBee/wordDict.db')
    cursor = conn.cursor()
    
    input = input()
    points
        
    #check for every case in the user's guess to give points or have them input again
    if input.length() < 4:
        raise Exception("Too Short")
    elif input not in wordList:
        raise Exception("Not a word in word List")
    #elif input == foundWords:
        #raise Exeption("Already Found")

    query = "select wordScore from dictionary where fullWord = '" + [input] + "';"
    cursor.execute(query)
    points = cursor.fetchone()[0]
        
    conn.commit()
    conn.close()
          
    return points