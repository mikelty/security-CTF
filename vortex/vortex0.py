from telnetlib import Telnet
#Gq#qu3bF3
host='vortex.labs.overthewire.org'
port=5842

with Telnet(host,port) as tn:
    raw_integers,total=tn.read_some(),0
    for i in range(4):
        integer=raw_integers[i*4:i*4+4]
        total+=int.from_bytes(integer,byteorder='little',signed=False)
    raw_total=(total).to_bytes(4,byteorder='little')
    tn.write(raw_total)
    print(tn.read_all())
