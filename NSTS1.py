#!/usr/bin/env python3 

# Script Name:                  Network Security Tool with Scapy Part 1 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      01/23/24
# Purpose:                      Create your own network scanning tool with the Python library Scapy

# Imports OS and scapy Librar
import os
from scapy.all import *

# Check if the script is running with elevated privileges
if os.geteuid() != 0:
    print("Error: This script requires elevated privileges. Please run with sudo.")
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
    # Craft TCP SYN packet for each porting using IP and TCP classes from scapy
    packet = IP(dst=target_ip)/TCP(dport=port, flags="S")

    # Send crafted packet using sr1 and receive a response. Timeout parameter set to one second and verbose to 0 to suppress output
    response = sr1(packet, timeout=1, verbose=0)

    # Check the response to determine the state of the port
    if response and response.haslayer(TCP):
        # Check for SYN-ACK (0x12) flag using an if statement which then prints message notifying user port is open. 
        if response[TCP].flags == 18:
            print(f"Port {port} is open")
            
            # Craft and send RST packet to gracefully close the connection
            rst_packet = IP(dst=target_ip)/TCP(dport=port, flags="R")
            send(rst_packet, verbose=0)
        # Check for RST (0x14) flag, which then prints a message port is closed
        elif response[TCP].flags == 20:
            print(f"Port {port} is closed")
        # If no flags are recieved prints message which notifies user that port is filtered and packet is silently dropped    
        else:
            print(f"Port {port} is filtered and silently dropped")
    # No reponse = Print Message notifying user that port is closed.        
    else:
        print(f"Port {port} is closed (no response)")



# Done
        
