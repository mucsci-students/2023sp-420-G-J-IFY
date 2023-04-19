from model.output import Output
import pytest


def testObjectEquality():
    outty1 = Output.getInstance()
    outty2 = Output.getInstance()
    assert outty1 is outty2


def testObjectDuplicate():
    with pytest.raises(Exception):
        Output.getInstance()
        Output()


def testGetField():
    outty1 = Output.getInstance()
    outty2 = Output.getInstance()
    outty1.setField('Testing Output.getField()')
    assert outty2.getField() == 'Testing Output.getField()'


def testSetField():
    outty = Output.getInstance()
    outty.setField('Testing Output.setField()')
    assert outty.getField() == 'Testing Output.setField()'
