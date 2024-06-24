#!/usr/bin/env python3 

# Script Name:                  Signature-based Malware Detection Part 2 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      06/24/24
# Purpose:                      Development of your own basic antivirus tool in Python.



import os
import hashlib
import platform
import time


# Computes the MD5 Hash of a file specfied by file path
def generate_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except IOError as e:
        print(f"Could not read file {file_path}: {e}")
        return None
    return hash_md5.hexdigest()

# Scans each file and folder in directory, generating MD5 hashes for files and printing detailed information about each file.
def search_files(directory):
    matches = []
    files_searched = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            files_searched += 1
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            md5_hash = generate_md5(file_path)

            if md5_hash:
                print(f"MD5: {md5_hash} | Time: {timestamp} | File: {file} | Size: {file_size} bytes | Path: {file_path}")
                matches.append(file_path)

    return matches, files_searched

# Main entry point of script prompting user for input and orchestrating file search process
def main():
    filename = input("Enter the file name to search for: ")
    directory = input("Enter the directory to search in: ")

    if platform.system() == 'Windows':
        directory = directory.replace('/', '\\')
    else:
        directory = directory.replace('\\', '/')

    matches, files_searched = search_files(directory)

    print(f"Total files searched: {files_searched}")
    print(f"Total matches found: {len(matches)}")

# Ensures that main function is executed only when script is run directly
if __name__ == "__main__":
    main()


# Done