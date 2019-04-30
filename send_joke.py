#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import ssl
import requests
import datetime
import yaml

def load_config(path='config.yml'):
    with open(path, 'r') as f:
        return yaml.load(f)

def get_joke(cfg):
    r = requests.get(cfg['url'], headers=cfg['headers'])
    return r.text

def send_mail(srv, mail, message):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(srv['address'], srv['port'], context=context) as server:
        server.login(srv['user'], srv['password'])

        msg = MIMEText(message, 'html', 'utf8')
        msg['from'] = mail['email']
        msg['subject'] = Header(mail["subject"], 'utf8')
        
        for to in mail['to']:
            msg['to'] = to
            server.sendmail(msg['from'], to, msg.as_string())

if __name__ == '__main__':
    cfg = load_config()
    joke = get_joke(cfg['joke'])
    send_mail(cfg['server'], cfg['mail'], joke)
    
    with open('joke_log.txt', 'a') as f:
        now = datetime.datetime.now()
        print(now.isoformat(), joke, file=f)

