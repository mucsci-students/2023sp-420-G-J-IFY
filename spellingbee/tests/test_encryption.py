###############################################################################
# test_encryption.py
# Author: Yah'hymbey Baruti Ali-Bey
# Date of Creation: 4-8-2023
#
# This module is the test code for encryption and decryption object to ensure
# functionality across all files and objects.
#
###############################################################################

import encrypter
import pytest

@pytest.fixture
def puzzleFixture():
    dict = {"Author": "GJIFY","RequiredLetter": "a", "PuzzleLetters": "acklorw",
            "CurrentPoints": 0, "MaxPoints": 323, "GuessedWords": [],
            "WordList": ["acro", "alar", "alow", "arak", "arco", "awol",
                         "caca", "calk", "call", "calo", "cark", "carl",
                         "carr", "claw", "coal", "coca", "cola", "craw",
                         "kaka", "kola", "kora", "lack", "lall", "lark",
                         "loca", "okra", "olla", "oral", "orca", "orra",
                         "rack", "roar", "wack", "walk", "wall", "wark",
                         "wawl", "acock", "alack", "allow", "arrow", "cacao",
                         "calla", "carol", "clack", "claro", "cloak", "coala",
                         "cocoa", "coral", "craal", "crack", "crawl", "croak",
                         "karoo", "koala", "kraal", "local", "loral", "wacko",
                         "walla", "wrack", "alcool", "arrack", "calcar",
                         "callow", "carack", "cloaca", "coccal", "collar",
                         "corral", "karroo", "wallow", "caracal", "caracol",
                         "carrack", "cloacal", "corolla", "oarlock", "warlock",
                         "warwork", "callaloo", "caracara", "rackwork",
                         "wallaroo"]
            }

    return dict

@pytest.fixture
def encryptPuzzle(puzzleFixture):
    return encrypter.encryptionHandler(puzzleFixture, 1)

@pytest.fixture
def decryptPuzzle(encryptPuzzle):
    return encrypter.encryptionHandler(encryptPuzzle, 0)

# Test Code
def testEqualSizeListDe(puzzleFixture, decryptPuzzle):
    assert(len(puzzleFixture["WordList"]) == len(decryptPuzzle["WordList"]))

def testEqualListDe(puzzleFixture, decryptPuzzle):  
    assert(str(puzzleFixture["WordList"]) == str(decryptPuzzle["WordList"]))
                    
def testEncryption(puzzleFixture, encryptPuzzle):
    assert(str(puzzleFixture["WordList"]) == str(encryptPuzzle["WordList"]))