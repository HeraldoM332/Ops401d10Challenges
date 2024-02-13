#!/usr/bin/env python3 

# Script Name:                  Event Logging Tool Part 1 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      02/13/24
# Purpose:                      Logging system events for response and/or analysis is a major part of security operations. 



# Imports OS, Scapy and Logging library
import os
from scapy.all import *
import logging

# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set up logging configuration with a relative path
log_file_path = os.path.join(current_directory, 'port_scanner.log')

try:
    with open(log_file_path, 'w'):
        pass
except IOError:
    print(f"Error: Unable to write to {log_file_path}. Please check permissions.")
    exit(1)

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the script is running with elevated privileges
if os.geteuid() != 0:
    logging.error("This script requires elevated privileges. Please run with sudo.")
    exit(1)

# This is where you will define target IP and your port range
target_ip = "192.168.1.1"  # Replace with your target IP, this IP is an example

# Prompt the user to input the port range
start_port = int(input("Enter the start port: "))
end_port = int(input("Enter the end port: "))

# Create a range of ports based on user input
port_range = range(start_port, end_port + 1)

# Loop through each port in the specified range
for port in port_range:
    # Craft TCP SYN packet for each port using IP and TCP classes from scapy
    packet = IP(dst=target_ip)/TCP(dport=port, flags="S")

    # Send crafted packet using sr1 and receive a response. Timeout parameter set to one second and verbose to 0 to suppress output
    response = sr1(packet, timeout=1, verbose=0)

    # Check the response to determine the state of the port
    if response and response.haslayer(TCP):
        # Check for SYN-ACK (0x12) flag using an if statement which then prints message notifying the user port is open. 
        if response[TCP].flags == 18:
            logging.info(f"Port {port} is open")
            
            # Craft and send RST packet to gracefully close the connection
            rst_packet = IP(dst=target_ip)/TCP(dport=port, flags="R")
            send(rst_packet, verbose=0)
        # Check for RST (0x14) flag, which then prints a message port is closed
        elif response[TCP].flags == 20:
            logging.info(f"Port {port} is closed")
        # If no flags are received, print a message which notifies the user that the port is filtered and the packet is silently dropped    
        else:
            logging.info(f"Port {port} is filtered and silently dropped")
    # No response = Print Message notifying the user that the port is closed.        
    else:
        logging.info(f"Port {port} is closed (no response)")

# Done