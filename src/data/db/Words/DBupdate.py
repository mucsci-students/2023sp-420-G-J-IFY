#This program specifically updates how the DB is queried and updates the DB to include all word list
#Jacob Lovegren 2/13/23

import sqlite3
import itertools


# gatAllWordsFromPangram - takes puzzle object, uses key
# letters and pangram letters, and returns a 
# set of all words that puzzle could contain
# @PARAM puzzle object
# Finishes by setting allWordList in puzzle object to result
def getAllWordsFromPangram(uniLet, keyLet): 
    #create powerset of letters from baseword
    pSet = list(powerset(uniLet))
    cleanSet = []

    #remove sets from powerset to produce subset with keyletter
    for a in pSet:
        if keyLet in a:
            cleanSet.append(sortStrToAlphabetical(''.join(a)))


    #connect to DB, run querey
    conn = sqlite3.connect('wordDict.db')
    cursor = conn.cursor()


    tempTable = "create temporary table validLetters (uniLetts);"
    cursor.execute(tempTable)

    querey = "insert into validLetters (uniLetts) values ('"

    for a in cleanSet:
        querey += a + "'), ('"
    querey += "');"
    cursor.execute(querey)
    
    naturalJoin = "select sum(wordScore) from dictionary join validLetters on dictionary.uniqueLetters is validLetters.uniLetts;"
    cursor.execute(naturalJoin)

    #catch return form query
    tuples = (cursor.fetchall())[0]
    #turn list of tuples into list of strings
    gameScore = tuples[0]
    #close DB
    conn.commit()
    conn.close()

    #return list of valid words
    return gameScore

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

def findShortest():


    ctr = 0

    #run for everything that doesn't start with a
    alphabet= ['ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap'] #need to add a to these in query
    #alphabet = ['n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b'] #ran 'o' ahead of time, add back in later

    for alpha in alphabet:
        #connect to DB, run querey
        conn = sqlite3.connect('wordDict.db')
        cursor = conn.cursor()
        cursor.execute("select distinct uniqueLetters from pangrams where uniqueLetters like '" + alpha + "%';")
        allUniqLetters = cursor.fetchall()
        for eachTup in allUniqLetters:
            uniStr = eachTup[0]
            for eachChar in uniStr:
                gameScore = getAllWordsFromPangram(uniStr, eachChar)
                query = "insert into allGames (uniqueLetters, keyLetter, score) values ('" + uniStr + "', '" + eachChar + "', " + str(gameScore) + ");"
                cursor.execute(query)
                ctr += 1
        conn.commit()
        conn.close()
    print("This has updated entries for all " + str(ctr) + " entries")

#only run this if you need to update the DB!!!!!!!!

##AGAIN!!!! DO NOT RUN THIS CODE!!!
#findShortest()
