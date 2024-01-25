#!/usr/bin/env python3 

# Script Name:                  Network Security Tool with Scapy Part 3 of 3
# Author:                       Heraldo Morales
# Date of latest revision:      01/24/24
# Purpose:                      Create your own network scanning tool with the Python library Scapy




# Imports OS module and scapy Library
import os
from scapy.all import *

# The main function that is overall in charge of network scanning based on user input
def network_scanner():
    target = input("Enter the target (IP address or CIDR format): ")

    # Check if the target is an IP address or a CIDR format
    if '/' in target:
        perform_icmp_ping_sweep(target)
    else:
        target_ip = target  # If the target is an IP address, assign it directly
        perform_tcp_port_scan(target_ip)

# Function that performs ICMP ping sweep on a given network address. Single IP or CIDR format
def perform_icmp_ping_sweep(network_address):
    network, _, subnet_mask = network_address.partition('/')
    ip_addresses = [str(ip) for ip in IPNetwork(network_address) if ip != IPNetwork(network_address).network and ip != IPNetwork(network_address).broadcast]

    online_hosts = 0

    for ip in ip_addresses:
        packet = IP(dst=ip) / ICMP()
        response = sr1(packet, timeout=1, verbose=0)

        if not response:
            print(f"Host {ip} is down or unresponsive.")
        elif response.haslayer(ICMP) and response[ICMP].type == 3 and response[ICMP].code in [1, 2, 3, 9, 10, 13]:
            print(f"Host {ip} is actively blocking ICMP traffic.")
        else:
            print(f"Host {ip} is responding.")
            online_hosts += 1

            # Call the port scan function for responsive hosts
            perform_tcp_port_scan(ip)

    print(f"\nNumber of online hosts: {online_hosts}")

# Function that performs TCP port scanning on target IP address
def perform_tcp_port_scan(target_ip):
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    port_range = range(start_port, end_port + 1)

    for port in port_range:
        packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
        response = sr1(packet, timeout=1, verbose=0)

        if response and response.haslayer(TCP):
            if response[TCP].flags == 18:
                print(f"Port {port} is open")
                rst_packet = IP(dst=target_ip) / TCP(dport=port, flags="R")
                send(rst_packet, verbose=0)
            elif response[TCP].flags == 20:
                print(f"Port {port} is closed")
            else:
                print(f"Port {port} is filtered and silently dropped")
        else:
            print(f"Port {port} is closed (no response)")

# Main Execution. Ensure that script runs. Uses a while loop where it calls network scanner to perform based on user input until user says no
if __name__ == "__main__":
    while True:
        network_scanner()
        continue_scan = input("Do you want to scan another target? (yes/no): ")
        if continue_scan.lower() != 'yes':
            break


# Done