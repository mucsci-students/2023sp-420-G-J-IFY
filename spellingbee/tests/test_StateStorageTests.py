# author: Gaige Zakroski
# tests for various parts of a StateStorage module
import pytest
import os.path
from os import path
import string
import random
import sys
import os
import StateStorage as spellingbee
import json
from model.puzzle import Puzzle
from model.output import Output
import MakePuzzle
from pathlib import Path
current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

# Globals
outty = Output.getInstance()
list = []


# Creates a random string of length 10
def makeRandomJsonName():
    letters = string.ascii_lowercase
    result = ""
    for i in range(10):
        result += random.choice(letters)
    return result


def makeShortestGame():
    obj = Puzzle('q', 'kamotiq')
    obj.allWordList = ['kamotiq']
    obj.maxScore = 14
    return obj


# Params: fileName    - name of the file to check
#       : dictToCheck -  the dictionary to comapre to the dictionary
#       in the file
# Checks the contents of a file and ensures the file has the correct data in it
# If the file does not have the correct data in it then an asserionError will
# be raised
def checkContents(fileName, dictToCheck):
    with open(fileName) as file:
        dict = json.load(file)
    return dict == dictToCheck


# Params: fileName - Name of the file
# Checks to see if the file exists in the current directory
# If the file specified does not exist in the directory then an assertionError
# will be raised
def checkIfExists(fileName):
    return path.isfile(fileName)


def __makeDict(saveStateObj):
    dict = {'RequiredLetter': saveStateObj.getKeyLetter(),
            'PuzzleLetters': saveStateObj.getUniqueLetters(),
            'CurrentPoints': saveStateObj.getScore(),
            'MaxPoints': saveStateObj.getMaxScore(),
            'GuessedWords': saveStateObj.getFoundWords(),
            'WordList': saveStateObj.getAllWords()}
    return dict


def __makeDict2(saveStateObj):
    dict = {'Author': 'GJIFY',
            'RequiredLetter': saveStateObj.getKeyLetter(),
            'PuzzleLetters': saveStateObj.getUniqueLetters(),
            'CurrentPoints': saveStateObj.getScore(),
            'MaxPoints': saveStateObj.getMaxScore(),
            'GuessedWords': saveStateObj.getFoundWords(),
            'WordList': saveStateObj.getAllWords()}
    return dict


def removeSave(fileName):
    path = str(Path.cwd()) + '/' + fileName
    os.remove(path)


