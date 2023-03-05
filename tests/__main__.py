# authors: Gaige Zakroski
# test file to tie all test together
import sys
import os


current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)


print('{str:-^{num}}'.format(str = 'Testing', num = 21))
import saveStateTests
print('{str:-^{num}}'.format(str = '=', num = 40))
import StateStorageTests
print('{str:-^{num}}'.format(str = '=', num = 40))
import MakePuzzleTests
print('{str:-^{num}}'.format(str = '=', num = 40))
import saveCheckTests
print('{str:-^{num}}'.format(str = '=', num = 40))


