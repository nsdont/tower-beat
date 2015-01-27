#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
import sqlite3
import json
import datetime
import importlib
import keyring
import requests

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

from lxml import etree

import consts

import logging
import logging.config
logging.config.dictConfig(consts.LOGGING)

logger = logging.getLogger('beatit')

config = {}
notifiers = []


def notify(message, *args, **kwargs):
    for notifier in notifiers:
        notifier.notify(message, *args, **kwargs)


def decrypt_cookie_value(value):
    password = keyring.get_password(
        consts.KEYRING_SERVICE, consts.KEYRING_USERNAME).encode('utf-8')
    key = PBKDF2(password,
                 consts.DECRYPT_COOKIE_VALUE_SALT,
                 consts.DECRYPT_COOKIE_VALUE_LENGTH,
                 consts.DECRYPT_COOKIE_VALUE_ITERATIONS)
    cipher = AES.new(key, AES.MODE_CBC, IV=consts.DECRYPT_COOKIE_VALUE_IV)

    decrypted_value = cipher.decrypt(value[3:])
    return decrypted_value[:-ord(decrypted_value[-1])].decode('utf-8')


def read_session_cookie():
    if 'session_cookie' in config:
        return config['session_cookie']

    with sqlite3.connect(consts.SESSION_COOKIES_LOCATION) as conn:
        cursor = conn.execute(consts.QUERY_STATEMENT)
        cookie = cursor.fetchone()

    if not cookie:
        notify(consts.NOTIFICATION_NOT_LOGIN)
        return None

    encrypted_cookie_value = cookie[-1]
    decrypted_cookie_value = decrypt_cookie_value(encrypted_cookie_value)
    return decrypted_cookie_value


def analyze_response(response):
    tree = etree.HTML(response.content.decode('utf-8'))
    dues = tree.xpath(consts.DUE_XPATH)

    for due in dues:
        date = datetime.datetime.strptime(due.text, '%Y-%m-%d')
        today = datetime.datetime.now()
        if all([date.year == today.year,
                date.month == today.month,
                date.day == today.day]):
            notify(consts.NOTIFICATION_TASK_FOUND,
                   open=response.url)
            return


def load_config():
    logger.info('Loading configuration...')
    rv = {}
    try:
        with open(os.path.join(consts.BASE_DIR,
                               'config.json')) as f:
            rv = json.loads(f.read())
    except Exception as e:
        logger.error('An exception raised during loading config: '
                     '"{e.message}".'.format(e=e))
        logger.warning('Default configuration used.')
        rv = {'notifiers': ['notifiers.console'], 'projects': []}

    config.update(rv)
    logger.info('Configuration loaded.')


def load_notifiers():
    logger.info('Loading notifiers...')
    for mod_path in config['notifiers']:
        mod = importlib.import_module(mod_path)
        notifier = mod.Notifier(config)
        notifiers.append(notifier)
        logger.info('"{mod_path}" loaded.'.format(mod_path=mod_path))
    logger.info('Notifiers loaded.')


def tower_beat():
    logger.info('Reading session cookie.')
    session_cookie = read_session_cookie()
    if not session_cookie:
        raise Exception('Session cookie lost.\nExit.')

    logger.info('Session cookie read.')

    cookies = {consts.SESSION_COOKIE_NAME: session_cookie}
    for url in config['projects']:
        logger.info('Fetching project information from '
                    '"{url}".'.format(url=url))
        response = requests.get(url, cookies=cookies)
        if response.url == consts.LOGIN_URL:
            notify(consts.NOTIFICATION_NOT_LOGIN)
            raise Exception('No available session.')
        analyze_response(response)

    logger.info('Done.')


def main():
    load_config()
    load_notifiers()

    tower_beat()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e.message)
