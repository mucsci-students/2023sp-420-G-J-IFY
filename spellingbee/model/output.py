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

    ###########################################################################
    # getInstance() -> Output
    #
    # DESCRIPTION:
    #   If there is not yet an existing instance of Output, a new one is
    #     created and returned. Otherwise the existing instance is returned
    ###########################################################################
    @staticmethod
    def getInstance() -> object:
        if Output.__instance is None:
            Output()
        return Output.__instance

    ###########################################################################
    # __init__()
    #
    # DESCRIPTION:
    #   If there is already an existing instance of Output, an exception is
    #     thrown with message 'Multiple instances of Output is disallowed'
    #     Otherwise the instance becomes self.
    #
    # RAISES
    #   Exception
    #     - constructor is called after an instance of Output is already
    #         created
    ###########################################################################
    def __init__(self):
        if Output.__instance is not None:
            raise Exception('Multiple instances of Output is disallowed')
        else:
            Output.__instance = self
            self.field = ''

    ###########################################################################
    # setField(inStr: str) -> None
    #
    # DESCRIPTION
    #   sets the stored string field to proveded inStr
    ###########################################################################
    def setField(self, inStr: str) -> None:
        self.field = inStr

    ###########################################################################
    # getField() -> str
    #
    # DESCRIPTION
    #   returns the stored string field
    ###########################################################################
    def getField(self) -> str:
        return self.field
