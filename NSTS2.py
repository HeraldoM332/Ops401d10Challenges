#!/usr/bin/env python3 

# Script Name:                  Network Security Tool with Scapy Part 2 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      01/24/24
# Purpose:                      Create your own network scanning tool with the Python library Scapy



# Imports OS and Scapy Library
import os
from scapy.all import *

# Check if the script is running with elevated privileges. Exits if not
if os.geteuid() != 0:
    print("Error: This script requires elevated privileges. Please run with sudo.")
    exit(1)

# Function to perform TCP port scanning. Prompts user for targer IP address and port range, then scans ports to determine if open,closed or filtered.
def tcp_port_scanner():
    target_ip = input("Enter the target IP: ")

    # Prompt the user to input the port range
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    # Create a range of ports based on user input
    port_range = range(start_port, end_port + 1)
    # Loop through each port in the specified range
    for port in port_range:
        # Craft TCP SYN packet for each port using IP and TCP classes from scapy
        packet = IP(dst=target_ip) / TCP(dport=port, flags="S")

        # Send crafted packet using sr1 and receive a response. Timeout parameter set to one second and verbose to 0 to suppress output
        response = sr1(packet, timeout=1, verbose=0)

        # Check the response to determine the state of the port
        if response and response.haslayer(TCP):
            # Check for SYN-ACK (0x12) flag using an if statement which then prints message notifying user port is open.
            if response[TCP].flags == 18:
                print(f"Port {port} is open")

                # Craft and send RST packet to gracefully close the connection
                rst_packet = IP(dst=target_ip) / TCP(dport=port, flags="R")
                send(rst_packet, verbose=0)
            # Check for RST (0x14) flag, which then prints a message port is closed
            elif response[TCP].flags == 20:
                print(f"Port {port} is closed")
            # If no flags are received prints message which notifies user that port is filtered and packet is silently dropped
            else:
                print(f"Port {port} is filtered and silently dropped")
        # No response = Print Message notifying the user that the port is closed.
        else:
            print(f"Port {port} is closed (no response)")


# Defines function icmp_ping_swweep() performs ICMP ping sweep. prompts user for a network address in CIDR format
def icmp_ping_sweep():
    network_address = input("Enter the network address (CIDR format, e.g., '10.10.0.0/24'): ")
    
    # Extracting the network address and subnet mask
    network, _, subnet_mask = network_address.partition('/')
    
    # Generate a list of all addresses in the given network
    ip_addresses = [str(ip) for ip in IPNetwork(network_address) if ip != IPNetwork(network_address).network and ip != IPNetwork(network_address).broadcast]

    online_hosts = 0

# ICMP Ping Sweep Function
    for ip in ip_addresses:
        # Craft ICMP Echo Request packet for each IP address using IP and ICMP classes from scapy
        packet = IP(dst=ip) / ICMP()

        # Send crafted packet using sr1 and receive a response. Timeout parameter set to one second and verbose to 0 to suppress output
        response = sr1(packet, timeout=1, verbose=0)

        if not response:
            print(f"Host {ip} is down or unresponsive.")
        elif response.haslayer(ICMP) and response[ICMP].type == 3 and response[ICMP].code in [1, 2, 3, 9, 10, 13]:
            print(f"Host {ip} is actively blocking ICMP traffic.")
        else:
            print(f"Host {ip} is responding.")
            online_hosts += 1

    print(f"\nNumber of online hosts: {online_hosts}")
# Defines function main. Displays main menu to user and takes choices between TCP port range scanner and ICMP ping sweep mode
def main():
    print("Network Security Tool Menu:")
    print("1. TCP Port Range Scanner Mode")
    print("2. ICMP Ping Sweep Mode")

    choice = input("Enter your choice (1 or 2): ")
# Main function implementations. Insidoe main it checks Users choice and calls corresponding function. 
    if choice == "1":
        tcp_port_scanner()
    elif choice == "2":
        icmp_ping_sweep()
    else:
        print("Invalid choice. Please enter either 1 or 2.")
# Main exectution block
if __name__ == "__main__":
    main()


# Done    
