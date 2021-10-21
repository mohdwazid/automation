#!/bin/python3.6
import paramiko
import time
import argparse

parser = argparse.ArgumentParser(description="NIS service verification")
parser.add_argument("-srvfile", help="Server file")

args = parser.parse_args()
srvfile = args.srvfile
#srvstatic = '10.1.5.1'
user = 'root'
port = 22
#password = '0n2mspd!'
with open(srvfile) as sf:
    srvs = sf.readlines()
    for srv in srvs:
        try:
            print("=============================================")
            print("Server is ", srv)
            srvname= srv.replace('\n', '')
            command = 'hostname;id mohdw;cd /home/mohdw;pwd'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(srvname,port,user,"")
            stdin, stdout, stderr = ssh.exec_command(command, bufsize=1)
            lines = stdout.readlines()

            for line in lines:
                try:
                    print(line)
                except:
                    print("#### Unable to print line ####", line)
        except:
            print("##### Unable to connect to server :#####", srvname)
