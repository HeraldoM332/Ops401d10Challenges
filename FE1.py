#!/usr/bin/env python3 
# Script Name:                  File Encryption Part 1
# Author:                       Heraldo Morales
# Date of latest revision:      01/16/24
# Purpose:                      Script that encrypts a single file


# Imports Fernet from cryptography.fernet and it imports OS for handling file operations and checking file existence.
from cryptography.fernet import Fernet
import os


# Attempts to open key.key file and read content, if the file is not found, generates a new key and saves to file. Returns loaded or newly generated Key
def load_key():
    try:
        return open("key.key", "rb").read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key


# Takes filename and a key as parameters, initialzes Fernet object with provided key. Read entire content of file into file_data, encrpyts the file data using f.encrypt, writes encrypted data to new file with .encrypted extension. 
def encrypt_file(filename, key):
    f = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename + ".encrypted", "wb") as file:
        file.write(encrypted_data)

# Prints Success Message
    print("File encrypted successfully.")


# Takes filename & Key as parameters. initializes fernet with provided key, reads encrypted content into encrypted_data
def decrypt_file(filename, key):
    f = Fernet(key)

    with open(filename, "rb") as file:
        encrypted_data = file.read()

# Decrypts file using f.decrypt(encrypted_data) writes, decrypted data to a new file with a .decrypted extension
    decrypted_data = f.decrypt(encrypted_data)

    with open(filename + ".decrypted", "wb") as file:
        file.write(decrypted_data)

# Prints Success Message
    print("File decrypted successfully.")

# Takes a cleartext string and Key as parameters, initializes fernet object with provided key, encrypts the string using f.encrypt(plaintext.edncode())
def encrypt_string(plaintext, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(plaintext.encode())

# Prints encrypted Message    
    print("Encrypted Message:", encrypted_data.decode())

# Takes encrypted message and key as parameters. Initializes a Fernet object with provided Key, Decrypts message using f.decrypt(encrypted_message.encdoe())
def decrypt_string(encrypted_message, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_message.encode())
# Prints the decrypted message    
    print("Decrypted Message:", decrypted_data.decode())

# Prompts User to Select Mode, Loads key using load_key function, based on selected mode, prompts for filepath or cleartext string.
def main():
    mode = int(input("Select a mode: 1 - Encrypt File, 2 - Decrypt File, 3 - Encrypt Message, 4 - Decrypt Message: "))
    key = load_key()

# If loop calls appropriate function, while handling invalid mode selections
    if mode == 1 or mode == 2:
        filename = input("Enter the filepath: ")
        if mode == 1:
            encrypt_file(filename, key)
        elif mode == 2:
            decrypt_file(filename, key)

    elif mode == 3 or mode == 4:
        message = input("Enter the cleartext string: ")
        if mode == 3:
            encrypt_string(message, key)
        elif mode == 4:
            decrypt_string(message, key)

    else:
        print("Invalid mode selected.")

# Ensures that main function is called only when script is executed directly (not imported as module)
if __name__ == "__main__":
    main()

    

# Done
