#!/usr/bin/env python3

import os
import crypt
import sys
import hashlib

from output_functions import *

hashType    = sys.argv[1]
LogsToCrack = sys.argv[2]
DictFile    = sys.argv[3]
result      = {}

###################################
#                                 #
#      Preprocess                 #
#                                 #
###################################

def main():
    if (areArgsValids() == True):
        startCracking()
        writeResultInFile()
    printBye()

def areArgsValids():
    if len(sys.argv) != 4:
        return argLenError()
    if isNotValidFile(LogsToCrack) or isNotValidFile(DictFile):
        return False
    if isNotValidHash():
        return errorInHash(HashType)
    return True

def isNotValidFile(filename):
    if not os.path.isfile(filename):
        return fileDoNotExist(filename)
    elif not os.access(filename, os.R_OK):
        return wrongPermOnFile(filename)
    return False

def isNotValidHash():
    validHash = ("all", "unix_crypt", "md5", "sha256", "sha512")
    return not (hashType.lower() in validHash)

def writeResultInFile():
    with open("crackingResult.passwd", "a+") as res:
        for user in result:
            res.write(user + ":" + result[user])
    printWhereFindOutput()


###################################
#                                 #
#     Initialisation Cracking     #
#                                 #
###################################

def startCracking():
    logFile = open(LogsToCrack)
    for line in logFile.readlines():
        passToCrack = line.split(':')[1].strip('\n')
        user        = line.split(':')[0]
        hashName    = setHashName()
        for hsh in hashName:
            printFront('+', col.YELLOW)
            print ("Start cracking with " + hsh + " hash")
            res = redirectHsh(hsh, DictFile, passToCrack)
            if (res != False):
                addSolution(user, res)
                printSuccess(user, passToCrack, res)
                break ;
            else:
                printFailure(user, passToCrack, hsh)


def setHashName():
    hashName = hashType.lower()
    if (hashName == "all"):
        return ["unix_crypt", "md5", "sha256", "sha512"]
    return [hashName]


def redirectHsh(hsh, filename, passToCrack):
    if (hsh == "unix_crypt"):
        return crackUnixCrypt(filename, passToCrack)
    elif (hsh == "md5"):
        return crackMD5(filename, passToCrack)
    elif (hsh == "sha256"):
        return crackSHA256(filename, passToCrack)
    elif (hsh == "sha512"):
        return crackSHA512(filename, passToCrack)
    return False

def addSolution(user, res):
    result[user] = res

###################################
#                                 #
#   Hash Cracking                 #
#                                 #
###################################

## CRACKING UNIX ENCRYPTION

def crackUnixCrypt(filename, password):
    dictFile = open(filename)
    salt = password[:2]
    if invalidSalt(salt):
        return False
    for word in dictFile.readlines():
        if (cmpGeneratePassHash(salt, word, password)):
            return (word)
    return False

def invalidSalt(salt):
    if False in map(lambda x: x is ascii, salt):
        return False
    return True

def cmpGeneratePassHash(salt, word, password):
    if (crypt.crypt(word.replace('\n', ''), salt) == password):
        return True
    return False


## MD5 ENCRYPTION

def crackMD5(filename, password):
    dictFile = open(filename)
    for word in dictFile.readlines():
        cpy = word
        word = str.encode(word.strip('\n'))
        if (password == hashlib.md5(word).hexdigest()):
            return (cpy)
    return False

## SHA256 ENCRYPTION

def crackSHA256(filename, password):
    dictFile = open(filename)
    for word in dictFile.readlines():
        cpy = word
        word = str.encode(word.strip('\n'))
        if (password == hashlib.sha256(word).hexdigest()):
            return (cpy)
    return False

## SHA512 ENCRYPTION

def crackSHA512(filename, password):
    dictFile = open(filename)
    for word in dictFile.readlines():
        cpy = word
        word = str.encode(word.strip('\n'))
        if (password == hashlib.sha512(word).hexdigest()):
            return (cpy)
    return False


if __name__ in '__main__':
    main()
