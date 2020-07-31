# Challenge Link: https://ringzer0ctf.com/challenges/159
# Same Tree: /html/body/div[2]/div/div[2]/div/text()[2]
# => html > body > 2nd div > 1st div > 2nd div > 1st div > all text but only in 2nd line
# Cookie = {'PHPSESSID':'<Your-Cookie>'} (Get when Inspect the site after logged in)

# You can copy your code from Challenge 1, 3, 4, 6 & 8 it will be the same on the beginning.
import requests
from lxml import html
import re
import webbrowser
import time
import json
from re import search

pm = "" # private message = hash
x = "" # consider it is the plain text
mycookie = {'PHPSESSID':'<Your-Cookie>'}

def TakeHash():
    while True:
        global x
        global pm
        # My Cookie
        global mycookie
        APIkey = '<YOUR hashes.org APIKEY>'
        # Create Request to get the PageContent from the Challenge
        r = requests.get('https://ringzer0ctf.com/challenges/159', cookies=mycookie)
        tree = html.fromstring(r.content)
        # Get the message inside the Parsed HTML we got above
        msg = tree.xpath('/html/body/div[2]/div/div[2]/div/text()[2]').pop().strip()
        pm = msg
        # Test it if we get the message on Terminal
        print ('Challenge message: ', msg)
        URL = 'https://hashes.org/api.php?key=' + APIkey + '&query=' + msg
        r = requests.get(URL)
        data = r.json()
        x = str(data['result'][msg])
        #print ('Result:',data)
        if x == "None":
            print ('Result:',data['result'][msg])
            time.sleep(3) # Wait 3 seconds since Hashes.org won't allow you request more than 20r/min
        else:
            x = str(data['result'][msg]['plain'])
            break

TakeHash()
print (pm,' = ',x)
# Result URL
rURL = ('https://ringzer0ctf.com/challenges/159/' + x)
# Print it to Terminal to Open it by Clicking
#print('Click me: ',rURL)
# Get FLAG:
rlink = requests.get(rURL, cookies=mycookie)
flag=search("FLAG-.{26}",rlink.text).group() # I modify this to 26 after I know the FLAG is contains 26 chars after FLAG- . First time trying just set it to 50 or bigger :)
print(flag)
# Or open browser to get the FLAG
#webbrowser.open_new_tab(rURL)
