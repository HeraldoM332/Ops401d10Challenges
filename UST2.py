#!/usr/bin/env python3

# Script Name:                  Uptime Sensor Tool Part 2 of 2
# Author:                       Heraldo Morales
# Date of latest revision:      05/20/24
# Purpose:                      An uptime sensor tool that uses ICMP packets to evaluate if hosts on the LAN are up or down, and sends email notifications on status changes.





import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
from ping3 import ping
import traceback

def send_notification(from_email, from_password, to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, from_password)
            server.send_message(msg)

        print("Email notification sent successfully.")
    except Exception as e:
        print("Failed to send email notification:")
        traceback.print_exc()

def uptime_sensor(ip_address, to_email, from_email, from_password):
    last_status = None
    while True:
        response = ping(ip_address)
        current_status = "up" if response else "down"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if last_status is None:
            last_status = current_status
        elif current_status != last_status:
            subject = f"Host Status Change for {ip_address}"
            body = f"Timestamp: {timestamp}\nHost: {ip_address}\nPrevious Status: {last_status}\nCurrent Status: {current_status}"
            send_notification(from_email, from_password, to_email, subject, body)
            last_status = current_status

        print(f"{timestamp} - {ip_address} is {current_status}")
        time.sleep(2)

if __name__ == "__main__":
    ip_to_test = "8.8.8.8"  # Example IP address, replace with your target IP
    to_email = input("Enter the email address to send notifications to: ")
    from_email = input("Enter the email address to send notifications from: ")
    from_password = input("Enter the app password for two-step verification: ")

    uptime_sensor(ip_to_test, to_email, from_email, from_password)




