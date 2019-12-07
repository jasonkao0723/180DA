* Boot up raspberry pi
* Ssh to Raspberry pi
* Setup /etc/wpa_supplicant/wpa_supplicant.conf
* Add auto report ip function
* How to run python script upon boot up
* Set raspberry pi as wifi repeater
* Reportip.py

#### Boot up raspberry pi

After flash the image, here we used stretch 2019

Open /Volumes/boot 

Open the cmdline.txt with sublime Text, add the following to the end

```
modules-load=dwc2,g_ether
```

Open the config.txt with sublime Text, add the following to the end

```
dtoverlay=dwc2
enable_uart=1
```

To enable ssh, we have to create ssh file, this can be done in terminal:

```
$ cd /Volumes/boot
$ touch ssh
```

To enable wifi, do this in terminal

```
$ touch wpa_supplicant.conf
```

Choose one of them, or both from the next section "Setup /etc/wpa_supplicant/wpa_supplicant.conf", add to your wpa_supplicant.conf file.

Save and eject the SD card.

#### Ssh to Raspberry pi

```
ssh pi@raspberrypi.local
```

Setup password

```
passwd
# for short weak password
sudo -s
passwd
```

####Setup /etc/wpa_supplicant/wpa_supplicant.conf

Replace ssid and password with your wifi name and password

Set up wifi eduroam

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
        ssid="eduroam"
        scan_ssid=1
        key_mgmt=WPA-EAP
        eap=PEAP
        identity="yourusername@ucla.edu"
        password="yourpassword"
        phase1="peaplabel=0"
        phase2="auth=MSCHAPV2"
}
```

Set up wifi home

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="Kenny-EE"
    psk="TingFengHui"
    scan_ssid=1
}
```

```

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="Kenny-EE"
    psk="TingFengHui"
    id_str="AP1"
}

network={
    ssid="bear_iphone"
    psk="12345678"
    id_str="AP2"
}


```

Update and Upgrade your Pi

```
sudo apt update && sudo apt full-upgrade && sudo reboot
```

####Add auto report ip function

1. ```sudo apt install git```

2. ```git clone https://github.com/jasonkao0723/180DA.git  ```

3. Go to 180DA/Andrew/proj0/ , copy the file [reportip.py](https://github.com/jasonkao0723/180DA/blob/master/Andrew/proj0/reportip.py) to a place where you want to store

   Alternatively, check the **Reportip.py** section, and copy to your home folder

4. ```vim reportip.py```, edit the email configuration

   ```
   smtpserver：smtp.gmail.com
   username：email account
   password: password
   sender：sender, same as username
   receiver：a list of email can be put in here
   subject: IP[changed]
   ```

   ```
   smtpserver：smtp.gmail.com
   username：email account
   password: password
   sender：ece180raspberrypi@gmail.com
   receiver：a list of email can be put in here
   subject: IP[changed]
   ```

5. Run python upon boot up

   ```
   Run sudo -s
   Run vim /etc/rc.local
   # report ip to e-mail
   # Copy and past to rc.local
   rm /path/lastip.txt
   touch /path/lastip.txt
   /usr/bin/python /path/reportip.py
   ```

#### How to run python script upon boot up

1. Turn on auto login by selecting Boot Options-->Console Autologin Text console, automatiaclly logged in as ‘pi’ user```sudo raspi-config```
2. Edit /etc/profile, add path of python script to the end

#### Set raspberry pi as wifi repeater

https://blog.thewalr.us/2017/09/26/raspberry-pi-zero-w-simultaneous-ap-and-managed-mode-wifi/

* Wifi name = "GoJasonGo"
* Password = "goodpassword"

```
## /etc/hostapd/hostapd.conf
ctrl_interface=/var/run/hostapd
ctrl_interface_group=0
interface=ap0
driver=nl80211
ssid=GoJassonGo
hw_mode=g
channel=11
wmm_enabled=0
macaddr_acl=0
auth_algs=1
wpa=2
wpa_passphrase=goodpassword
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
```

####Reportip.py

Tings to change:

* receiver, your email, if you want to receive text message, replace email with 

   ```phone number@txt.att.net``` (For AT&T)

* subject, the subject of email

```python
import subprocess
import socket
import fcntl
import time
import struct
import smtplib
import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import re
import urllib2

# get bluetooth mac address
result = subprocess.check_output(['hciconfig'], stdin=subprocess.PIPE)
result = re.search('BD Address:(.*)ACL', result)
result = result.group(1)
result = result.strip()
print(result)

# the e-mail config
# this is just a simple format,this e-mail doesn't exist.
smtpserver  = "smtp.gmail.com"
sender_port = 587
username  = "ece180raspberrypi@gmail.com"
password  = "iwgtGC2018"
sender 	  = "ece180raspberrypi@gmail.com"
receiver  = ["wbb1263@gmail.com"]
subject   = "[Henry's Pi]"

def sendEmail(msg):
    msgRoot = "Subject: " + subject + "\n\n" + "IP address: " + str(msg) +"\n"+ "BT address: " + str(result)
    smtp = smtplib.SMTP("smtp.gmail.com", sender_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    # if cannot receive email, uncomment the next line, it shows debug information
    # smtp.set_debuglevel(1)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot)
    smtp.quit()

def check_network():
    while True:
        try:
            print ("Network is Ready!")
            break
        except Exception, e:
           print (e)
           print ("Network is not ready,Sleep 5s....")
           time.sleep(10)
    return True

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s'.encode(), ifname[:15].encode())
    )[20:24])


if __name__ == '__main__':
    check_network()
    ipaddr= get_ip_address('wlan0')
    emailip=str(ipaddr)
    print ("IP: {}".format(emailip))
    sendEmail(emailip)
    print ("Successfully send the e-mail.")
```

