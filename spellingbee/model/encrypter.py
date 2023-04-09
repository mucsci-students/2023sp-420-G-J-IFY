###############################################################################
# encrypter.py
# Author: Yah'hymbey Baruti Ali-Bey
# Date of Creation: 4-8-2023
#
# Gets a dictionary and encrypts the word list from that dictionary
#
# (Global, public) functions:
#   encryptList(key, wordList, dict) -> Dict
#   decrpytList(key, wordList, dict) -> Dict
#   encryptionHandler(dict, toEncrypt) -> Dict
#
###############################################################################
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad


# Test Code
def compareList(l1, l2):
    if (len(l1) != len(l2)):
        print("Lengths do not match")
        return
    
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            print("Word at index " + i + "does not equal")
            return
            
    print("It works!!")

################################################################################
# encryptList(key, wordList : list, dict : dict) -> dict:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
# 
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - Puzzle object storing current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - Updated puzzle object
################################################################################
def encryptList(key, wordList, dict):
    # Create an AES cipher object
    cipher = AES.new(key, AES.MODE_CBC)
        
    plainText = _convertWordListToString(wordList)
    newPlainText = plainText.encode('utf-8')
    
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(pad(newPlainText, AES.block_size))
    # Grab file info
    dict["WordList"] = [str(cipher.iv), str(ciphertext)]
    
    return dict

################################################################################
# parse(key, wordList : list, dict : dict) -> dict:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
# 
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - Puzzle object storing current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - Updated puzzle object
################################################################################
def decryptList(key, wordList, dict):
    iv = eval(wordList[0].encode('utf-8'))
    decryptData = eval(wordList[1].encode('utf-8'))

    # Create an AES cipher object using the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    plaintext = unpad(cipher.decrypt(decryptData), AES.block_size)
    
    newList = _convertToList(plaintext.decode('utf-8'))
    dict["WordList"] = newList

    # Grab file info
    return dict
        
################################################################################
# parse(dict : dict, toEncrypt: bool) -> dict:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
# 
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - Puzzle object storing current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - Updated puzzle object
################################################################################
def encryptionHandler(dict, toEncrypt):
    # Set password and plaintext
    password = dict["Author"]

    # Generate a random salt
    salt = _saltGrabber()
    # Derive a key from the password and salt using PBKDF2
    key = PBKDF2(password, salt, dkLen=32)
    
    if toEncrypt: 
       newDict = encryptList(key, dict["WordList"], dict)
    if not toEncrypt:
       newDict = decryptList(key, dict["WordList"], dict)
    
    return newDict
    

################################################################################
# parse() -> bytes:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
# 
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - Puzzle object storing current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - Updated puzzle object
################################################################################
def _saltGrabber():
    salt = " "
    with open("DO_NOT_REMOVE.bin", "wb") as file:
        salt = file.read()
    return salt

################################################################################
# parse(wordList : list) -> str:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
# 
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - Puzzle object storing current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - Updated puzzle object
################################################################################
def _convertWordListToString(wordList):
    # initialize an empty string
    str1 = " "
   
    # return string 
    return (str1.join(wordList))

################################################################################
# parse(string: str) -> list:
#
# DESCRIPTION:
#   Directs game functionality based on string input, game object
# 
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   game : object
#     - Puzzle object storing current game state
#   outty : object
#     - Output object storing output strings
#
# RETURNS:
#   object
#     - Updated puzzle object
################################################################################
def _convertToList(string):
    li = list(string.split(" "))
    return li