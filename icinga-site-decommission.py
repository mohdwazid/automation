#!/usr/bin/env /bin/python3
import requests
import json
import sys
import subprocess
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if len(sys.argv)==3:
    org=sys.argv[1]
    location=sys.argv[2]
else:
    print('Usage: icinga_disable_site.py org location')
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
    'filter':'match(location,host.vars.location) && match(org,host.vars.org) ',
    'filter_vars':{
        'location':'*%s'%location,
        'org':'*%s'%org,
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

print(" ### Total number of servers to be disabled >>> " +  str(servercount) )

for count in range(servercount):
    #hlocation = icingaoutput['results'][count]['attrs']['vars']['location']
    hname = icingaoutput['results'][count]['name']

    cmdout = subprocess.Popen(["/bin/icingacli","director","host","set",hname,"--disabled","n"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = cmdout.communicate()

    print(stdout)
    print(stderr)
