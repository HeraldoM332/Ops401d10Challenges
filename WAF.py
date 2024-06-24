#!/usr/bin/env python3 

# Script Name:                  Web Application Finger Printing
# Author:                       Heraldo Morales
# Date of latest revision:      06/15/24
# Purpose:                      A Python script that utilizes multiple banner grabbing approaches against a single target.


import subprocess
import telnetlib
import shutil

# Colors for better readability
class bcolors:
    HEADER = '\033[96m'  # Cyan
    OKBLUE = '\033[94m'  # Blue
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'  # Red
    ENDC = '\033[0m'  # Reset to default color
    BOLD = '\033[1m'  # Bold
    UNDERLINE = '\033[4m'  # Underline

# Function to perform banner grabbing using Netcat
def netcat_banner_grabbing(target, port):
    if shutil.which("nc") is None:
        print(f"{bcolors.FAIL}Netcat is not installed or not found in PATH.{bcolors.ENDC}")
        return
    try:
        print(f"{bcolors.HEADER}Performing Netcat banner grab...{bcolors.ENDC}")
        nc_command = f'echo | nc -v {target} {port}'
        result = subprocess.run(nc_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"{bcolors.OKBLUE}Netcat Result:{bcolors.ENDC}\n{result.stdout or result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"{bcolors.FAIL}An error occurred while trying to run Netcat:{bcolors.ENDC}")
        print(e.stderr)

# Function to perform banner grabbing using Telnet
def telnet_banner_grabbing(target, port):
    try:
        print(f"{bcolors.HEADER}Performing Telnet banner grab...{bcolors.ENDC}")
        with telnetlib.Telnet(target, port) as tn:
            tn.write(b'\n')
            output = tn.read_until(b'\n', timeout=5).decode('utf-8')
            print(f"{bcolors.OKBLUE}Telnet Result:{bcolors.ENDC}\n{output}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred while trying to run Telnet:{bcolors.ENDC}")
        print(e)

# Function to perform banner grabbing using Nmap
def nmap_banner_grabbing(target, port):
    if shutil.which("nmap") is None:
        print(f"{bcolors.FAIL}Nmap is not installed or not found in PATH.{bcolors.ENDC}")
        return
    try:
        print(f"{bcolors.HEADER}Performing Nmap banner grab...{bcolors.ENDC}")
        nmap_command = ['nmap', '-sV', '-p', str(port), '-Pn', target]
        result = subprocess.run(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"{bcolors.OKGREEN}Nmap Result:{bcolors.ENDC}\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"{bcolors.FAIL}An error occurred while trying to run Nmap:{bcolors.ENDC}")
        print(e.stderr)

def main():
    # Prompt user for input
    target = input("Please enter the URL or IP address: ")
    port = input("Please enter the port number: ")

    # Perform banner grabbing using Netcat
    netcat_banner_grabbing(target, port)
    
    # Perform banner grabbing using Telnet
    telnet_banner_grabbing(target, port)
    
    # Perform banner grabbing using Nmap
    nmap_banner_grabbing(target, port)

if __name__ == "__main__":
    main()

# Done
