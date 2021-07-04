# In order to complete this challenge you must be able to two things:
#
#  1. You need to be able to hash the Message and reply quickly, which implies
#     using some sort of program (Python in our case) to make this possible.
#
#  2. You must be able to see the Message which means you have to be logged in.
#
# To acomplish the first task, we can write a small python script as we've
# done here that can scrape the page, hash the Message, and reply quickly, but
# the problem is that without logging into the site we can't see the Message,
# so we must first be able to be logged in.
#
# Using BurpSuite, we can proxy all the traffic from our browser to the
# ringzer0team.com server. After logging into the site we an interesting
# cookie called "PHPSESSID", this is a PHP session cookie used for tracking a
# user's session including if a user is logged in or not.
#
# Knowing that the PHPSESSID cookie is used to tell if a user is logged in  we
# can now submit that cookie with our Python script request to make the server
# believe that the script is  acting as the logged in user. This let's us
# access the page.
#
# With this two task completed the python script is trivial:

from lxml import html
import requests
import hashlib
import webbrowser

# Grab my PHPSESSID cookie so I can access the page. Otherwise it would tell
# me that I need to login to see the challenge. :D
cookie = {'PHPSESSID':'uhdod6kult7quke8u9smfj31u2'}

# Grab the page content and parse it into a dom tree.
page = requests.get('https://ringzer0team.com/challenges/13', cookies=cookie)
tree = html.fromstring(page.content)

# Grab the Message in question.
message = tree.xpath('/html/body/div[2]/div/div[2]/div/text()[2]').pop().strip()

print ('Message: ', message)

# Encode the Message
message=message.encode('utf-8')

# Hash Message into SHA512
hashedMessage = hashlib.sha512(message).hexdigest()

print ('Hashed: ', hashedMessage)

answerUrl = 'https://ringzer0team.com/challenges/13/' + hashedMessage
print (answerUrl)

# Open Web Browser with Answer URL
webbrowser.open_new_tab(answerUrl)
