# http://ringzer0ctf.com/challenges/119

import requests
import re

# List of each number with its ascii art
zero = '&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxx&nbsp;<br />'
one = '&nbsp;xx&nbsp;&nbsp;<br />x&nbsp;x&nbsp;&nbsp;<br />&nbsp;&nbsp;x&nbsp;&nbsp;<br />&nbsp;&nbsp;x&nbsp;&nbsp;<br />xxxxx<br />'
two = '&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x&nbsp;<br />&nbsp;&nbsp;xx&nbsp;<br />&nbsp;x&nbsp;&nbsp;&nbsp;<br />xxxxx<br />'
three = '&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;&nbsp;xx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxx&nbsp;<br />'
four = '&nbsp;x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxxxx<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x<br />&nbsp;&nbsp;&nbsp;&nbsp;x<br />'
five = 'xxxxx<br />x&nbsp;&nbsp;&nbsp;&nbsp;<br />&nbsp;xxxx<br />&nbsp;&nbsp;&nbsp;&nbsp;x<br />xxxxx<br />'

number_art = [zero, one, two, three, four, five]
# print number_art

# Authorization by 'username' and 'password'
# Enter your log-in details
URL = 'http://ringzer0ctf.com/login/'
USERNAME = 'kenji'
PASSWORD = '123@Blue3'
login_data = {'username':USERNAME,'password':PASSWORD}

my_session = requests.Session()
my_session.post(URL, data=login_data)

page_task = my_session.get('http://ringzer0ctf.com/challenges/119')
# print page_task.content

# Convert ascii art to a digital number 
pattern = '----- BEGIN MESSAGE -----<br />[\r\n\s]*(?:<br />)+?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)?((?:[&nbsp;x]+?<br />){5})(?:<br />)+?[\r\n\s]*----- END MESSAGE -----'
print(pattern)
message_art = re.findall(re.compile(pattern), page_task.text)
print(message_art)
# print message_art
message_answer = ''
for i in range(10):
    message_answer += str(number_art.index(str(message_art[0][i])))
# print message_answer

# Send our answer to server
page_answer = my_session.get('http://ringzer0ctf.com/challenges/119/' + message_answer)
# print page_answer.content

# Get final flag from response page
my_flag = 'FLAG-' + re.findall('<div class="flag">FLAG-(.+?)</div>', page_answer.text)[0]
print (my_flag)

# my_flag - that's your flag, which you have to submit




