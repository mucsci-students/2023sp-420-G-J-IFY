
import MakePuzzle
import saveState


# Test Cases for new puzzle

newPuzz = Puzzle('a', 'acklorw')
newPuzz.wordListStorage()
print(newPuzz.showAllWords())
#correct guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.showScore())
print(newPuzz.showFoundWords())
#bad letter
MakePuzzle.guess(newPuzz, 'wart')
print(newPuzz.showScore())
#too short
MakePuzzle.guess(newPuzz, 'war')
print(newPuzz.showScore())
#missing key
MakePuzzle.guess(newPuzz, 'cork')
print(newPuzz.showScore())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.showScore())
print(newPuzz.showFoundWords())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.showScore())
print(newPuzz.showFoundWords())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.showScore())
print(newPuzz.showFoundWords())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.showScore())
print(newPuzz.showFoundWords())
