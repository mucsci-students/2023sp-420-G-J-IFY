###############################################################################
# test_ObjectPool.py
# Author: Gaige Zakroski
# Date of Creation: 04-7-2023
#
# This module tests the ObjectPoolClass.
#
###############################################################################

import pytest
from model.ObjectPool import Thread, ThreadPool
import model.hint as hint
import model.output as output
import model.MakePuzzle as MakePuzzle

# Globals
outty = output.Output()


# Tests for Thread
# <public> Functions:
#   __init__(threadName : str) -> None:
#       Creates a thread
#
#   setThreadName(newName : str) -> None:
#       sets the thread name to a new name
#
#   getThreadName(self) -> str:
#       gets the name of a thread and returns it

@pytest.fixture
def puzzleThreadFixture():
    puzz = MakePuzzle.newPuzzle('warlock', 'a', outty, True)
    thread = Thread('Puzzle', puzz)
    return thread


@pytest.fixture
def outtyThreadFixture():
    thread = Thread('Output', outty)
    return thread


@pytest.fixture
def hintThreadFixture():
    puzz = MakePuzzle.newPuzzle('warlock', 'a', outty, True)
    hinty = hint.hint(puzz)
    thread = Thread('Hint', hinty)
    return thread


def testThreadContr(puzzleThreadFixture):
    assert (puzzleThreadFixture.threadName and
           puzzleThreadFixture.obj.__class__.__name__ == 'Puzzle')


def testSetThreadName(outtyThreadFixture):
    outtyThreadFixture.setThreadName('out')
    assert (outtyThreadFixture.threadName == 'out')


def testGetThreadName(hintThreadFixture):
    assert (hintThreadFixture.getThreadName() == 'Hint')


def testSetObject(puzzleThreadFixture):
    puzzleThreadFixture.setObject(outty)
    assert (isinstance(puzzleThreadFixture.obj, output.Output))


def testGetObjectThread(puzzleThreadFixture):
    assert (puzzleThreadFixture.getObject().__class__.__name__ == 'Puzzle')

# Tests for ThreadPool


@pytest.fixture
def threadPoolFullFixture(puzzleThreadFixture, hintThreadFixture,
                          outtyThreadFixture):
    return ThreadPool([puzzleThreadFixture, hintThreadFixture,
                       outtyThreadFixture])


@pytest.fixture
def threadPoolNotFullFixture(puzzleThreadFixture):
    return ThreadPool([puzzleThreadFixture])


def testContr(threadPoolFullFixture):
    assert (threadPoolFullFixture.size == 3)


def testContr2(threadPoolFullFixture):
    assert (threadPoolFullFixture.maxSize == 3)


def testContr3(threadPoolFullFixture):
    assert (threadPoolFullFixture.usedThreadList == [])


def testContr4(threadPoolFullFixture, puzzleThreadFixture, hintThreadFixture,
               outtyThreadFixture):
    assert (threadPoolFullFixture.availableThreadList ==
           [puzzleThreadFixture, hintThreadFixture, outtyThreadFixture])


def testAddThreadNotFull(threadPoolNotFullFixture, hintThreadFixture,
                         puzzleThreadFixture):
    threadPoolNotFullFixture.addThread(hintThreadFixture)
    assert (threadPoolNotFullFixture.size == 2 and
           threadPoolNotFullFixture.usedThreadList == [] and
           threadPoolNotFullFixture.availableThreadList ==
           [puzzleThreadFixture, hintThreadFixture])


def testAddThreadFull(threadPoolFullFixture, hintThreadFixture,
                      puzzleThreadFixture, outtyThreadFixture):
    with pytest.raises(Exception):
        threadPoolFullFixture.addThread(outtyThreadFixture)


def testGetThread(threadPoolFullFixture):
    thread = threadPoolFullFixture.getThread('Hint')
    assert (thread.getThreadName() == 'Hint' and
           len(threadPoolFullFixture.availableThreadList) == 2 and
           threadPoolFullFixture.usedThreadList == [thread])


def testGetThreadBad(threadPoolFullFixture):
    threadPoolFullFixture.getThread('Hint')
    with pytest.raises(AttributeError):
        threadPoolFullFixture.getThread('Hint')


def testReturnThread(threadPoolFullFixture):
    thread = threadPoolFullFixture.getThread('Hint')
    threadPoolFullFixture.returnThread(thread)
    assert (len(threadPoolFullFixture.availableThreadList) == 3 and
            len(threadPoolFullFixture.usedThreadList) == 0)


def testGetSize(threadPoolFullFixture):
    assert (threadPoolFullFixture.getSize() == 3)


def testGetAvailableThreadList(threadPoolFullFixture):
    assert (threadPoolFullFixture.getAvailableThreadList() ==
            ['Puzzle', 'Hint', 'Output'])


def testGetUsedThreadList(threadPoolFullFixture):
    threadPoolFullFixture.getThread('Hint')
    assert (threadPoolFullFixture.getUsedThreadList() == ['Hint'])


def testSetAvailableThreadList1(threadPoolFullFixture):
    thread = threadPoolFullFixture.getThread('Hint')
    threadPoolFullFixture.setAvailableThreadList([thread])
    assert (threadPoolFullFixture.availableThreadList == [thread])


def testSetAvailableThreadList2(threadPoolFullFixture):
    thread = threadPoolFullFixture.getThread('Hint')
    threadPoolFullFixture.setAvailableThreadList([thread])
    assert (threadPoolFullFixture.size == 1)


def testSetAvailableThreadList3(threadPoolFullFixture):
    thread = threadPoolFullFixture.getThread('Hint')
    threadPoolFullFixture.setAvailableThreadList([thread])
    assert (threadPoolFullFixture.usedThreadList == [])


def testReturnThreadBad(threadPoolFullFixture, hintThreadFixture):
    with pytest.raises(AttributeError):
        threadPoolFullFixture.returnThread(hintThreadFixture)


def testGetThreadBad2(threadPoolFullFixture, hintThreadFixture):
    threadPoolFullFixture.usedThreadList = [hintThreadFixture]
    with pytest.raises(AttributeError):
        threadPoolFullFixture.getThread('Hint')
