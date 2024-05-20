#!/usr/bin/env python3 

# Script Name:                  Uptime Sensor Tool Part 1 of 2
# Author:                       Heraldo Morales
# Date of latest revision:      05/20/24
# Purpose:                      An uptime sensor tool that uses ICMP packets to evaluate if hosts on the LAN are up or down.



# Imports Necessary Modules 
import time
from ping3 import ping
from datetime import datetime

# Defines uptime sensor function 
def uptime_sensor(ip_address):   # Takes ip address as an argument 
    while True:     # While true loop that keeps sensor running continuously 
        response = ping(ip_address)   # sends a single ICMP ping to the specified IP address.
        status = "Network Active" if response else "Network Inactive"  # Evaluates response
        timestamp = datetime.now()   # General timestamp
        print(f"{timestamp} {status} to {ip_address}")  # Prints status
        time.sleep(2)  # Pause Execution

# Main function 
# If loop checks if script runs directly
if __name__ == "__main__":
    ip_to_test = "8.8.8.8"  # Example IP address, replace with your target IP
    uptime_sensor(ip_to_test)  # Calls function


# Done    