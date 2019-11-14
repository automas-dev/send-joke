#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import ssl
import requests
import datetime
import json


CONFIG_FILE = 'config.json'
MAIL_LIST_FILE = 'mail_list.txt'
LOG_FILE = 'joke_log.txt'

with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)
    mail_server = config['mail_server']
    joke_server = config['joke_server']
    from_address = config['from_address']
    subject_line = config['subject_line']

with open(MAIL_LIST_FILE, 'r') as f:
    mail_list = list(filter(lambda l: len(l) > 0,
                            map(lambda l: l.strip(),
                                f)))


def log_joke(joke):
    with open(LOG_FILE, 'a') as f:
        now = datetime.datetime.now()
        f.write(now.isoformat())
        f.write(' ' + joke + '\n')


def get_joke(url, headers):
    resp = requests.get(url, headers=headers)
    joke = resp.content.decode('utf-8', errors='replace')
    log_joke(joke)
    return joke


joke = get_joke(joke_server['url'], joke_server['headers'])
print('Get Joke:', joke)

context = ssl.create_default_context()
address = mail_server['address']
port = mail_server['port']
username = mail_server['username']
password = mail_server['password']

print('Connecting to mail server')
with smtplib.SMTP_SSL(address, port, context=context) as server:
    server.login(username, password)
    print('Authentication successful')

    for to in mail_list:
        print('Sending to', to)
        msg = MIMEText(joke.encode('utf8'), 'html', 'utf8')
        msg['from'] = from_address
        msg['subject'] = Header(subject_line, 'utf8')
        msg['to'] = to
        server.sendmail(msg['from'], to, msg.as_string())
