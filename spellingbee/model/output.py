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
class Output(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Output, cls).__new__(cls)
            cls.instance.field = ''
        return cls.instance

    def setField(self, inStr):
        self.field = inStr

    def getField(self):
        return self.field
