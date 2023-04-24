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
from model.output import Output

outty = Output.getInstance()

###############################################################################
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
###############################################################################


def encryptionHandler(dict: dict, toEncrypt: bool) -> dict:
    try:
        if _dictKeyChecker(dict, "Author") and (_dictKeyChecker
                                                (dict, "WordList")
                                                or
                                                _dictKeyChecker
                                                (dict, "SecretWordList")):
            # Set password and plaintext
            password = dict["Author"]
            # Generate a random salt
            salt = _saltGrabber()
            # Derive a key from the password and salt using PBKDF2
            key = PBKDF2(password, salt, dkLen=32)

            if toEncrypt:
                # Call dictionary checker
                if _wordListTypeCheck(dict, "List"):
                    dict = _encryptList(key, dict["WordList"], dict)
            elif not toEncrypt:
                if _wordListTypeCheck(dict, "String"):
                    dict = _decryptList(key, dict["SecretWordList"], dict)
    except SyntaxError:
        outty.setField("ERROR!: Bad List Encryption")
    except ValueError:
        outty.setField("ERROR!: Bad Encryption")

    return dict

###############################################################################
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
###############################################################################


def _encryptList(key, wordList: list, dict: dict) -> dict:
    # Create an AES cipher object
    cipher = AES.new(key, AES.MODE_CBC)

    plainText = _convertWordListToString(wordList)
    newPlainText = plainText.encode('utf-8')

    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(pad(newPlainText, AES.block_size))
    # Grab file info
    dict["WordList"] = str(cipher.iv) + "duo" + str(ciphertext)
    dict["SecretWordList"] = dict.pop("WordList")

    return dict

###############################################################################
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
###############################################################################


def _decryptList(key, wordList: list, dict: dict) -> dict:
    newWordList = wordList.split("duo")
    iv = eval(newWordList[0].encode('utf-8'))
    decryptData = eval(newWordList[1].encode('utf-8'))

    # Create an AES cipher object using the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    plaintext = unpad(cipher.decrypt(decryptData), AES.block_size)

    newList = _convertToList(plaintext.decode('utf-8'))
    dict["SecretWordList"] = newList
    dict["WordList"] = dict.pop("SecretWordList")

    # Grab file info
    return dict

###############################################################################
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
###############################################################################


def _saltGrabber() -> bytes:
    salt = b'p\xf11\x15t\xdbQgc\xf4\xeb\x8d\xe6tu\xc6'
    # with open("DO_NOT_REMOVE_SALT.bin", "wb") as file:
    #    salt = file.read()
    return salt

###############################################################################
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
###############################################################################


def _convertWordListToString(wordList):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(wordList))


###############################################################################
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
###############################################################################


def _convertToList(string):
    li = list(string.split(" "))
    return li

###############################################################################
# _dictChecker(dict: dict) -> bool:
#
# DESCRIPTION:
#   verifies a dictioanry is usable for encryption handler
#
# PARAMETERS:
#   dict : dict
#     - dictionary that needs to be checked
#
# RETURNS:
#   bool
#     - where the dictionary is usable or not
###############################################################################


def _dictKeyChecker(dict: dict, keyName: str) -> bool:
    match keyName:
        case "Author":
            return keyName in dict
        case "WordList":
            return keyName in dict
        case "SecretWordList":
            return keyName in dict

###############################################################################
# _wordListList(dict: dict) -> bool:
#
# DESCRIPTION:
#   verifies a dictioanry is usable for encryption handler
#
# PARAMETERS:
#   dict : dict
#     - dictionary that needs to be checked
#
# RETURNS:
#   bool
#     - where the dictionary is usable or not
###############################################################################


def _wordListTypeCheck(dict: dict, typeCheck: str) -> bool:
    match typeCheck:
        case "List":
            return type(dict["WordList"]) is list
        case "String":
            return type(dict["SecretWordList"]) is str
