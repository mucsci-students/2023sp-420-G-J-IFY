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

#params: letters is a list of the letters
#shuffles letters but keeps the center letter at the front of the list
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

#params: puzzle object, input that the user gave
#checks the database for valid words, already found words and words that do not exist
def guess(puzzle, input):
    
    conn = sqlite3.connect('src/SpellingBee/wordDict.db')
    cursor = conn.cursor()
        
    #check for every case in the user's guess to give points or output error
    if input in puzzle.showAllWordList(): #checks words in the word list to see if it is valid for the puzzle
        if input in puzzle.showFoundWords(): #check if it is already found
            print("Already Found")
        else:
            #query the database to see how many points to give
            query = "select wordScore from dictionary where fullWord = '" + [input] + "';"
            cursor.execute(query)
            puzzle.updatePoints(cursor.fetchone()[0])
    elif len(input) < 4: #if the word is not in the list check the size
        print("Too short")
    else:
        #query the database to see if it is a word at all
        query1 = "select uniqueLetters from dictionary where fullWord = '" + [input] + "';"
        response = cursor.execute(query1)
        if response == None:
            print("Not a word in word list")
        elif set(response[0]).issubset(set(puzzle.showUniqueLetters())): #check if the letters contain the center letter
            print("Missing center letter")
        else:
            #must be letters not in the puzzle in this case
            print("Bad letters")
            
    conn.commit()
    conn.close()

test = saveState.Puzzle('a', 'warlock')

guess(test, 'warlock')