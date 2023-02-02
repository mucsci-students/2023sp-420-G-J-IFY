# Authors: Francesco Spagnolo 
# Course : CSCI 420
# Modified Date: 2/1/2023
# A module for shuffling the letters in the puzzle

import random

def shuffle(letters):
        
    mainLetter = letters.first() #saving the main letter for before the shuffle
    random.shuffle(letters) 
        
    for main in letters: #looping through to find the main letter in shuffled list
        if mainLetter == letters[main]:
            #removing main letter and swapping positions of letters to put main letter in the front
            letters.remove(letters[main])
            letters[main] = letters[0]
            letters[0] = mainLetter 
                
    return letters