# test if we save an empty game and a file is not already created with the same
# name a new one is created and empty
@pytest.fixture
def puzzleFixture():
    dict = {"RequiredLetter": "a", "PuzzleLetters": "acklorw",
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

    obj = Puzzle('a', 'warlock')

    obj.uniqueLett = dict["PuzzleLetters"]
    obj.allWordList = dict["WordList"]
    obj.maxScore = dict["MaxPoints"]
    return (obj, dict)


@pytest.fixture
def puzzleFixture2():
    dict = {"Author": "GJIFY",
            "RequiredLetter": "a", "PuzzleLetters": "acklorw",
            "CurrentPoints": 0, "MaxPoints": 323, "GuessedWords": [],
            "WordList": ["acro", "alar", "alow", "arak", "arco", "awol",
                         "caca", "calk", "call", "calo", "cark", "carl",
                         "carr", "claw", "coal", "coca", "cola", "craw",
                         "kaka", "kola", "kora", "lack", "lall", "lark",
                         "loca", "okra", "olla", "oral", "orca", "orra",
                         "rack", "roar", "wack", "walk", "wall", "wark",
                         "wawl", "acock", "alack", "allow", "arrow",
                         "cacao",
                         "calla", "carol", "clack", "claro", "cloak",
                         "coala",
                         "cocoa", "coral", "craal", "crack", "crawl",
                         "croak",
                         "karoo", "koala", "kraal", "local", "loral",
                         "wacko",
                         "walla", "wrack", "alcool", "arrack", "calcar",
                         "callow", "carack", "cloaca", "coccal", "collar",
                         "corral", "karroo", "wallow", "caracal",
                         "caracol",
                         "carrack", "cloacal", "corolla", "oarlock",
                         "warlock",
                         "warwork", "callaloo", "caracara", "rackwork",
                         "wallaroo"]
            }
    obj = Puzzle('a', 'warlock')

    obj.uniqueLett = dict["PuzzleLetters"]
    obj.allWordList = dict["WordList"]
    obj.maxScore = dict["MaxPoints"]
    return (obj, dict)


@pytest.fixture
def playedPuzzle(puzzleFixture):
    obj = puzzleFixture[0]
    MakePuzzle.guess(obj, "warlock", False)
    MakePuzzle.guess(obj, "warlock", False)
    MakePuzzle.guess(obj, "wrack", False)
    MakePuzzle.guess(obj, "alcool", False)
    return obj


@pytest.fixture
def saverObj(playedPuzzle):
    return spellingbee.Saver(playedPuzzle)


@pytest.fixture
def completedPuzzle():
    obj = makeShortestGame()
    MakePuzzle.guess(obj, 'kamotiq', False)
    return obj


@pytest.fixture
def makeBadFoundWordList():
    dictDict = {
        "RequiredLetter": "w",
        "PuzzleLetters": "cehinrw",
        "CurrentPoints": 7,
        "MaxPoints": 269,
        "GuessedWords": [
            "dickbutt",
            "bearfucker"
        ],
        "WordList": [
            "chew", "crew", "eeew", "ewer", "hewn", "ween", "weer", "weir",
            "were", "whee", "when", "whew", "whin", "whir", "wich", "wine",
            "wire", "wren", "hewer", "newer", "newie", "renew", "rewin",
            "wench", "wheen", "where", "which", "whine", "whirr", "wince",
            "winch", "wirer", "wrier", "chewer", "rechew", "rewire", "weenie",
            "weewee", "weiner", "whence", "whiner", "wiener", "wienie",
            "wincer", "winier", "winner", "wirier", "wrench", "chewier",
            "icewine", "renewer", "weenier", "wencher", "wennier", "wherein",
            "whinier", "wincher", "whinnier", "wrencher"
        ]
    }
    return dictDict


@pytest.fixture
def makeBadScoreGame():
    dict = {
        "RequiredLetter": "w",
        "PuzzleLetters": "cehinrw",
        "CurrentPoints": 600,
        "MaxPoints": 10000,
        "GuessedWords": [
            "wine",
            "winner"
        ],
        "WordList": [
            "chew", "crew", "eeew", "ewer", "hewn", "ween", "weer", "weir",
            "were", "whee", "when", "whew", "whin", "whir", "wich", "wine",
            "wire", "wren", "hewer", "newer", "newie", "renew", "rewin",
            "wench", "wheen", "where", "which", "whine", "whirr", "wince",
            "winch", "wirer", "wrier", "chewer", "rechew", "rewire", "weenie",
            "weewee", "weiner", "whence", "whiner", "wiener", "wienie",
            "wincer", "winier", "winner", "wirier", "wrench", "chewier",
            "icewine", "renewer", "weenier", "wencher", "wennier", "wherein",
            "whinier", "wincher", "whinnier", "wrencher"
        ]
    }
    return spellingbee.__setFields(dict)


@pytest.fixture
def makeBadUniqueLetters():
    dict = {
        "RequiredLetter": "w",
        "PuzzleLetters": "zaplwq",
        "CurrentPoints": 7,
        "MaxPoints": 269,
        "GuessedWords": [
            "wine",
            "winner"
        ],
        "WordList": [
            "chew", "crew", "eeew", "ewer", "hewn", "ween", "weer", "weir",
            "were", "whee", "when", "whew", "whin", "whir", "wich", "wine",
            "wire", "wren", "hewer", "newer", "newie", "renew", "rewin",
            "wench", "wheen", "where", "which", "whine", "whirr", "wince",
            "winch", "wirer", "wrier", "chewer", "rechew", "rewire", "weenie",
            "weewee", "weiner", "whence", "whiner", "wiener", "wienie",
            "wincer", "winier", "winner", "wirier", "wrench", "chewier",
            "icewine", "renewer", "weenier", "wencher", "wennier",
            "wherein", "whinier", "wincher", "whinnier", "wrencher"
        ]
    }
    return spellingbee.__setFields(dict)


def test__CheckFileExitsBadFile():
    with pytest.raises(FileNotFoundError):
        spellingbee.__checkFileExists(Path("./saves/KEEPTHISHERE.TX"))


def test__CheckFileExitsgoodFile():
    spellingbee.__checkFileExists(Path("./spellingbee"))


def testCorruptGameLoadFromExplorer():
    path = Path.cwd()
    pathToFile = str(path) + '/spellingbee/tests/TestFile.json'
    spellingbee.load(pathToFile)
    pytest.raises(AssertionError)


def testSaveFromExplorer(playedPuzzle):
    path = Path.cwd()
    savePath = str(path)
    fileName = 'TestFile2'
    spellingbee.saveFromExplorer(savePath, fileName, playedPuzzle, False)
    dict = __makeDict(playedPuzzle)
    assert (checkContents(fileName + '.json', dict))
    removeSave(fileName + '.json')


def testSaveFromExplorerPuzzleOnly(playedPuzzle, puzzleFixture):
    path = Path.cwd()
    savePath = str(path)
    fileName = 'TestFile2'
    spellingbee.saveFromExplorer(savePath, fileName, playedPuzzle, True)
    dict = puzzleFixture[1]
    assert (checkContents(fileName + '.json', dict))
    removeSave(fileName + '.json')


def testCheckLoadGood(playedPuzzle):
    dict1 = __makeDict(playedPuzzle)
    dict2 = spellingbee.checkLoad(__makeDict(playedPuzzle))
    assert (dict1 == dict2)


def testCheckLoadBadScore(makeBadScoreGame):
    path = Path.cwd()
    pathToFile = (str(path) + ''
                  '/spellingbee/tests/checkSavesTestFiles/badScoreGame.json')
    spellingbee.saveFromExplorer('./spellingbee/tests/checkSavesTestFiles',
                                 'badScoreGame', makeBadScoreGame, False)
    with open(pathToFile) as file:
        dict = json.load(file)
    assert (spellingbee.checkLoad(dict)['MaxPoints'] == 269 and spellingbee.
            checkLoad(dict)['CurrentPoints'] == 7)
    os.remove(pathToFile)


def testCheckCorruptJSONExplorer():
    with open('badJSON.json', 'w') as fp:
        json.dump({"makeGarbage": "trying"}, fp)
    fp.close()
    path = Path.cwd()
    pathToFile = (str(path) + '/badJSON.json')
    output = " contains critical errors that \nprevent the game from "
    output += "functioning properly\nReturning to game..."
    spellingbee.load(pathToFile)
    assert (outty.getField().endswith(output))
    os.remove(pathToFile)


def testCheckCorruptJSONsaveFolder():
    with open('badJSON.json', 'w') as fp:
        json.dump({"makeGarbage": "stilltrying"}, fp)
    fp.close()
    output = "The file badJSON.json contains critical errors that \n"
    output += "prevent the game from functioning properly\n"
    output += "Returning to game..."
    spellingbee.load('badJSON.json')
    assert (outty.getField() == output)


def testCheckGoodFile(puzzleFixture):
    with open('good.json', 'w') as fp:
        json.dump(puzzleFixture[1], fp)
    fp.close()
    path = Path.cwd()
    pathToFile = (str(path) + '/good.json')
    output = " contains critical errors that \nprevent the game from "
    output += "functioning properly\nReturning to game..."
    puzz = spellingbee.load(pathToFile)
    assert (puzz is not None)
    os.remove(pathToFile)


def testCheckLoadBadUniqueLetters(makeBadUniqueLetters):
    path = Path.cwd()
    pathToFile = (str(path) + '/spellingbee/tests/checkSavesTestFiles/'
                  'badUniqueLetters.json')
    spellingbee.saveFromExplorer('./spellingbee/tests/checkSavesTestFiles',
                                 'badUniqueLetters', makeBadUniqueLetters,
                                 False)
    with open(pathToFile) as file:
        dict = json.load(file)

    assert (spellingbee.checkLoad(dict) is None)
    os.remove(pathToFile)


def testCheckLoadBadFoundWordList(makeBadFoundWordList):
    dictDict = spellingbee.checkLoad(makeBadFoundWordList)
    assert (dictDict['GuessedWords'] == [])


def testExplorerJson(playedPuzzle):
    path = Path.cwd()
    savePath = str(path)
    fileName = 'TestFile2.json'
    spellingbee.saveFromExplorer(savePath, fileName, playedPuzzle, False)
    dict = __makeDict(playedPuzzle)
    assert (checkContents(fileName, dict))
    removeSave(fileName)


def testExecuteSaveFromExplorerCurrent(playedPuzzle):
    path = Path.cwd()
    savePath = str(path) + '/TestFile2.json'
    strat = spellingbee.Saver(spellingbee.savePuzzleStrategy())
    strat.executeStrategy(savePath, playedPuzzle, False)
    dict = __makeDict2(playedPuzzle)
    assert (checkContents('TestFile2.json', dict))


def testExecuteSaveFromExplorerPuzzle(playedPuzzle, puzzleFixture2):
    path = Path.cwd()
    savePath = str(path) + '/TestFile2.json'
    strat = spellingbee.Saver(spellingbee.savePuzzleStrategy())
    strat.executeStrategy(savePath, playedPuzzle, True)
    dict = puzzleFixture2[1]
    assert (checkContents('TestFile2.json', dict))
    removeSave('TestFile2.json')


def testStrategyContr():
    with pytest.raises(NotImplementedError):
        spellingbee.Strategy().exectute('him', None, None)


def testEncryptionCurrent(playedPuzzle):
    strat = spellingbee.Saver(spellingbee.encryptedSaveStrategy())
    pathz = Path.cwd()
    savePath = str(pathz) + '/ImHiM.json'
    strat.executeStrategy(savePath, playedPuzzle, False)
    obj = MakePuzzle.newPuzzle('warlock', 'a', False)
    strat = spellingbee.Saver(spellingbee.encryptedSaveStrategy())
    strat.executeStrategy(savePath, obj, False)
    him = spellingbee.load(savePath)
    assert (him.allWordList == obj.allWordList)


def testEncryptionPuzzle(playedPuzzle):
    strat = spellingbee.Saver(spellingbee.encryptedSaveStrategy())
    pathz = Path.cwd()
    savePath = str(pathz) + '/ImHiM.json'
    strat.executeStrategy(savePath, playedPuzzle, True)
    obj = MakePuzzle.newPuzzle('warlock', 'a', False)
    strat = spellingbee.Saver(spellingbee.encryptedSaveStrategy())
    strat.executeStrategy(savePath, obj, False)
    him = spellingbee.load(savePath)
    assert (him.getFoundWords() == [])


def testEncryptLoadNofile():
    pathz = Path.cwd()
    savePath = str(pathz)
    spellingbee.load(savePath + './cool')
    assert (outty.getField() == "The file " + savePath + './cool' +
            " does not exist in this directory\n"
            "Returning to game...")


def testEncryptLoadBadFile():
    pathz = Path.cwd()
    savePath = str(pathz) + '/badJSON.json'
    with open('badJSON.json', 'w') as fp:
        json.dump({"makeGarbage": "stilltrying"}, fp)
    fp.close()
    spellingbee.load(savePath)
    assert (outty.getField() == "The file " + savePath +
            " contains critical errors that \n"
            "prevent the game from functioning properly\n"
            "Returning to game...")
