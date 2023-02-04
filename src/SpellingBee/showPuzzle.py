# Authors: Francesco Spagnolo 
# Course : CSCI 420
# Modified Date: 2/4/2023
# A module for displaying the puzzle

# Params: letters: takes a list of the letters for a given puzzle
# Prints out letters for a given puzzle
def showPuzzle(letters):
    string = ''
    
    for x in letters[1:4]:
        if x == letters[1]:
            string += x
        else: string += ' ' + x
        
    string += ' (' + letters[0] + ')'
    
    for x in letters[4:]:
        string += ' ' + x
    print(string)