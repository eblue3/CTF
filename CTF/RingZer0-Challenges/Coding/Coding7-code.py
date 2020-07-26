# Challenge Link: https://ringzer0ctf.com/challenges/15
# Same Tree: /html/body/div[2]/div/div[2]/div/text()[2]
# => html > body > 2nd div > 1st div > 2nd div > 1st div > all text but only in 2nd line
# Cookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'} (Get when Inspect the site after logged in)

# You can copy your code from Challenge 1, 3 & 4, it will be the same on the beginning.
import requests
from lxml import html
import hashlib
import webbrowser
import base64

# My Cookie
mycookie = {'PHPSESSID':'do4ggv5iunp51pfcmsrn38idq3'}

# Create Request to get the PageContent from the Challenge
r = requests.get('https://ringzer0ctf.com/challenges/15', cookies=mycookie)
tree = html.fromstring(r.content)

# Get the message inside the Parsed HTML we got above
message = tree.xpath('/html/body/div[2]/div/div[2]/div[1]/text()[2]').pop().strip()
#print ('Message:', message)

# Get the Checksum:
checksum = tree.xpath('/html/body/div[2]/div/div[2]/div[2]/text()[2]').pop().strip()
# Print to test the Checksum later
print ('Checksum: ', checksum)

data  = base64.b64decode(message)
#print ('Data:', data)
data = data[::-1]
#print ('Data:', data)
_data = hashlib.md5(data).hexdigest()
print ('Data:', _data)

if _data == checksum:
    result = (data[1510:1514]).decode('iso-8859-2')+(data[1518:1520]).decode('iso-8859-2')
    print("Secret Word:",result)

    # Result URL
    rURL = ('https://ringzer0ctf.com/challenges/15/' + result)
    # Print it to Terminal to Open it by Clicking
    print('Click me: ',rURL)
    # Or open browser to get the FLAG
    webbrowser.open_new_tab(rURL)