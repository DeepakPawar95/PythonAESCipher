#!/usr/bin/python
import os
import struct
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class bcolors:
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   RED = '\033[31m'
   ENDC = '\033[0m'

# Function to encrypt message with the user password
def encryptMessage(key, filename):
    chunksize = 64 * 256
    outputFile = "en_" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)		# File size is stored in first 16-byte
    IV = Random.new().read(16)					# Random 16-byte initialisation vector 

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

	print(bcolors.GREEN + "\n\n[Encrypted message stored in file]: en_" + filename + "\n\n")

# Function to create key from user password
def createKey(password):
            hasher = SHA256.new(password.encode('utf-8'))
            return hasher.digest()


print(bcolors.RED + "\n#############################################################\n")
print(bcolors.RED + "		Python AES Encryptor		")
print(bcolors.RED + "\n#############################################################\n\n")


# Get filename and password from user
filename = raw_input(bcolors.BLUE + "[Message Filename]: " + bcolors.ENDC)
password = raw_input(bcolors.BLUE + "[Password]: " + bcolors.ENDC)

key = createKey(password)
encryptMessage(key, filename)

