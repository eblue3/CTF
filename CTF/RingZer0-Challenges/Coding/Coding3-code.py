# Challenge Link: https://ringzer0ctf.com/challenges/32
# Same Tree: /html/body/div[2]/div/div[2]/div/text()[2]
# => html > body > 2nd div > 1st div > 2nd div > 1st div > all text but only in 2nd line
# Cookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'} (Get when Inspect the site after logged in)

# You can copy your code from Challenge 1, it will be the same on the beginning.
from lxml import html
import requests
import hashlib
import binascii
import webbrowser

# My Cookie
mycookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'}

# Create Request to get the PageContent from the Challenge
r = requests.get('https://ringzer0ctf.com/challenges/14', cookies=mycookie)
tree = html.fromstring(r.content)

# Get the Binary Message inside the Parsed HTML we got above
message = tree.xpath('/html/body/div[2]/div/div[2]/div/text()[2]').pop().strip()
# Test it if we get the Message on Terminal
print ('Challenge Binary Message: ', message)

# Convert the Message into Ascii Representation
n = int(message, 2)
asciimess = binascii.unhexlify('%x' % n)
print ('Ascii Message: ',asciimess)

# Hashing the Binary Encoded we got
hashmess = hashlib.sha512(asciimess).hexdigest()
# Test it on Terminal
print ('Challenge Result: ', hashmess)

# Result URL
rURL = ('https://ringzer0ctf.com/challenges/14/' + hashmess)
# Print it to Terminal to Open it by Clicking
print('Click me: ',rURL)
# Or open browser to get the FLAG
webbrowser.open_new_tab(rURL)
