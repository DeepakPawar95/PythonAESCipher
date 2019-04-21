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

# Function to decrypt given file message using user password
def decryptMessage(key, filename):
    chunksize = 64 * 256
    outputfile = "de_" + filename
    
    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))			# File size from first 16-byte
        IV = infile.read(16)				# Initialisation vector from next 16-byte
        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputfile, 'wb') as outfile:
            while True:
                msg = infile.read(chunksize)
                msg_length = len(msg)

                if msg_length == 0:
                    break

                decrypted_msg = decryptor.decrypt(msg)
                decrypted_length = len(decrypted_msg)

                if filesize > decrypted_length:
                    outfile.write(decrypted_msg)
                else:
                    outfile.write(decrypted_msg[:filesize])

                filesize -= decrypted_length

	    print(bcolors.GREEN + "\n\n[Decrypted message stored in file]: de_" + filename + "\n\n")

# Function to create key from user password
def createKey(password):
            hasher = SHA256.new(password.encode('utf-8'))
            return hasher.digest()


print(bcolors.RED + "\n#############################################################\n")
print(bcolors.RED + "           Python AES Decryptor            ")
print(bcolors.RED + "\n#############################################################\n\n")


# Get filename and password from user
filename = raw_input(bcolors.BLUE + "[Message Filename]: " + bcolors.ENDC)
password = raw_input(bcolors.BLUE + "[Password]: " + bcolors.ENDC)


key = createKey(password)
decryptMessage(key, filename)
