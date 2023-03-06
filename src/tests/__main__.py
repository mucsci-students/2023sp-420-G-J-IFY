# authors: Gaige Zakroski
# test file to tie all test together
import sys
import os

from pathlib import Path

print(Path.cwd())

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)


print('{str:-^{num}}'.format(str = 'Testing', num = 21))
import tests.saveStateTests
print('{str:-^{num}}'.format(str = '=', num = 40))
import tests.StateStorageTests
print('{str:-^{num}}'.format(str = '=', num = 40))
import tests.MakePuzzleTests
print('{str:-^{num}}'.format(str = '=', num = 40))
#import tests.saveCheckTests
#print('{str:-^{num}}'.format(str = '=', num = 40))


