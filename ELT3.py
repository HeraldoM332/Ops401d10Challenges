#!/usr/bin/env python3 

# Script Name:                  Event Logging Tool Part 3 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      03/14/24
# Purpose:                      Logging system events for response and/or analysis is a major part of security operations. 




import os
import logging
from logging import StreamHandler  # Import StreamHandler directly from logging
from logging.handlers import RotatingFileHandler
from scapy.all import *

# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set up console logging for debugging
console_handler = StreamHandler()  # Use StreamHandler for console output
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger('').addHandler(console_handler)

# Set up logging configuration with a rotating file handler
log_file_path = os.path.join(current_directory, 'port_scanner.log')

try:
    with open(log_file_path, 'w'):
        pass
except IOError:
    print(f"Error: Unable to write to {log_file_path}. Please check permissions.")
    exit(1)

# Use a RotatingFileHandler to rotate logs based on size
file_handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)  # Use FileHandler for writing to a file
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add both handlers to the root logger
logging.getLogger('').addHandler(file_handler)

# Explicitly set the root logger level to DEBUG
logging.getLogger('').setLevel(logging.DEBUG)

# Debugging statement to check if script reaches this point
logging.debug("Script setup completed")

# Check if the script is running with elevated privileges
if os.geteuid() != 0:
    logging.error("This script requires elevated privileges. Please run with sudo.")
    exit(1)

# Debugging statement to check if script reaches this point
logging.debug("Elevated privileges check passed")

# This is where you will define the target IP and your port range
target_ip = "192.168.1.1"  # Replace with your target IP, this IP is an example

# Prompt the user to input the port range
start_port = int(input("Enter the start port: "))
end_port = int(input("Enter the end port: "))

# Create a range of ports based on user input
port_range = range(start_port, end_port + 1)

# Loop through each port in the specified range
for port in port_range:
    logging.debug(f"Checking port: {port}")

    # Craft TCP SYN packet for each port using IP and TCP classes from scapy
    packet = IP(dst=target_ip)/TCP(dport=port, flags="S")

    logging.debug(f"Crafted packet for port: {port}")

    # Send crafted packet using sr1 and receive a response. Timeout parameter set to one second and verbose to 0 to suppress output
    try:
        response = sr1(packet, timeout=1, verbose=0)
        logging.debug(f"Response received for port {port}")
    except Exception as e:
        logging.debug(f"Exception: {e}")
        logging.exception("An exception occurred during script execution")

    # Check the response to determine the state of the port
    if response and response.haslayer(TCP):
        logging.debug(f"Response received for port {port}")
        # Check for SYN-ACK (0x12) flag using an if statement which then prints a message notifying the user the port is open.
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
        logging.debug(f"No response for port {port}")
        logging.info(f"Port {port} is closed (no response)")

logging.debug("Script execution completed")
# Done