#!/bin/python3

import re
import os
import socket
import sys

remoteDomains = []
localDomains = []
localMailArray = {}
remoteMailArray = {}
domain=''

def localDomain():
    localDomain = []
    vDomain = open("/var/qmail/control/virtualdomains","r")
    for domain in vDomain:
        localDomain.append(domain.split(":")[0])
    return localDomain
    vDomain.close()
    
def vhostDomain():
    absPath=''
    domain=''
    vhostDomain=[]
    vhost = []
    dir = "/etc/httpd/conf.d/"
    for item in os.walk(dir):
        curDir = item[0]
        subDirs = item[1]
        subFiles = item[2]
        for subFile in subFiles:
            if subFile.startswith('vhost_'):
                absPath = "{}/{}".format(curDir,subFile)
                if absPath not in vhost:
                    vhost.append(absPath)
    for file in vhost:
        line = open(file,'r')
        for item in line:
            if 'ServerName' in item or 'ServerAlias' in item:
                match = re.search("w*\.[a-z].+",item)
                if match is not None:
                    domains = match.group()
                    for item in domains.split():
                        if item not in vhostDomain:
                            vhostDomain.append(item)
    line.close
    return vhostDomain
            
logFile = open("/var/log/send/current",'r')
vDomain = localDomain()
vhostDomain = vhostDomain()
for line in logFile:
    if "from" in line:
        match = re.search("\<.+>", line)
        if match is not None:
            domain = match.group().strip('<>').split('@')[1]
            sender = match.group().strip('<>')
        if domain in vDomain or domain == socket.gethostname() or domain in vhostDomain:
            localDomains.append(sender)
##counting domains
for domain in localDomains:
    if domain not in localMailArray:
        localMailArray[domain] = 1
    else:
        localMailArray[domain] += 1

for domain in remoteDomains:
    if domain not in remoteMailArray:
        remoteMailArray[domain] = 1
    else:
        remoteMailArray[domain] += 1
def getHits(t):
    return t[1]

sortedResult = sorted(localMailArray.items(),key=getHits)
print("+--------------------------------------------------------------------+------------+")
print("|Email Address                                                       |       Count|")
print("+--------------------------------------------------------------------+------------+")
for item in sortedResult:
    mailAddress = item[0]
    hits = item[1]
    print("|{:68}| {:11}|".format(mailAddress,hits))
print("+--------------------------------------------------------------------+------------+")

