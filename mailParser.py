#!/bin/python3

import re
import os
import socket

remoteDomains = []
localDomains = []
localMailArray = {}
remoteMailArray = {}
def localDomain():
    localDomain = []
    vDomain = open("/var/qmail/control/virtualdomains","r")
    for domain in vDomain:
        localDomain.append(domain.split(":")[0])
    return localDomain
    vDomain.close()

logFile = open("/var/log/send/current",'r')
vDomain = localDomain()
for line in logFile:
    if "from" in line:
        try:
            match = re.search("\<.+>", line)
            domain = match.group().strip('<>').split('@')[1]
            sender = match.group().strip('<>')
            if domain in vDomain or domain == socket.gethostname():
                localDomains.append(sender)
            else:
                remoteDomains.append(sender)
        except:
            continue
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
