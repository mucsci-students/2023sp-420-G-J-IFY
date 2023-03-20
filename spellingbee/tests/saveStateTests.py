# authors: Gaige Zakroski
import sys
import os


current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)
#import spellingbee
import unittest
import model.puzzle as Puzzle


# tests the constuctor
class testSaveState(unittest.TestCase):
    #test constuctor
    obj = Puzzle.Puzzle('a', 'warlock')
    assert(obj.keyLett == 'a')
    assert(obj.uniqueLett == 'warlock')
    assert(obj.shuffleLett == 'warlock')
    assert(obj.score == 0)
    assert(obj.maxScore == 0)
    assert(obj.foundWordList == [])
    assert(obj.allWordList == [])
    assert(obj.rank == ' ')
    print("testConstructor: PASSED")
            
        
    #test get keyLetter
    assert(obj.getKeyLetter() == obj.keyLett)
    print("testgetKeyLetter: PASSED")
        
    # test getUniqueLetters
    assert(obj.getUniqueLetters() == obj.uniqueLett)
    print("testgetUniqueLetters: PASSED")
        
    # test getShuffleLetters
    assert(obj.getShuffleLetters() == obj.shuffleLett)
    print("testgetShuffleLetters: PASSED")

    # test getMaxScore
    assert(obj.getMaxScore() == obj.maxScore )
    print("testgetMaxScore: PASSED")
        
    # testgetFoundWords
    assert(obj.getFoundWords() == obj.foundWordList)
    print("testgetFoundWords: PASSED")
    # test getAllWords
    assert(obj.getAllWords() == obj.allWordList)
    print("testgetAllWords: PASSED")
    
    # testgetScore
    assert(obj.getScore() == obj.score)
    print("testgetScore: PASSED")
    
    # test getRank
    assert(obj.getRank() == obj.rank)
    print("testgetScore: PASSED")

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
    assert(obj.getFoundWords() == ["warlock", "wrack", "alcool", "arrack", "wallaroo"])
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
    