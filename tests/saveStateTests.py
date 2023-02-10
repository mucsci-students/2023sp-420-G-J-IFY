# authors: Gaige Zakroski
import saveState 

# tests the constuctor
def testConstructor():
    try:
       
        assert(obj.keyLett == 'a' and obj.uniqueLett == 'warlock' and obj.shuffleLett == 'warlock')
        assert(obj.score == 0 and obj.maxScore == 0 and obj.foundWordList == [] and obj.allwordList == [] and obj.rank == ' ')
    except:
        print("testConstructor: FAILED")

def testShowKeyLetter(obj):
    try:
        assert(obj.showKeyLetter() == obj.keyLett)
    except:
        print("testShowKeyLetter: FAILED")

def testShowUniqueLetters(obj):
    try:
        assert(obj.showUniqueLetters() == obj.uniqueLett)
    except:
        print("testShowUniqueLetters: FAILED")

def testShowShuffleLetters(obj):
    try:
        assert(obj.showShuffleLett == obj.shuffleLett)
    except:
       print("testShowShuffleLetters: FAILED")

def testShowMaxScore(obj):
    try:
        assert(obj.showMaxScore() == obj.maxScore )
    except:
       print("testShowMaxScore: FAILED")

def testShowFoundWords(obj):
    try:
        assert(obj.showFoundWords() == obj.foundWordList)
    except:
        print("testShowFoundWords: FAILED")

def testshowAllWords(obj):
    try:
        assert(obj.showAllWords() == obj.allWordList)
    except:
        print("testshowAllWords: FAILED")

def testShowScore(obj):
    try:
        assert(obj.showScore() == obj.score())
    except:
        print("testShowScore: FAILED")

def testShowRank(obj):
    try:
        assert(obj.showRank() == obj.rank)
    except:
        print("testShowScore: FAILED")

def testUpdateFoundWords(obj):
    try:
        obj.updateFoundWords('warlock')
        obj.updateFoundWords('wrack')
        obj.updateFoundWords('wallaroo')
        assert(obj.foundWordList == ['warlock', 'wrack', 'wallaroo'])
    except:
        print("testUpdateFoundWords: FAILED")

def testUpdateScore(obj):
    try:
        obj.updateScore(10)
        assert(obj.score == 10)
        obj.updateScore(30)
        assert(obj.score == 40)
        
    except:
        print("testUpdateScore: FAILED")

def testSetKeyLetter(obj):
    try:
        obj.setKeyLetter('b')
        assert(obj.keyLett == 'b')
    except:
        print("testSetKeyLetter: FAILED")

def testSetUniqueLetters(obj):
    try:
        obj.setUniqueLetters('barnical')
        assert(obj.uniqueLett == 'barnical')
    except:
        print("testSetUniqueLetters: FAILED")

def testSetShuffleLetters(obj):
    try:
        obj.setShuffleLetters('barnical')
        assert(obj.shuffleLett == 'barnical')
    except:
        print("testSetShuffleLetters: FAILED")

def testSetScore(obj):
    try:
        obj.setScore(100)
        assert(obj.score == 100)
    except:
        print("testSetScore: FAILED")

def testSetMaxScore(obj):
    try:
        obj.setMaxScore(200)
        assert(obj.maxScore == 200)
    except:
        print("testSetMaxScore: FAILED")

def testSetFoundWords(obj):
    try:
        obj.setFoundWords = ["warlock", "wrack", "alcool", "arrack", "wallaroo"]
        assert(obj.foundWordList == ["warlock", "wrack", "alcool", "arrack", "wallaroo"])
    except:
        print("testSetFoundWords: FAILED")

def testSetAllWordList(obj):
    try:
        obj.setAllWordList(["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
        assert(obj.allWordList == ["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
    except:
        print("testSetAllWordList: FAILED")

def testSetRank(obj):
    try:
        obj.setRank('Queen Bee')
        assert(obj.rank == 'Queen Bee')
    except:
        print("testSetRank: FAILED")

def testUpdateRank(obj):
    try:
        obj.updateRank()
        assert(obj.rank == "Nice")
    except:
        print("testUpdateRank: FAILED")

def testShuffleChars(obj):
    try:
        obj.shuffleChars()
        assert( not obj.shuffleLett == obj.uniqueLett)
    except:
        print("testShuffleChars: FAILED")

obj = saveState.Puzzle('a', 'warlock')
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


