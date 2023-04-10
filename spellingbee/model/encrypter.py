###############################################################################
# encrypter.py
# Author: Yah'hymbey Baruti Ali-Bey
# Date of Creation: 4-8-2023
#
# Gets a dictionary and encrypts the word list from that dictionary 
# or decrypts a wordlist from the dictionary
#
# (Global, public) functions:
#   encryptionHandler(dict, toEncrypt) -> Dict
#
###############################################################################
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
    
################################################################################
# encryptionHandler(dict : dict, toEncrypt: bool) -> dict:
#
# DESCRIPTION:
#   Handles whether a dict needs to be encrypted or decrypted
# 
# PARAMETERS:
#   usrinput : str
#     - String provided by user containing either a guess, a command, or bad
#       input.
#   toEncrypt : bool
#     - boolean value to determine if the file needs to be encrypted or 
#       decrypted
#
# RETURNS:
#   dict
#     - encrypted or decrypted dict
################################################################################
def encryptionHandler(dict : dict, toEncrypt: bool) -> dict:
    # Set password and plaintext
    password = dict["Author"]

    # Generate a random salt
    salt = _saltGrabber()
    # Derive a key from the password and salt using PBKDF2
    key = PBKDF2(password, salt, dkLen=32)
    
    if toEncrypt: 
       newDict = _encryptList(key, dict["WordList"], dict)
    elif not toEncrypt:
       newDict = _decryptList(key, dict["WordList"], dict)
    
    return newDict

################################################################################
# encryptList(key, wordList : list, dict : dict) -> dict:
#
# DESCRIPTION:
#   Encryptes a wordlist
# 
# PARAMETERS:
#   key
#     - Key needed to encrypt the list
#   wordList : List
#     - List that needs to be encrypted
#   dict : dict
#     - Dictionary containing the wordlist
#
# RETURNS:
#   dict
#     - dictionary with encrypted word list
################################################################################
def _encryptList(key, wordList: list, dict: dict) -> dict:
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
# decryptList(key, wordList : list, dict : dict) -> dict:
#
# DESCRIPTION:
#   decryptes a wordlist
# 
# PARAMETERS:
#   key
#     - Key needed to decrypt the list
#   wordList : List
#     - List that needs to be encrypted
#   dict : dict
#     - Dictionary containing the wordlist
#
# RETURNS:
#   dict
#     - dictionary with decrypted word list
################################################################################
def _decryptList(key, wordList: list, dict: dict) -> dict:
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
# _saltGrabber() -> bytes:
#
# DESCRIPTION:
#   grabs salt for encryptions
# 
# PARAMETERS:
#
# RETURNS:
#   salt
#     - random binary for encryption
################################################################################
def _saltGrabber() -> bytes:
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
#   wordList : list
#     - wordList that needs to be converted to a stringS
# RETURNS:
#   wordList
#     - string representation of wordlist
################################################################################
def _convertWordListToString(wordList):
    # initialize an empty string
    str1 = " "
   
    # return string 
    return (str1.join(wordList))

################################################################################
# _convertToList(string: str) -> list:
#
# DESCRIPTION:
#   converts a string to a list
# 
# PARAMETERS:
#   string : str
#     - String provided by user containing either a guess, a command, or bad
#
# RETURNS:
#   li
#     - list representation of a string
################################################################################
def _convertToList(string):
    li = list(string.split(" "))
    return li