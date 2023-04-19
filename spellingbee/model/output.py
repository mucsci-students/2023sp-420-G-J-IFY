###############################################################################
# Output.py
# Author: Jacob Lovegren
# Date of Creation: 03-01-2023
###############################################################################
###############################################################################
# class Output()
# Description:
#   An object to hole output for GUI and CLI from model
#
# <public> Attributes:
#   field : str
#
# <public> Functions:
#   setField(self, inStr : str)
#     - Set the field field with a string
#
#   getField(self)
#     - Return the string from field
###############################################################################
class Output:
    __instance = None

    @staticmethod
    def getInstance():
        if Output.__instance is None:
            Output()
        return Output.__instance

    def __init__(self):
        if Output.__instance is not None:
            raise Exception('Multiple instances of Output is disallowed')
        else:
            Output.__instance = self
            self.field = ''

    def setField(self, inStr):
        self.field = inStr

    def getField(self):
        return self.field
