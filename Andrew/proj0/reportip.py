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
receiver  = ["ece180raspberrypi@gmail.com"]
subject   = "[Susie_RPI]IP CHANGED"

# file_path config
file_path = "/root/rootcrons/lastip.txt"

def sendEmail(msg):
    msgRoot = "Subject: " + subject + "\n\n" + "IP address: " + str(msg) +"\n"+ "BT address: " + str(result)
    smtp = smtplib.SMTP("smtp.gmail.com", sender_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
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
    print(emailip)
    ip_file = open(file_path)
    last_ip = ip_file.read()
    ip_file.close()
    if last_ip == emailip:
        print ("IP not change.")
    else:
        print ("IP changed. New ip: {}".format(emailip))
        ip_file = open(file_path,"w")
        ip_file.write(str(emailip))
        ip_file.close()

        sendEmail(emailip)
        print ("Successfully send the e-mail.")
