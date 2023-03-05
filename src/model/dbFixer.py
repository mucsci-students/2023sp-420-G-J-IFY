################################################################################
# dbFixer.py
# Author: Gaige Zakroski, 
# Date of Creation: 3-1-2023
#
#a module that goes to the db file and then leaves
#
# (Global, public) functions:
#   goToDB() -> None
#   LeaveDB() -> None
################################################################################


import os
from os import path

from pathlib import Path

################################################################################
# goToDB() -> None
#
# DESCRIPTION:
#  Moves directorys to the DB
#
# PARAMETERS:
# NONE
#
# RETURNS:
#  result 
#       bool value stating if we moved to the db
#
################################################################################
def goToDB() -> bool:
    # move down into the db
    os.chdir('./src/model')
    #return checkExists()

################################################################################
# leaveDB() -> None
#
# DESCRIPTION:
#  leaves the folder with Database
#
# PARAMETERS:
#   None
#
# RETURNS:
#   bool stating if we left the dict correctly and we are in the top level dir
#
################################################################################
def leaveDB() -> bool:
    os.chdir('..')
    os.chdir('..')
    #return not checkExists()


################################################################################
# checkExists() -> None
#
# DESCRIPTION:
#   sees if the db is in the current directory
#
# PARAMETERS:
# 
#
# RETURNS:
#  
#
################################################################################

def checkExists() -> None:
    return path.exists('wordDict.db')
