
import MakePuzzle
import puzzle


# Test Cases for new puzzle

newPuzz = Puzzle('a', 'acklorw')
newPuzz.wordListStorage()
print(newPuzz.getAllWords())
#correct guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.getScore())
print(newPuzz.getFoundWords())
#bad letter
MakePuzzle.guess(newPuzz, 'wart')
print(newPuzz.getScore())
#too short
MakePuzzle.guess(newPuzz, 'war')
print(newPuzz.getScore())
#missing key
MakePuzzle.guess(newPuzz, 'cork')
print(newPuzz.getScore())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.getScore())
print(newPuzz.getFoundWords())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.getScore())
print(newPuzz.getFoundWords())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.getScore())
print(newPuzz.getFoundWords())
#double guess
MakePuzzle.guess(newPuzz, 'warlock')
print(newPuzz.getScore())
print(newPuzz.getFoundWords())
