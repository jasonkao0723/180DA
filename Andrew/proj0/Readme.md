**ECE-180DA report 2**

Yu Gao

#### Accomplished task

1. Retrieving IP address of raspberry pi and send it to my email and phone as txt message

   * Log in to Root account using command ```sudo -s```, because I need to add file under ```/root/rootcrons```

   * ```vim reportip.py```, edit the email configuration

     ```
     smtpserver：smtp.gmail.com
     username：email account
     password: password
     sender：sender, same as username
     receiver：a list of email can be put in here
     subject: IP[changed]
     ```

   * ```crontab /root/rootcrons/rootcron```, add the test to crontab list.

   * ```/etc/init.d/cron restart```, make the crontab configuration effective right now

   * Test by excuse the ```reportip.py``` once, the output should be "successful"

   * Send the email with IP address on every boot up

     ```
     # sudo -s
     # vim /etc/rc.local
     # report ip to e-mail
     rm /root/rootcrons/lastip.txt
     touch /root/rootcrons/lastip.txt
     /usr/bin/python /root/rootcrons/reportip.py
     ```

<div style="page-break-after: always;"></div>

<img src="https://github.com/jasonkao0723/180DA/blob/master/Andrew/proj0/IMG_3529.PNG" width="281" height="609" />

1. Extract the bluetooth MAC address from raspberry pi.

   ```python
   # hciconfig | grep "BD Address" | awk '{ print $3}'
   # run hciconfig command in python and extract address information
   
   import subprocess
   import re
   
   result = subprocess.run(['hciconfig'], stdout=subprocess.PIPE)
   result = str (result.stdout)
   result = re.search('BD Address:(.*)ACL', result)
   result = result.group(1)
   result = result.strip()
   print(result)
   ```

2. Pair two raspberry pi via bluetoothctl.

<img src="https://github.com/jasonkao0723/180DA/blob/master/Andrew/proj0/Screen%20Shot%202019-11-15%20at%2011.12.33%20AM.png" width="758" height="530" />

#### Not accomplished task

1. Sending message via bluetooth in python. I found a module "bluetooth" online, will try it this Friday.

#### Plan for the next week

1. Creating a html website, and using ftp upload the IP address up to the server
2. Pairing 4 raspberry pi and send message from 1st to the rest of raspberry pis.

#### Notes

* Absolute address in crontab file and rc.local

* When send message from pi to email, remember to disable the "Less secure app access" by going to https://myaccount.google.com/lesssecureapps?utm_source=google-account&utm_medium=web, otherwise error like this:

  ```
  smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepte
  d. Learn more at\n5.7.8 http://support.google.com/mail/bin/answer.py?answer=1425
  7\n5.7.8 {BADCREDENTIALS} s10sm9426107qam.7 - gsmtp')
  ```

