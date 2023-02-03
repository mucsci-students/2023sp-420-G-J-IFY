#The needed funciton call is getAllWordsFromBase. There are some other
#functions that are called, but shouldn't generally be needed 

#ALL YOU NEED TO DO IS getAllWordsForPuzzle(pLetters, kLetter)

#This function takes a string of unique letters pLetters and a key
#letter kLetter, generates the subset of those conditions, and creates
#a table in the db of only those words that fit the needs of the pangram
#@PARAM pLetters: A unique string of 7 chars
#@PARAM kLetter: a single character that is the key to the words
#@RETURN list of all possible words for given pLetters and kLetter

#Author Jacob Lovegren
#2/2/23

import sqlite3
import itertools


#reduce powerset to all combos that include key letter
def getAllWordsFromPangram(pLetters, kLetter):
    #create powerset of letters from baseword
    pSet = list(powerset(pLetters))
    cleanSet = []

    #remove sets from powerset to produce subset with keyletter
    ctr = 0
    while ctr < len(pSet):
        if kLetter in pSet[ctr]:
            cleanSet.append(sortStrToAlphabetical(''.join(pSet[ctr])))
        ctr += 1
    generateGameList(cleanSet)


#This function generates a powerset of a list
from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


#Generate 
def generateGameList(subStrSet):
    #first, generate initial querey for DB
    querey = "select fullWord from dictionary where uniqueLetters is '" + subStrSet[0] + "' "
    #next, append onto this a gross number of conditions which
    #are just the subset of the powerset of unique letters that 
    #include the subset
    ctr = 1
    while ctr < len(subStrSet):
        querey += " or uniqueLetters is '" + subStrSet[ctr] + "' "
        ctr += 1
    querey += ";"
    
    #connect to DB, run querey
    conn = sqlite3.connect('src/SpellingBee/wordDict.db')
    cursor = conn.cursor()
    cursor.execute(querey)
    
    #catch return form query
    tuples = (cursor.fetchall())

    #turn list of tuples into list of strings
    listList = list(itertools.chain(*tuples))

    #close DB
    conn.commit()
    conn.close()
    return listList

#extra catch, make sure unique letters are sorted
def sortStrToAlphabetical(unsorted):
    uniqueLettersList = sorted(set(unsorted))
    #convert list to string
    return ''.join(uniqueLettersList)


#getAllWordsFromPuzzle('abcdefg', 'a')