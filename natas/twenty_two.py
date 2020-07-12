import requests

auth=('natas22','chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ')
url='http://natas22.natas.labs.overthewire.org/index.php?revelio=true'
s=requests.Session()
r=s.get(url,auth=auth,allow_redirects=False)
print(r.text)
