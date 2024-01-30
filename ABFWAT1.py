#!/usr/bin/env python3 

# Script Name:                  Automated Brute Force Wordlist Attack Tool Part 1 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      01/29/24
# Purpose:                      Develop a custom tool that performs brute force attacks to better understand the types of automation employed by adversaries.


# Imports time module for handling operations that deal with time and ssl module for SSL/TLS support
import time
import ssl

# This portion attempts to handle a specific error related to SSL by setting up SSL context. Manages the SSL certifcate verifcation proccess. If attribute error occurs its caught and no action is take, otherwise sets up unverified SSL context
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Defines function iterator() prompts user for dictionary file path
# Opens specified file using open() function with specified encoding
# Reads each line from file removes trail whitespaces and assigns line to variable word
    # Prints word to screen and introduces delay of 1 second using time.sleep(1)
    # Repeats Procces all lines in file are processed        
def iterator():
    filepath = input("Enter your dictionary filepath:\n")
    file = open(filepath, encoding="ISO-8859-1")
    line = file.readline()
    while line:
        line = line.rstrip()
        word = line
        print(word)
        time.sleep(1)
        line = file.readline()
        # Closes file after reading
    file.close()

# Defines function named check_for_word() takes a list of words as input
    # Prompts user to enter a word
    # Checks if entered word is in provided list and prints corresponding message
def check_for_word(words):
    user_answer = input("Enter a word: ")
    if user_answer in words:
        print("The word is in the dictionary")
    else:
        print("The word is not in the dictionary")

# Defines function named load_extrernal_file() reads contents of file.
        # Intiializes empty list named password_list
        # Opens specified file in read mode using open()
        # Reads each line from file, removes trail whitespaces, appends to password_list and prints list
        # Continues reading until end of file is reached
def load_external_file():
    password_list = []
    with open('rockyou.txt', 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.rstrip()
            password_list.append(line)
            print(password_list)

# Main Section
            # Script uses if __name__ == "__main__": to construct to check if script is being run direcctly
            # Continuous loop, presents a menu to user with 3 options. 
if __name__ == "__main__":
    while True:
        mode = input("""
Brute Force Wordlist Attack Tool Menu
1 - Offensive, Dictionary Iterator
2 - Defensive, Password Recognized
3 - Exit
Please enter a number: 
""")
        if mode == "1":       # Calls iterator function for offensive mode
            iterator()
        elif mode == "2":     # Calls the load_external_file() function to get a list of words and call checck_for_word() for defensive mode
            word_list = load_external_file()
            check_for_word(word_list)
        elif mode == '3':   # Breaks out of loops to exit program
            break
        else:               # Invalid option, prints invalid selection
            print("Invalid selection...")


# Done