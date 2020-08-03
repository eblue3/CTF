# Challenge Link: https://ringzer0ctf.com/challenges/57
# Same Tree: /html/body/div[2]/div/div[2]/div/text()[2]
# => html > body > 2nd div > 1st div > 2nd div > 1st div > all text but only in 2nd line
# Cookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'} (Get when Inspect the site after logged in)

# You can copy your code from Challenge 1, 3, 4 & 6 it will be the same on the beginning.
import requests
from lxml import html
import hashlib
import webbrowser

# My Cookie
mycookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'}

# Create Request to get the PageContent from the Challenge
r = requests.get('https://ringzer0ctf.com/challenges/57', cookies=mycookie)
tree = html.fromstring(r.content)

# Get the message inside the Parsed HTML we got above
message = tree.xpath('/html/body/div[2]/div/div[2]/div[1]/text()[2]').pop().strip()
saltyy = tree.xpath('/html/body/div[2]/div/div[2]/div[2]/text()[2]').pop().strip()
# Test it if we get the message on Terminal
print ('Challenge message: ', message)
print ('Length of Message: ', len(message))
print ('Salt Added: ', saltyy)

# It has 40 characters, and maybe is a hash => 160 bits => It maybe is SHA1 / HAS-160 / RIPEMD-160
# As the previous Hash Breaker, we have answer inside 0-9999 => So We try Pass+Saltyy first, If failed, try Saltyy+Pass
# => We write a function to hash it from 0000 to 9999. If it's a match with $message => we try to Submit it. Otherwise I will try the others two
for i in range(0,10000):
    x = str(i)
    if message == (hashlib.sha1(x + saltyy).hexdigest()):
        break

# => Tried Pass+Saltyy and it's right :)

# Result URL
rURL = ('https://ringzer0ctf.com/challenges/57/' + x)
# Print it to Terminal to Open it by Clicking
print('Click me: ',rURL)
# Or open browser to get the FLAG
webbrowser.open_new_tab(rURL)
