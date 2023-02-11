# authors: Gaige Zakroski
import saveState 
import unittest

# tests the constuctor
def testConstructor():
    try:
        obj = saveState.Puzzle('a', 'warlock')
        assert(obj.keyLett == 'a')
        assert(obj.uniqueLett == 'warlock')
        assert(obj.shuffleLett == 'warlock')
        assert(obj.score == 0)
        assert(obj.maxScore == 0)
        assert(obj.foundWordList == [])
        assert(obj.allWordList == [])
        assert(obj.rank == ' ')
        print("testConstructor: PASSED")
        return obj
    except:
        print("testConstructor: FAILED")

def testShowKeyLetter(obj):
    try:
        assert(obj.showKeyLetter() == obj.keyLett)
        print("testShowKeyLetter: PASSED")
    except:
        print("testShowKeyLetter: FAILED")

def testShowUniqueLetters(obj):
    try:
        assert(obj.showUniqueLetters() == obj.uniqueLett)
        print("testShowUniqueLetters: PASSED")
    except:
        print("testShowUniqueLetters: FAILED")

def testShowShuffleLetters(obj):
    try:
        assert(obj.showShuffleLetters() == obj.shuffleLett)
        print("testShowShuffleLetters: PASSED")
    except:
       print("testShowShuffleLetters: FAILED")

def testShowMaxScore(obj):
    try:
        assert(obj.showMaxScore() == obj.maxScore )
        print("testShowMaxScore: PASSED")
    except:
       print("testShowMaxScore: FAILED")

def testShowFoundWords(obj):
    try:
        assert(obj.showFoundWords() == obj.foundWordList)
        print("testShowFoundWords: PASSED")
    except:
        print("testShowFoundWords: FAILED")

def testshowAllWords(obj):
    try:
        assert(obj.showAllWords() == obj.allWordList)
        print("testshowAllWords: PASSED")
    except:
        print("testshowAllWords: FAILED")

def testShowScore(obj):
    try:
        assert(obj.showScore() == obj.score)
        print("testShowScore: PASSED")
    except:
        print("testShowScore: FAILED")

def testShowRank(obj):
    try:
        assert(obj.showRank() == obj.rank)
        print("testShowScore: PASSED")
    except:
        print("testShowScore: FAILED")

def testUpdateFoundWords(obj):
    try:
        obj.updateFoundWords('warlock')
        obj.updateFoundWords('wrack')
        obj.updateFoundWords('wallaroo')
        assert(obj.foundWordList == ['warlock', 'wrack', 'wallaroo'])
        print("testUpdateFoundWords: PASSED")
    except:
        print("testUpdateFoundWords: FAILED")

def testUpdateScore(obj):
    try:
        obj.updateScore(10)
        assert(obj.score == 10)
        obj.updateScore(30)
        assert(obj.score == 40)
        print("testUpdateScore: PASSED")
    except:
        print("testUpdateScore: FAILED")

def testSetKeyLetter(obj):
    try:
        obj.setKeyLetter('b')
        assert(obj.keyLett == 'b')
        print("testSetKeyLetter: PASSED")
    except:
        print("testSetKeyLetter: FAILED")

def testSetUniqueLetters(obj):
    try:
        obj.setUniqueLetters('barnical')
        assert(obj.uniqueLett == 'barnical')
        print("testSetUniqueLetters: PASSED")
    except:
        print("testSetUniqueLetters: FAILED")

def testSetShuffleLetters(obj):
    try:
        obj.setShuffleLetters('barnical')
        assert(obj.shuffleLett == 'barnical')
        print("testSetShuffleLetters: PASSED")
    except:
        print("testSetShuffleLetters: FAILED")

def testSetScore(obj):
    try:
        obj.setScore(100)
        assert(obj.score == 100)
        print("testSetScore: PASSED")
    except:
        print("testSetScore: FAILED")

def testSetMaxScore(obj):
    try:
        obj.setMaxScore(200)
        assert(obj.maxScore == 200)
        print("testSetMaxScore: PASSED")
    except:
        print("testSetMaxScore: FAILED")

def testSetFoundWords(obj):
    try:
        list = ["warlock", "wrack", "alcool", "arrack", "wallaroo"]
        obj.setFoundWords(list)
        assert(obj.showFoundWords() == ["warlock", "wrack", "alcool", "arrack", "wallaroo"])
        print("testSetFoundWords: PASSED")
    except:
        print("testSetFoundWords: FAILED")

def testSetAllWordList(obj):
    try:
        obj.setAllWordList(["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
        assert(obj.allWordList == ["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
        print("testSetAllWordList: PASSED")
    except:
        print("testSetAllWordList: FAILED")

def testSetRank(obj):
    try:
        obj.setRank('Queen Bee')
        assert(obj.rank == 'Queen Bee')
        print("testSetRank: PASSED")
    except:
        print("testSetRank: FAILED")

def testUpdateRank(obj):
    try:
        obj.updateRank()
        assert(obj.rank == "Great")
        print("testUpdateRank: PASSED")
    except:
        print("testUpdateRank: FAILED")

def testShuffleChars(obj):
    try:
        obj.shuffleChars()
        assert( not obj.shuffleLett == obj.uniqueLett)
        print("testShuffleChars: PASSED")
    except:
        print("testShuffleChars: FAILED")


obj = testConstructor()
testShowKeyLetter(obj)
testShowUniqueLetters(obj)
testShowShuffleLetters(obj)
testShowMaxScore(obj)
testShowFoundWords(obj)
testshowAllWords(obj)
testShowScore(obj)
testShowRank(obj)
testUpdateFoundWords(obj)
testUpdateScore(obj)
testSetKeyLetter(obj)
testSetUniqueLetters(obj)
testSetShuffleLetters(obj)
testSetScore(obj)
testSetMaxScore(obj)
testSetFoundWords(obj)
testSetAllWordList(obj)
testSetRank(obj)
testUpdateRank(obj)
testShuffleChars(obj)


