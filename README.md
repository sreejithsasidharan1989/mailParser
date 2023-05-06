### mailParser
-----------
#### Introduction
I wanted to share a Python script I’ve been working on with all of you. As you are all aware, the majority of the time when it comes to spam investigation, system administrators that works with servers installed with qmail rely on the output of the qmqtool command to ascertain whether there is active spamming occurring on the server. The qmqtool command is generally helpful, but if the spamming occurred before you could begin looking into it and the qmqtool command didn’t bring up much information, then you’ll need to examine the mail logs to identify the offender. Those who have worked with the send mail logs would undoubtedly agree with me that skimming through those logs is like looking for a needle in a haystack. This is where this script comes handy. You can use this script to simplify the process by having it parse the contents of the log files and count the number of emails sent from all mailboxes. The script will only show you email addresses that is either using the native server for sending emails or if the domain is hosted locally on that server. Becuase, in both cases, a domain can send an email. Additionally, you can pass an email address to this script as an argument to track the email attributes like, timestamp, sender’s address, receiver’s address and direction.


###### How to use the script:

1. Clone the this GitHub repository into your mellon server: 
   git clone https://github.com/sreejithsasidharan1989/mailParser

2. This will create a folder called "mailParser" within your working directory.
3. Now, run chmod u+x mailParser/mailParser.py
4. Then copy the script into an executable path
5. $ mailParser.py
```
+--------------------------------------------------------------------+------------+
|Email Address                                                       |       Count|
+--------------------------------------------------------------------+------------+
|test@example.com                                                    |          04|
|patrick@demosite.com                                                |          11|
|root@localhost                                                      |          11|
|admin@testsite.net                                                  |          16|
|sale@example.com                                                    |          23|
|postmaster@abcd.net                                                 |          30|
|info@mysite.com                                                     |         190|
+--------------------------------------------------------------------+------------+
```
###### 1. You can also run the script by passing a specific log file name as an argument
#
```
mailParser.py /var/log/send/@4000000063cb769e3358478c.s
```

###### 2. The scripts also accepts email address as a valid argument and track it from the current mail log file
#
```
mailParser.py test@example.com
+--------------------+-----------------------------------------+------------------------------+--------------+
|   Date             |        Sender                           |          Receiver            |   Direction  |
+--------------------+-----------------------------------------+------------------------------+--------------+
|2023-04-25 08:43:24 | test@example.com                        | mygmail@gmail.com            | Outgoing     |
|2023-04-25 08:43:24 | test@example.com                        | testmail@outlook.com         | Outgoing     |
|2023-04-25 08:54:10 | test@example.com                        | sales@sampledomain.com       | Outgoing     |
|2023-04-25 09:22:30 | test@example.com                        | demo@gmail.com               | Outgoing     |
+--------------------+-----------------------------------------+------------------------------+--------------+
```

###### 3.  The script can take only one argument at a time, if you specificy no arguments at all the it will use the log file /var/log/send/current by default.
#
###### 4. If there are more than one arguments, the script just terminates with following message
#
```
mailParser.py /var/log/send/@4000000063cb769e3358478c.s test@example.com
Command Usage: mailParser </var/log/send/<filename>
```

###### 5. It is also worth to note that, if the specified file path is incorrect or the mailbox format is flawed., please expect the script to bail out
#
#

#### Upcoming Feature
The output of the email track function will indicate whether the email was successfully received by the target recipient in a future update release of this script.


