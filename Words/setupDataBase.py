"""
This is the program I used to yeet words into database. This will not need to be run
again, but it feels wrong to not share how this got setup. 

This should move elsewhere in the project, I should check with Isaak about
where, but for now, we're in src

This is a solid reference for how to interact with sqlite3 with python
and my janky ass json hack though
"""



import sqlite3
conn = sqlite3.connect('src/SpellingBee/wordDict.db')
cursor = conn.cursor()


import json 

# Opening JSON file, manually change input depending on word length
#with open('Words/pangramFinalList.json') as f:
#    data = json.load(f)



#//DB already created in folder, here's the create table command for clarity
#cursor.execute("""Create table pangrams(
#                fullWord text,
#                uniqueLetters text
#               )""")

"""
i = 0 #loop counter
pctr = 0 #sanity check counters, Pangram CTR
nctr = 0 #Non-pangram CTR

#//This has also been done, DB of pangram's added, DO NOT RUN AGAIN!!!!
#iterate through entire list
for a in data:
    pangram = data[i]['word']
    #store unique letters sorted alphabetically as list
    uniqueLettersList = sorted(set(pangram))
    #convert list to string
    strSet = ''.join(uniqueLettersList)
    print(pangram + " " + strSet)
    cursor.execute("insert into pangrams values (?, ?)", (pangram, strSet))
    i += 1
"""


#import json 
# Opening JSON file, manually change input depending on word length
#with open('Words/validWordsDictionary.json') as f:
#    data = json.load(f)

#//DB already created in folder, here's the create table command for clarity
#cursor.execute("""Create table dictionary(
#                fullWord text,
#                uniqueLetters text, 
#                wordScore int
#               )""")

"""
i = 0 #loop counter
pctr = 0 #sanity check counters, Pangram CTR
nctr = 0 #Non-pangram CTR

#//This has also been done, DB of pangram's added, DO NOT RUN AGAIN!!!!
#iterate through entire list
for a in data:
    word = data[i]['word']
    #store unique letters sorted alphabetically as list
    uniqueLettersList = sorted(set(word))
    #convert list to string
    strSet = ''.join(uniqueLettersList)
    print(word + " " + strSet)
    if len(word) = 4:
        score = 1
    else:
        score = len(word)
    cursor.execute("insert into dictionary values (?, ?, ?)", (word, strSet, score))
    i += 1
"""

sqlCommand = "select * from dictionary"

cursor.execute(sqlCommand)

print(cursor.fetchall())

conn.commit()

conn.close()