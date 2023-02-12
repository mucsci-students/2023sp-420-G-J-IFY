#The needed funciton call is getAllWordsFromBase. There are some other
#functions that are called, but shouldn't generally be needed 

#ALL YOU NEED TO DO IS getAllWordsForPuzzle(pLetters, kLetter)

#This function takes a string of unique letters pLetters and a key
#letter kLetter, generates the subset of those conditions, and creates
#a table in the db of only those words that fit the needs of the pangram
#@PARAM pLetters: A unique string of 7 chars
#@PARAM kLetter: a single character that is the key to the words
#@RETURN list of all possible words for given pLetters and kLetter
#Updated version of generateSubset. getAllWordsFrom Pangram
#takes in a puzzle object and pulls its needed info from there. 
#it also returns the word list to a field in that object

#Author Jacob Lovegren
#2/2/23
#revised 2/5/23
#rerevised 2/7/23

import sqlite3
import itertools


# gatAllWordsFromPangram - takes puzzle object, uses key
# letters and pangram letters, and returns a 
# set of all words that puzzle could contain
# @PARAM puzzle object
# Finishes by setting allWordList in puzzle object to result
def getAllWordsFromPangram(puzz): 
    #create powerset of letters from baseword
    pSet = list(powerset(puzz.showUniqueLetters()))
    cleanSet = []

    #remove sets from powerset to produce subset with keyletter
    ctr = 0
    while ctr < len(pSet):
        if puzz.showKeyLetter() in pSet[ctr]:
            cleanSet.append(sortStrToAlphabetical(''.join(pSet[ctr])))
        ctr += 1
    #Time to querey the DB   
    #first, generate initial querey for DB
    querey = "select fullWord from dictionary where uniqueLetters is '" + cleanSet[0] + "' "
    #next, append onto this a gross number of conditions which
    #are just the subset of the powerset of unique letters that 
    #include the subset
    ctr = 1
    while ctr < len(cleanSet):
        querey += " or uniqueLetters is '" + cleanSet[ctr] + "' "
        ctr += 1
    querey += ";"    

    #connect to DB, run querey
    conn = sqlite3.connect('wordDict.db')
    cursor = conn.cursor()
    cursor.execute(querey)
    
    #catch return form query
    tuples = (cursor.fetchall())
    #turn list of tuples into list of strings
    listList = list(itertools.chain(*tuples))
    #close DB
    conn.commit()
    conn.close()

    #return list of valid words
    return listList

# powerset takes an iterable object and creates a powerset of that object
# (being a set with every possible subset of that object)
# @PARAM itrable - an iterable object, in this use case its catching a string of unique letters
# @RETURN a powerset of the PARAM, in this case, a set of all subsets of those unique letters
from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


# sortStrToAlphabetical takes an unsorted string, sorts
# its characters alphabetically, and returns an alphabetical string
# @PARAM unsorted - an unsorted string 
# @RETURN a string of characters sorted alphabetically
def sortStrToAlphabetical(unsorted):
    uniqueLettersList = sorted(set(unsorted))
    #convert list to string
    return ''.join(uniqueLettersList)
