#Jacob Lovegren 2/2/23
#Generate max score from wordlist

import sqlite3


#findMaxScore - this functions takes a list of words 
#for a game, quereies the DB for all words in the game,
#and adds together the total possible points for the given pangram
#@PARAM listList, a list of strings containing all words in DB
#   for given pangram 
#@RETURN maxScore, the total possible score for a starting word
def findMaxScore(listList):
    #connect to DB
    conn = sqlite3.connect('wordDict.db')
    cursor = conn.cursor()
    
    ctr = 0
    maxScore = 0
    #loop through list, querey DB for each word, aggregate values
    for a in listList:
        query = """select wordScore
        from dictionary
        where fullWord = '""" + listList[ctr] + "';"
        cursor.execute(query)
        maxScore += cursor.fetchone()[0]
        ctr += 1

    #close DB
    conn.commit()
    conn.close()

    return maxScore

#findMaxScore(["apple", "banana", "warlock"])