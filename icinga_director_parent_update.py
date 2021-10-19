#!/usr/bin/env /bin/python3
import unicodedata
import requests
import json
import sys
import subprocess
import urllib3
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if len(sys.argv)==3:
    oldparent=sys.argv[1]
    newparent=sys.argv[2]
else:
    print('Usage: icinga_disable_site.py oldparent newparent')
    sys.exit()

hdr={
    'Accept':'application/json',
    'X-HTTP-Method-Override':'GET'
}
aut=(
    'apirouser',
    'S1erst0w3r'
)

url='https://localhost:5665/v1/objects/hosts'

dat={
    'filter':'match(oldparent,host.vars.parents) ',
    'filter_vars':{
        'oldparent':'*%s'%oldparent
    }
}

res=requests.post(
    url,
    headers=hdr,
    auth=aut,
    data=json.dumps(dat),
    verify=False
)

print(" ### Status Code >>> ", res.status_code)

icingaoutput = res.json()

servercount = len(icingaoutput['results'])

print(" ### Total number of servers under oldparent >>> " +  str(servercount) )
print("======================================================")

for count in range(servercount):
#for count in range(1):
    hname = icingaoutput['results'][count]['name']
    print(" ### Server to be updated >>> " + hname)

    # Appending the new parent
    idaddcmd = ['/bin/icingacli', 'director', 'host', 'set', hname, '--append-vars.parents', newparent]
    print(" ### Final Add Command >>>")
    print(idaddcmd)
    print(" ### Running Add Command >>>")
    idaddcmdout = subprocess.Popen(idaddcmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = idaddcmdout.communicate()
    print(stdout)
    print(stderr)

    time.sleep(10)

    # Deleting the existing parent
    iddelcmd = ['/bin/icingacli', 'director', 'host', 'set', hname, '--remove-vars.parents', oldparent]
    print(" ### Final Delete Command >>>")
    print(iddelcmd)
    print(" ### Running Delete Command >>>")
    iddelcmdout = subprocess.Popen(iddelcmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = iddelcmdout.communicate()
    print(stdout)
    print(stderr)
