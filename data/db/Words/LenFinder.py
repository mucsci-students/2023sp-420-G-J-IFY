'''
This is my incredibly dumb solution to this problem. While 
inefficient, it does work...
'''

import json
 
# Opening JSON file, manually change input depending on word length
with open('pangramFinalList.json') as f:
    data = json.load(f)

#open outfile
'''
Had a difficult time getting text to append, so I just copied
each output file before it got overwritten in the next run
'''
with open('pangrams.txt', 'w') as outFile:
    outFile.write('')

    i = 0 #loop counter
    pctr = 0 #sanity check counters, Pangram CTR
    nctr = 0 #Non-pangram CTR

    #iterate through entire list
    for a in data:
        #if pangram, write to file including all json syntax
        if 7 == len(set(data[i]['word'])):
            outFile.write('{"word":"' + data[i]['word'] + '"},')
            pctr += 1
        else:
            nctr += 1
        i += 1

outFile.close

#output sanity check
print('Pangrams: ' + str(pctr) + '\nNon-Pangrams: ' + str(nctr))