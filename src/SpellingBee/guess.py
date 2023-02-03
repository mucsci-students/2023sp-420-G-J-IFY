# Authors: Francesco Spagnolo
# Course : CSCI 420
# Modified Date: 2/1/2023
# A module for the main guess making

import sqlite3
# Params: wordList: takes the complete word list as 
# Finds legitimate base word and creates a puzzle based on that
def guess(wordList):
    
    conn = sqlite3.connect('src/SpellingBee/wordDict.db')
    cursor = conn.cursor()
    
    input = input()
    points
        
    #check for every case in the user's guess to give points or have them input again
    for word in wordList:
        if input.length() < 4:
            print("Too Short")
        elif input != word:
            print("Not a word in word List")
        #elif input == foundWords:
            #print("Already Found")
        query = "select wordScore from dictionary where fullWord = '" + [input] + "';"
        cursor.execute(query)
        points = cursor.fetchone()[0]
        
    conn.commit()
    conn.close()
          
    return points