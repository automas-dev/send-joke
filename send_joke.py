#!/usr/bin/env python3

import os
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
LOG_FILE = 'joke_log.json'
BODY_FILE = 'body.html'


class JokeFetchError(Exception):
    pass


# Load config file
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)
    mail_server = config['mail_server']
    joke_server = config['joke_server']
    from_address = config['from_address']
    subject_line = config['subject_line']


# Load email list
with open(MAIL_LIST_FILE, 'r') as f:
    mail_list = list(filter(lambda l: len(l) > 0,
                            map(lambda l: l.strip(),
                                f)))


# Create the log file if it does not exist
if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        f.write('[]')


# Load the log file to check for duplicates
with open(LOG_FILE, 'r') as f:
    log_data = json.load(f)
    print('Loaded log data')
    print(log_data)


# Load the body template
with open(BODY_FILE, 'r') as f:
    body_template = f.read()


def log_has_joke(joke_id):
    for joke in log_data:
        if joke['id'] == joke_id:
            return True
    return False


def log_joke(joke):
    with open(LOG_FILE, 'w') as f:
        now = datetime.datetime.now()
        joke['timestamp'] = str(now)
        log_data.append(joke)
        json.dump(log_data, f)


def get_joke(url, headers, attempts=3):
    for i in range(attempts):
        print('Attempt', i+1)
        resp = requests.get(url, headers=headers)
        joke = resp.content.decode('utf-8', errors='replace')
        joke = json.loads(joke)
        log_joke(joke)
        return joke['joke']
    raise JokeFetchError(
        f'Could not find a new joke after {attempts} attempts')


def in_tags(tag, text, attr=''):
    return f'<{tag} {attr}>{text}</{tag}>'


def build_message(joke):
    text = ''

    if 'message' in config:
        text += config['message'] + '<br/><br/>\n'

    #text += in_tags('div', joke, 'class="joke"')
    text += joke

    return body_template % text


try:
    joke = get_joke(joke_server['url'],
                    joke_server['headers'], joke_server['attempts'])
    print('Get Joke:', joke)
except JokeFetchError as e:
    print('Failed to fetch a joke')
    print(e)
    joke = None

context = ssl.create_default_context()
address = mail_server['address']
port = mail_server['port']
username = mail_server['username']
password = mail_server['password']

print('Connecting to mail server')
with smtplib.SMTP_SSL(address, port, context=context) as server:
    server.login(username, password)
    print('Authentication successful')

    if joke is None:
        msg = MIMEText('Your joke server failed to find a unique joke!'.encode(
            'utf8'), 'html', 'utf8')
        msg['from'] = from_address
        msg['subject'] = Header('Joke Server Fatal Error', 'utf8')
        msg['to'] = from_address
        server.sendmail(msg['from'], from_address, msg.as_string())
        exit(1)

    for to in mail_list:
        print('Sending to', to)
        text = build_message(joke)
        print('Final message', text)
        msg = MIMEText(text.encode('utf8'), 'html', 'utf8')
        msg['from'] = from_address
        msg['subject'] = Header(subject_line, 'utf8')
        msg['to'] = to
        server.sendmail(msg['from'], to, msg.as_string())
