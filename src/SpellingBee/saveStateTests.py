# authors: Gaige Zakroski
import saveState 
import unittest

# tests the constuctor
class testSaveState(unittest.TestCase):
    #test constuctor
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
            
        
    #test show keyLetter
    assert(obj.showKeyLetter() == obj.keyLett)
    print("testShowKeyLetter: PASSED")
        
    # test ShowUniqueLetters
    assert(obj.showUniqueLetters() == obj.uniqueLett)
    print("testShowUniqueLetters: PASSED")
        
    # test ShowShuffleLetters
    assert(obj.showShuffleLetters() == obj.shuffleLett)
    print("testShowShuffleLetters: PASSED")

    # test ShowMaxScore
    assert(obj.showMaxScore() == obj.maxScore )
    print("testShowMaxScore: PASSED")
        
    # testShowFoundWords
    assert(obj.showFoundWords() == obj.foundWordList)
    print("testShowFoundWords: PASSED")
    # test showAllWords
    assert(obj.showAllWords() == obj.allWordList)
    print("testshowAllWords: PASSED")
    
    # testShowScore
    assert(obj.showScore() == obj.score)
    print("testShowScore: PASSED")
    
    # test ShowRank
    assert(obj.showRank() == obj.rank)
    print("testShowScore: PASSED")

    # testUpdateFoundWords
    obj.updateFoundWords('warlock')
    obj.updateFoundWords('wrack')
    obj.updateFoundWords('wallaroo')
    assert(obj.foundWordList == ['warlock', 'wrack', 'wallaroo'])
    print("testUpdateFoundWords: PASSED")
       

    #test UpdateScore
    obj.updateScore(10)
    assert(obj.score == 10)
    obj.updateScore(30)
    assert(obj.score == 40)
    print("testUpdateScore: PASSED")

    # test SetKeyLetter
    obj.setKeyLetter('b')
    assert(obj.keyLett == 'b')
    print("testSetKeyLetter: PASSED")

    # test SetUniqueLetters
    obj.setUniqueLetters('barnical')
    assert(obj.uniqueLett == 'barnical')
    print("testSetUniqueLetters: PASSED")
        
    # test SetShuffleLetters
    obj.setShuffleLetters('barnical')
    assert(obj.shuffleLett == 'barnical')
    print("testSetShuffleLetters: PASSED")
        
    # test SetScore
    obj.setScore(100)
    assert(obj.score == 100)
    print("testSetScore: PASSED")

    # test SetMaxScore
    obj.setMaxScore(200)
    assert(obj.maxScore == 200)
    print("testSetMaxScore: PASSED")

    # test SetFoundWords
    list = ["warlock", "wrack", "alcool", "arrack", "wallaroo"]
    obj.setFoundWords(list)
    assert(obj.showFoundWords() == ["warlock", "wrack", "alcool", "arrack", "wallaroo"])
    print("testSetFoundWords: PASSED")
       
    # test SetAllWordList
    obj.setAllWordList(["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
    assert(obj.allWordList == ["warlock", "wrack", "alcool", "arrack", "wallaroo", "cloacal", "corolla", "wallow", "corral"])
    print("testSetAllWordList: PASSED")
       
    # test  SetRank
    obj.setRank('Queen Bee')
    assert(obj.rank == 'Queen Bee')
    print("testSetRank: PASSED")
      
    # test UpdateRank
    obj.updateRank()
    assert(obj.rank == "Great")
    print("testUpdateRank: PASSED")
       
    # test ShuffleChars 
    obj.shuffleChars()
    assert( not obj.shuffleLett == obj.uniqueLett)
    print("testShuffleChars: PASSED")
       

if __name__ == '__main__':
    unittest.main()
    