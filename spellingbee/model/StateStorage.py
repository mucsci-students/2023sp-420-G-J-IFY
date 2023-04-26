###############################################################################
# StateStorage.py
# Author: Gaige Zakroski, Yah'hymbey Baruti Ali-Bey, Jacob Lovegren
# Date of Creation: 2-8-2023
#
# A Module that contains many functions that will be capable of saving
# and loading the state of a game from a json file
#
# (Global, public) functions:
#   savePuzzle(saveStateObj: Obj, fileName : str)
#       - Saves a blank puzzle state
#   loadPuzzle(fileName : str) -> Puzzle Obj
#       - Loads a saved puzzle
#   saveCurrent(puzzle: Obj, fileName : str)
#       - Saves a current state of a puzzle
###############################################################################
import sys
import os
import sqlite3
import MakePuzzle
import json
import os.path
import model
from pathlib import Path
from model.output import Output
import encrypter

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

outty = Output.getInstance()


###############################################################################
# class NotInDBException(Exception)
# Description:
#   An exception for when a unique/key combo does not exist in our DB
#
# Arguments:
#   EXCEPTION : EXCEPTION
###############################################################################
class NotInDBException(Exception):
    pass


###############################################################################
# class BadJSONException(Exception)
# Description:
#   An exception for when a critical error occured in a json load format
#
# Arguments:
#   EXCEPTION : EXCEPTION
###############################################################################
class BadJSONException(Exception):
    pass


###############################################################################
# __makeDict(saveStateObj: obj) -> dict
#
# DESCRIPTION:
#   Takes a saveState objects fields and puts them into a dictionary to make
#   saving easier
#
# PARAMETERS:
#   saveStateObj: obj
#     - A saveState object
#
# RETURNS:
#   dict
#     - Returns a dictionary of all fields of a saveState object
###############################################################################
def __makeDict(saveStateObj):
    dict = {
        "RequiredLetter": saveStateObj.getKeyLetter(),
        "PuzzleLetters": saveStateObj.getUniqueLetters(),
        "CurrentPoints": saveStateObj.getScore(),
        "MaxPoints": saveStateObj.getMaxScore(),
        "GuessedWords": saveStateObj.getFoundWords(),
        "WordList": saveStateObj.getAllWords(),
    }
    return dict


###############################################################################
# __setFields(dict: dict) -> obj
#
# DESCRIPTION:
#   Sets the fields of the saveState object to the corisponing value in the
# dictionary
#
# PARAMETERS:
#   dict: dict
#     - A dictionary that contains the values of each feild of a saveState
# Object
#
# RETURNS:
#   obj
#     - Returns a saveState Object with all its fields set
###############################################################################
def __setFields(dict):
    obj = model.Puzzle(dict["RequiredLetter"], dict["PuzzleLetters"])
    obj.shuffleChars()
    obj.setScore(dict["CurrentPoints"])
    obj.setMaxScore(dict["MaxPoints"])
    obj.setFoundWords(dict["GuessedWords"])
    obj.setAllWordList(dict["WordList"])
    obj.setRank = obj.updateRank()
    return obj


###############################################################################
# __checkFileExists(pathToFile: str) -> bool
#
# DESCRIPTION:
#   Checks to see if a file exists in the current directory
#
# PARAMETERS:
#   pathToFIle : str
#     - Path to a specified file
#
# RETURNS:
#   p.exists()
#     - True if file does exist and false otherwise
#
# RAISES:
#  FileNotFoundError
#     - If path to file does not exist
###############################################################################
def __checkFileExists(pathToFile):
    p = pathToFile
    if not p.exists():
        raise FileNotFoundError
    else:
        return p.exists()


