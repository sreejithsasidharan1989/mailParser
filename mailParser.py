#!/usr/bin/python3

#import modules
import re
import os
import socket
import sys
import posixpath

##global variables
remoteDomains = []
localDomains = []
localMailArray = {}
remoteMailArray = {}
domain=''
mailArray = {}
args = sys.argv[1:]

#sort function
def getHits(t):
    return t[1]

#check for domain name in virtualdomains
def localDomain():
    localDomain = []
    vDomain = open("/var/qmail/control/virtualdomains","r")
    for domain in vDomain:
        localDomain.append(domain.split(":")[0])
    return localDomain
    vDomain.close()

#check for domain name in vhost files
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
                match = item.split()
                for domain in match:
                    if domain not in vhostDomain and domain.count('.') <= 2 and domain.count('.') >= 1 and domain.startswith('www.') is False and domain.startswith('ftp.') is False and domain.startswith('mail.') is False and domain.startswith('eadn-') is False:
                        vhostDomain.append(domain)
    line.close
    return vhostDomain

#track mail activity
def mailTracker(mailId):
    import subprocess
    domain = vhostDomain()
    log = subprocess.check_output("tai64nlocal < /var/log/send/current",shell=True)
    logFile = open('mail_log.txt','w')
    logFile.write(log.decode('utf-8'))
    logFile.close()
    logFile = open('mail_log.txt','r')
    ilogFile = iter(logFile)
    for line in ilogFile:
        try:
            flag=0
            date=''
            sender=''
            receiver=''
            direction=''
            if "info msg" in line:
                nline = next(ilogFile)
                match = re.search("(^[0-9].+\-[0-9].+\:\d+)",line)
                date = match.group()
                match = re.search("\d+: ",line)
                msg_id = match.group().rstrip(':')
                match = re.search("\<.+>", line)
                sender = match.group().strip('<>')
                match = re.search("[A-Za-z0-9\-\_\.]+\@[a-z.-]*", nline)
                receiver = match.group()
            
            if "to local" in nline:
                direction = "Incoming"
            else:
                direction = "Outgoing"
            if sender == mailId or receiver == mailId:
                if msg_id not in mailArray:
                    mailArray[msg_id] = {flag: {"Date": date, "Sender": sender, "Receiver":receiver, "Direction": direction}}
                else:
                    key_len = len(mailArray[msg_id].keys())
                    flag = flag + key_len
                    mailArray[msg_id].update({flag: {"Date": date, "Sender": sender, "Receiver":receiver, "Direction": direction}})

        except:
              continue
    print("+--------------------+-----------------------------------------+-----------------------------------------+--------------+")
    print("|   Date             |        Sender                           |          Receiver                       |   Direction  |")
    print("+--------------------+-----------------------------------------+-----------------------------------------+--------------+")
    for ids in mailArray:
         key = len(mailArray[ids].keys())
         key = key - 1
         for num in range(key, -1, -1):
            date = mailArray[ids][num]["Date"]
            sender = mailArray[ids][num]["Sender"]
            receiver = mailArray[ids][num]["Receiver"]
            direction = mailArray[ids][num]["Direction"]
            if mailId in sender:
               print("|{:15} | {:40}| {:40}| {:12} |".format(date,sender,receiver,direction))
    print("+--------------------+-----------------------------------------+-----------------------------------------+--------------+")

    if os.path.exists("mail_log.txt"):
       os.remove("mail_log.txt")

#count number of emails
def logParser(file):
    vhostDom=''
    logFile = open(file,'r')
    vDomain = localDomain()
    vhostDom = vhostDomain()
    for line in logFile:
        domain=''
        sender=''
        if "from <" in line:
            match = re.search("\<.+>", line)
            if match is not None:
                domain = match.group().strip('<>').split('@')[1]
                sender = match.group().strip('<>')
            if domain in vDomain or domain == socket.gethostname() or domain in vhostDom:
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
    sortedResult = sorted(localMailArray.items(),key=getHits)
    print("+--------------------------------------------------------------------+------------+")
    print("|Email Address                                                       |       Count|")
    print("+--------------------------------------------------------------------+------------+")
    for item in sortedResult:
        mailAddress = item[0]
        hits = item[1]
        print("|{:68}| {:11}|".format(mailAddress,hits))
    print("+--------------------------------------------------------------------+------------+")

if len(args) == 0:
    file = "/var/log/send/current"
    logParser(file)
else:
    if len(args) > 1:
        print("Command Usage: mailParser </var/log/send/<filename>")
    else:
       file = args[0]
       if re.search("[A-Za-z0-9\-\_\.]+\@[a-z.-]*", file):
          mailTracker(file)
       else:
          if posixpath.isfile(file):
             try:
                logParser(file)
             except:
                print("Check the provided email log path")

