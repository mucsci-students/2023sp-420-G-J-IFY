###############################################################################
# test_encryption.py
# Author: Yah'hymbey Baruti Ali-Bey
# Date of Creation: 4-8-2023
#
# This module is the test code for encryption and decryption object to ensure
# functionality across all files and objects.
#
###############################################################################

import hint
import pytest
import model.output
import MakePuzzle

# Test Code
def compareList(l1, l2):
    if (len(l1) != len(l2)):
        print("Lengths do not match")
        return
    
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            print("Word at index " + i + "does not equal")
            return
            
    print("It works!!")
    
def checkEncryption():
    pass

def checkDecrytion():
    pass

@pytest.fixture
def puzzleFixture():
    return MakePuzzle.newPuzzle('stainer', 'e', outty, False)