###############################################################################
# LoadFromExplorer(pathTOFile, outty)
#
# DESCRIPTION:
#   Will load a file using its path instead of its fileName
# PARAMETERS:
#   path : Path
#      - The path to the file being loaded
#
# RETURNS:
#   None
###############################################################################
def load(path: Path):
    try:
        f = open(path)

        dict = json.load(f)
        if "SecretWordList" in dict:
            dict = encrypter.encryptionHandler(dict, False)
        dict = checkLoad(dict)
        if dict is None:
            raise BadJSONException
        obj = __setFields(dict)
        return obj
    except FileNotFoundError:
        # If fileName does not exist then a FileNotFoundError is
        # raised saying the file does not exist
        outty.setField(
            "The file " + path + " does not exist in this directory\n"
            "Returning to game..."
        )
    except BadJSONException:
        outty.setField(
            "The file " + path + " contains critical errors that \n"
            "prevent the game from functioning properly\n"
            "Returning to game..."
        )


###############################################################################
# allLower(my_list : list(str)) -> list(str)
#
# DESCRIPTION:
#   This helper function changes all strings in a list to lower case
#
# PARAMETERS:
#   my_list
#       - A list of strings of unkown case
#
# RETURNS:
#   list(str)
#       - A list of strings in lower case
###############################################################################
def allLower(my_list):
    return [x.lower() for x in my_list]


###############################################################################
# checkLoad(loadFields)
#
# DESCRIPTION:
#   This fucntion checks all the possible reasons why our app could fail from
#   a foreign load
#
# PARAMETERS:
#   - dictDict - a dictionary of the .json fields
#
# RETURNS:
#   - Valid dictionary for game or None if invalid save file
#
# RAISES:
#   Exception for any load that will crash our program
###############################################################################
def checkLoad(dictDict):
    # SQLite Connections
    wordDict = sqlite3.connect("spellingbee/model/wordDict.db")
    cursor = wordDict.cursor()

    try:
        # Load specific dictionary fields into local variables
        # THROWS EXCEPTION IF KEY IS NOT IN DICT
        guessedWords = allLower(dictDict["GuessedWords"])
        puzzleLetters = dictDict["PuzzleLetters"].lower()
        requiredLetter = dictDict["RequiredLetter"].lower()
        currentPoints = dictDict["CurrentPoints"]
    # KeyError is raised IF the fields in the .json do not match the standard
    except KeyError:
        return None

    try:
        # Check if the unique letters/keyletter combo is in our DB
        # Append requiredLetter to puzzleLetters just in case they fucked
        # Up how they store the required letters
        uniqueLetters = "".join(sorted(set(puzzleLetters + requiredLetter)))
        cursor.execute(
            "select score from allGames where uniqueLetters = '"
            + uniqueLetters
            + "' and keyLetter = '"
            + requiredLetter
            + "';"
        )
        score = cursor.fetchone()
        # If the score isn't in our DB, then its not a valid game,
        # Reject the game
        if score is None:
            raise NotInDBException
    # NotinDBException is raised IF the game doesn't exist in our DB
    except NotInDBException:
        wordDict.commit()
        wordDict.close()
        return None

    # Just remake score and word list from our DB
    maxPoints = score[0]
    # GenerateWordList every time
    wordList = MakePuzzle.getAllWordsFromPangram(puzzleLetters,
                                                 requiredLetter)

    badWords = []

    # Check to make sure all guesses are valid
    if not set(guessedWords).issubset(set(wordList)):
        for word in guessedWords:
            # Make a list of all the bad guesses
            if word not in wordList:
                badWords.append(word)
        for thing in badWords:
            guessedWords.remove(thing)

    # Rescore the validated guess list
    tempTable = "create temporary table guessWords (guesses);"
    cursor.execute(tempTable)
    querey = "insert into guessWords (guesses) values ('"
    for a in guessedWords:
        querey += a + "'), ('"
    querey += "');"
    cursor.execute(querey)
    join = """
        select sum(wordScore) from dictionary join guessWords
        on dictionary.fullWord is guessWords.guesses;
        """
    cursor.execute(join)
    # This is what our score should be
    ourScore = cursor.fetchone()[0]
    # If there's doesn't match, set it to ours
    if ourScore is None:
        ourScore = 0
    if ourScore != currentPoints:
        currentPoints = ourScore

    # At this point, all fields are validates in our game,
    # remake dictionary
    dictDict["GuessedWords"] = guessedWords
    dictDict["WordList"] = wordList
    dictDict["PuzzleLetters"] = uniqueLetters
    dictDict["RequiredLetter"] = requiredLetter
    dictDict["CurrentPoints"] = currentPoints
    dictDict["MaxPoints"] = maxPoints

    # Close DB
    wordDict.commit()
    wordDict.close()
    # Return validated dictionary
    return dictDict


