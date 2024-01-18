#!/usr/bin/env python3 
# Script Name:                  File Encryption Part 2
# Author:                       Heraldo Morales
# Date of latest revision:      01/18/24
# Purpose:                      Script that encrypts a single file (cont...)

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


# Encript file function encypts a file, reads file content, encrypts using Genet and writes encryptedd data to new file, .encrypted appended to og fn
def encrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename + ".encrypted", "wb") as file:
        file.write(encrypted_data)

# Prints Success Message        
    print("File encrypted successfully.")

# Decrypt file, function decrypts file. Read encrypted file content, decrypts with Fernet and writes decrypted data to new file with .decrypted appended.
def decrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename + ".decrypted", "wb") as file:
        file.write(decrypted_data)
# Prints sucess message        
    print("File decrypted successfully.")

# encrypt_string function, encrypts string. Converts strings to bytes, encrypts with Fernet and encrypted message.
def encrypt_string(plaintext, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(plaintext.encode())
    print("Encrypted Message:", encrypted_data.decode())

# decrypt_string function decrypts string. converts the encrypted message to bytes, decrypts with Fernet and prints message
def decrypt_string(encrypted_message, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_message.encode())
    print("Decrypted Message:", decrypted_data.decode())

# Encrypt_folder function recursively encrypts folder and contents, calling on OS.walk to navigate the folder structure and calls
def encrypt_folder(root_folder, key):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
# Encrypt_file for each file encountered            
            encrypt_file(file_path, key)

# Decrypt_folder function recursively decrypts folder, encrypted by this tool. Calls on os.walk to navigate the folder structures and calls decrypt_file for each file encountered
def decrypt_folder(root_folder, key):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)


# Main Function
# Takes user input asking to select a mode as well as loading encryption key while also using and if loop for the commands            
def main():
    mode = int(input("Select a mode: 1 - Encrypt File, 2 - Decrypt File, 3 - Encrypt Message, 4 - Decrypt Message: "))
    key = load_key()

    if mode == 1 or mode == 2:
        filename = input("Enter the filepath or folder path: ")
        if os.path.isfile(filename):  # Check if it's a file
            if mode == 1:
                encrypt_file(filename, key)
            elif mode == 2:
                decrypt_file(filename, key)
        elif os.path.isdir(filename):  # Check if it's a directory
            if mode == 1:
                encrypt_folder(filename, key)
            elif mode == 2:
                decrypt_folder(filename, key)
        else:
            print("Invalid file or folder path.")

    elif mode == 3 or mode == 4:
        message = input("Enter the cleartext string: ")
        if mode == 3:
            encrypt_string(message, key)
        elif mode == 4:
            decrypt_string(message, key)

    else:
        print("Invalid mode selected.")

if __name__ == "__main__":
    main()


# Done