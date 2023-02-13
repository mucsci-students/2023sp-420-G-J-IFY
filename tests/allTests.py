# authors: Gaige Zakroski
# test file to tie all test together
import pytest


print('{str:-^{num}}'.format(str = 'Testing', num = 21))
import saveStateTests
print('{str:-^{num}}'.format(str = '=', num = 40))
import StateStorageTests
print('{str:-^{num}}'.format(str = '=', num = 40))
import MakePuzzleTests
print('{str:-^{num}}'.format(str = '=', num = 40))

