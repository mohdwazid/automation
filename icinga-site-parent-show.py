#!/usr/bin/env /bin/python3
import unicodedata
import requests
import json
import sys
import subprocess
import urllib3

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if len(sys.argv)==2:
    parent=sys.argv[1]
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

#parent='Shenzhen_Parent'

#url='https://10.201.199.98:5665/v1/objects/hosts'
url='https://localhost:5665/v1/objects/hosts'

dat={
    'filter':'match(parent,host.vars.parents) ',
    'filter_vars':{
        'parent':'*%s'%parent
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

print(" ### Total number of servers under parent >>> " +  str(servercount) )

for count in range(servercount):
    #hlocation = icingaoutput['results'][count]['attrs']['vars']['location']
    hname = icingaoutput['results'][count]['name']

    cmdout = subprocess.Popen(["/bin/icingacli","director","host","show",hname,"--json"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = cmdout.communicate()
    out = stdout.decode(sys.stdin.encoding)
    #err = stderr.decode(sys.stdin.encoding)

    jsonout = json.loads(out)
    print(" ### Icinga director object name is >>> " + jsonout["object_name"])
