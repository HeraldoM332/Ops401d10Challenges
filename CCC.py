#!/usr/bin/env python3
# Script Name:                  Cookie Capture Capades
# Author:                       Heraldo Morales
# Date of latest revision:      06/26/24
# Purpose:                      Capture a cookie and send it back out to the site in order to receive a valid response in HTTP text, all using Python’s Requests module.


import requests

# Function to capture and display cookies from the response
def capture_cookies(response):
    """Capture and display cookies from the response."""
    print("\033[94mCookies captured from the response:\033[0m")
    if response.cookies:
        for index, cookie in enumerate(response.cookies, 1):
            print(f"\033[92m{index}. Name: {cookie.name}, Value: {cookie.value}\033[0m")
    else:
        print("\033[91mNo cookies found in the response.\033[0m")

# Prompt the user for the URL
url = input("\033[95mEnter the URL: \033[0m")

# Check if the URL has a schema, if not, add 'http://' as default
if not url.startswith('http://') and not url.startswith('https://'):
    url = 'http://' + url

try:
    # Send an initial request to the site to capture the cookies
    response = requests.get(url)
except requests.exceptions.RequestException as e:
    print("\033[91mError occurred while making the request:", e, "\033[0m")
    exit()

# Display the captured cookies to the user
capture_cookies(response)

# Check if cookies were found before prompting for index selection
if response.cookies:
    # Prompt the user to select a cookie by index
    cookie_index = input("\033[95mEnter the index of the cookie you want to use: \033[0m")

    try:
        cookie_index = int(cookie_index)
    except ValueError:
        print("\033[91mInvalid input. Please enter a number.\033[0m")
        exit()

    if cookie_index < 1 or cookie_index > len(response.cookies):
        print("\033[91mInvalid index. Please enter a valid index.\033[0m")
        exit()

    # Extract the selected cookie from the response based on the index
    selected_cookie = list(response.cookies)[cookie_index - 1]

    # Now, send the selected cookie back to the site in a new request
    cookies = {selected_cookie.name: selected_cookie.value}  # Ensure passing the value as a string

    try:
        # Make a request to the site with the selected cookie
        response = requests.get(url, cookies=cookies)
    except requests.exceptions.RequestException as e:
        print("\033[91mError occurred while making the request:", e, "\033[0m")
        exit()

    # Print the response text
    print("\033[94mResponse Text:\033[0m")
    print(response.text)
else:
    print("\033[91mNo cookies found to select. Exiting.\033[0m")
