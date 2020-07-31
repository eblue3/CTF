# Challenge Link: https://ringzer0ctf.com/challenges/121
# Same Tree: /html/body/div[2]/div/div[2]/div/text()[2]
# => html > body > 2nd div > 1st div > 2nd div > 1st div > all text but only in 2nd line
# Cookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'} (Get when Inspect the site after logged in)

# You can copy your code from Challenge 1, 3, 4, 6 & 8 it will be the same on the beginning.
import requests
from lxml import html
import re
import webbrowser

# My Cookie
mycookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'}

# Create Request to get the PageContent from the Challenge
r = requests.get('https://ringzer0ctf.com/challenges/121', cookies=mycookie)
tree = html.fromstring(r.content)

# Get the message inside the Parsed HTML we got above
msg = tree.xpath('/html/body/div[2]/div/div[2]/div/text()[2]').pop().strip()
# Test it if we get the message on Terminal
print ('Challenge message: ', msg)

#check = msg.replace('\\x', '')
#print ('check = ', check)
#checkk = check.decode('hex')
#print ('check 2 = ', checkk)
# Get the "bindump" of the shellcode
sc = msg.replace('\\x', '').decode('hex')
#print ('sc = ', sc)
#hxcheck = sc.encode('hex')
#print ('check 3 = ', hxcheck)

# [0x54:0x54+0x0c] => Check Writeups about Assembly Reverse Engineer
hx = sc[0x54:0x54+0x0c].encode('hex')


#print ('hx = ', hx)
result = ''.join(chr(int(x,16) ^ 0xff) for x in re.findall('..', hx))
#print ('Result = ', result)

# Result URL
rURL = ('https://ringzer0ctf.com/challenges/121/' + result)
# Print it to Terminal to Open it by Clicking
print('Click me: ',rURL)
# Or open browser to get the FLAG
webbrowser.open_new_tab(rURL)
