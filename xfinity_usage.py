#!/usr/bin/python
# xfinity_usage.py
# Script designed to get Comcast Xfinity X1 internet
# usage data into a JSON format for Home Assistant.
#
# Version 1.0
# Original Author : Rick Rocklin
# Original Date   : 10/02/2017
#
# 10/17/2017: Output to file
# 11/02/2017: Updated to use mechanicalsoup
import mechanicalsoup
import re
import json

# URL that we authenticate against
login_url = "https://auth.xfinity.com/oauth/login?state=https%3A%2F%2Fcustomer.xfinity.com%2F%23%2F%3FCMP%3DILC_signin_myxfinity_re"
# URL that we grab all the data from
stats_url = "https://www.xfinity.com/internet/mydatausage"
# Your xfinity user account (e.g. username@comcast.net) and password
xfinity_user = "taurencesalter@comcast.net"
xfinity_pass = "Su93r$@v0"
json_file = "/home/homeassistant/.homeassistant/xfinity_usage.json"

# Setup browser
browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13',
)

# Open the login URL
login_page = browser.get(login_url)

# Similar to assert login_page.ok but with full status code in case of failure.
login_page.raise_for_status()

# Find the form named sign-in
login_form = mechanicalsoup.Form(
    login_page.soup.select_one('form[name="sign-in"]'))

# Specify username and password
login_form.input({'username': xfinity_user, 'password': xfinity_pass})

# Submit the form
browser.submit(login_form, login_page.url)

# Read the stats URL
stats_page = browser.get(stats_url)

# Grab the script with the stats in it
stats = stats_page.soup.findAll(
    'script', string=re.compile('utag_data'))[0].string

# Split and RSplit on the first { and on the last } which is where the data object is located
jsonValue = '{%s}' % (stats.split('{', 1)[1].rsplit('}', 1)[0],)

# Load into json
data = json.loads(jsonValue)

# Print JSON to file
with open(json_file, 'w+') as outfile:
    json.dump(data, outfile, sort_keys=True)