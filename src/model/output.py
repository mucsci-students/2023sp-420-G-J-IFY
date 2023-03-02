################################################################################
# Output.py
# Author: Jacob Lovegren
# Date of Creation: 03-01-2023
################################################################################


################################################################################
# class Output()
# Description:
#   An object to hole output for GUI and CLI from model
#
# <public> Attributes:
#   field : str
#
# <public> Functions:
#   setField(self, inStr : str)
#     - set the field field with a string
#
#   getField(self)
#     - return the string from field
################################################################################
class Output:
    def __init__(self):
        self.field = ""

    def setField(self, inStr):
        self.field = inStr

    def getField(self):
        return self.field