class Strategy:
    def exectute(self, path: str | None,
                 puzzle: object, onlyPuzz: bool | None):
        raise NotImplementedError

    def _makeDict(self, saveStateObj):
        dict = {
            "Author": "GJIFY",
            "RequiredLetter": saveStateObj.getKeyLetter(),
            "PuzzleLetters": saveStateObj.getUniqueLetters(),
            "CurrentPoints": saveStateObj.getScore(),
            "MaxPoints": saveStateObj.getMaxScore(),
            "GuessedWords": saveStateObj.getFoundWords(),
            "WordList": saveStateObj.getAllWords(),
        }
        return dict


class savePuzzleStrategy(Strategy):
    ###########################################################################
    # execute(path : string, fileName : str,
    # puzzle : object, onlyPuzz : bool) -> None:
    #
    # DESCRIPTION:
    #   This function saves a puzzle either with current progress or
    # just the puzzle its self
    #
    # PARAMETERS:
    #   path : str
    #      - Path to the folder where the save needs to go
    #   fileName: str
    #      - Name of the file
    #   puzzle : object
    #      - The game object that needs to be saved
    #   onlyPuzz: bool
    #      - A flag true if we are to only save the puzzle with no progress
    # and false if we are ton save the current state
    #
    # RETURNS:
    #   None
    ###########################################################################
    def exectute(self, filePath: str | None, puzzle: object,
                 onlyPuzz: bool | None):
        if onlyPuzz:
            newObj = model.Puzzle(puzzle.getKeyLetter(),
                                  puzzle.getUniqueLetters())
            newObj.setMaxScore(puzzle.getMaxScore())
            newObj.setAllWordList(puzzle.getAllWords())
            newObj.updateRank()
            dict = self._makeDict(newObj)
        else:
            dict = self._makeDict(puzzle)
        with open(filePath, "w") as file:
            json.dump(dict, file)


class encryptedSaveStrategy(Strategy):
    ###########################################################################
    # execute(path : string, fileName : str,
    # puzzle : object, onlyPuzz : bool) -> None:
    #
    # DESCRIPTION:
    #   This function saves a puzzle either with current progress or
    # just the puzzle its self and encrypts the word list
    #
    # PARAMETERS:
    #
    #   path : str
    #      - Path to the folder where the save needs to go
    #   fileName: str
    #      - Name of the file
    #   puzzle : object
    #      - The game object that needs to be saved
    #   onlyPuzz: bool
    #      - A flag true if we are to only save the puzzle with no progress
    # and false if we are ton save the current state
    #
    # RETURNS:
    #   None
    ###########################################################################
    def exectute(self, filePath: str | None, puzzle: object,
                 onlyPuzz: bool | None):
        dict = self._makeDict(puzzle)
        encryptedDict = encrypter.encryptionHandler(dict, True)
        if onlyPuzz:
            encryptedDict['GuessedWords'] = []
            encryptedDict['CurrentScore'] = 0
        with open(filePath, "w") as file:
            json.dump(encryptedDict, file)


class Saver:
    def __init__(self, strategy: Strategy):
        # makes a copy of the current puzzle
        self.strategy = strategy

    ###########################################################################
    # executeStrategy(self, path: str | None, fileName: str, puzzle: object,
    #                 onlyPuzz: bool | None):
    #
    # DESCRIPTION:
    #   exectutes a strategy
    #
    # PARAMETERS:
    #
    #   path : str
    #      - Path to the folder where the save needs to go
    #   fileName: str
    #      - Name of the file
    #   puzzle : object
    #      - The game object that needs to be saved
    #   onlyPuzz: bool
    #      - A flag true if we are to only save the puzzle with no progress
    # and false if we are ton save the current state
    #
    # RETURNS:
    #   NONE
    ###########################################################################
    def executeStrategy(self, filePath: str | None, puzzle: object,
                        onlyPuzz: bool | None):
        self.strategy.exectute(filePath, puzzle, onlyPuzz)
