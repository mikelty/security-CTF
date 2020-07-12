import requests

s=requests.Session()
r=s.get(url='http://natas6.natas.labs.overthewire.org/includes/secret.inc',auth=('natas6','aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1'))
print(r.text)
