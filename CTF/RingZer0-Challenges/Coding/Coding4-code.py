# Challenge Link: https://ringzer0ctf.com/challenges/32
# Same Tree: /html/body/div[2]/div/div[2]/div/text()[2]
# => html > body > 2nd div > 1st div > 2nd div > 1st div > all text but only in 2nd line
# Cookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'} (Get when Inspect the site after logged in)

# You can copy your code from Challenge 3 & 1, it will be the same on the beginning.
from lxml import html
import requests
import re
import webbrowser

# My Cookie
mycookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'}

# Create Request to get the PageContent from the Challenge
r = requests.get('https://ringzer0ctf.com/challenges/32', cookies=mycookie)
tree = html.fromstring(r.content)

# Get the message inside the Parsed HTML we got above
message = tree.xpath('/html/body/div[2]/div/div[2]/div/text()[2]').pop().strip()
# Test it if we get the message on Terminal
print ('Challenge message: ', message)

# Get x, y, z from the message
# Link to learn: https://www.w3schools.com/python/python_regex.asp
x = re.search(r"\A[0-9]\w+", message)
y = re.search(r"\b0x\w+", message)
z = re.search(r"\b1\w+", message)
# After many tests, the pattern of the Equation is: Int + Hexadecimal + Binary
# But you need all Parameters is the same Integer type => Convert it & Calculate it
equation = (int(x.group()) + int(y.group(),0) - int(z.group(),2))
print (equation)

# I believe we have the answer, but to attach to rURL variable, it must be string. So ...
equation = str(equation)

# Result URL
rURL = ('https://ringzer0ctf.com/challenges/32/' + equation)
# Print it to Terminal to Open it by Clicking
print('Click me: ',rURL)
# Or open browser to get the FLAG
webbrowser.open_new_tab(rURL)
