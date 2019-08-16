# -*- coding: utf-8 -*-

import os
import sys
import json
import copy
import time
import requests
import requests
import datetime

API_AUTH = 'https://www.victorsmartkill.com/api-token-auth/'
API_TRAPS = 'https://www.victorsmartkill.com/traps/'
API_MOBILEAPPS = 'https://www.victorsmartkill.com/mobileapps/'
API_OPERATORS = 'https://www.victorsmartkill.com/operators/2/'
API_USERS =  'https://www.victorsmartkill.com/users/'

Headers = {
           'Host' : 'www.victorsmartkill.com',
           'Connection':'keep-alive',
           'Accept':'*/*',
           'User-Agent':'Victor/1.7 (com.victor.victorsmartkill; build:10; iOS 12.4.0) Alamofire/4.7.0',
           'Accept-Language':'en-US;q=1.0',
           'Authorization':'Token {0}',
           'Accept-Encoding':'gzip;q=1.0, compress;q=0.5',
           'content-length': '0'
           }


def get_token(config_fname, token_fname):
    if not os.path.exists(config_fname):
        print('Needs config file "{0}"'.format(config_fname))
        sys.exit(1)

    with open(config_fname, 'r') as fd:
        config_str = fd.read()

    try:
        config = json.loads(config_str)
    except:
        print("Couldn't open config file '{0}'".format(config_fname))
        config = None

    if os.path.exists(token_fname):
        with open(token_fname, 'r') as fd:
            token_str = fd.read()

        token = json.loads(token_str)
    else:

        # Get the password from the command line
        if 'password' not in config:
            password = getpass.getpass()
        else:
            password = config['password']

        token = {}
        token['current'] = {}
        token['old'] = []
        data = {"username": config['username'],
                "password": password}
        response = requests.post(API_AUTH, data)
        token['current']['token'] = response.json()['token']
        token['current']['request_date'] = time.time()
        token['current']['experation_date'] = -1.0

        with open(token_fname, 'w') as fd:
            fd.write(json.dumps(token))

    return token['current']['token']


def update_config(config_fname, token_fname):

    token = get_token(config_fname, token_fname)
    headers = copy.deepcopy(Headers)
    headers['Authorization'] = headers['Authorization'].format(token)

    response = requests.get(API_TRAPS, headers=headers)

    traps_response = response.json()

    traps = []
    for trap in traps_response['results']:
        trap_id = trap['id']
        trap_name = trap['name']
        trap_serial = trap['serial_number']

        d = {"id": trap_id, "name": trap_name, "serial": trap_serial}
        traps.append(d)

    with open(config_fname, 'r') as fd:
        config_s = fd.read()

    config = json.loads(config_s)
    config['traps'] = traps

    with open(config_fname, 'w') as fd:
        fd.write(json.dumps(config))


def status(config_fname, token_fname, within=None, name=None):

    token = get_token(config_fname, token_fname)
    headers = copy.deepcopy(Headers)
    headers['Authorization'] = headers['Authorization'].format(token)

    r = []

    # if name is None check all traps

    if name:
        pass
    else:
        response = requests.get(API_TRAPS, headers=headers)

        traps_response = response.json()

        traps = []
        for trap in traps_response['results']:
            trap_id = trap['id']
            trap_name = trap['name']
            kills_present = trap['trapstatistics']['kills_present']
            last_kill = trap['trapstatistics']['last_kill_date']
            last_report = trap['trapstatistics']['last_report_date']

            d = {"id": trap_id,
                 "name": trap_name,
                 "kills_present": kills_present,
                 "last_kill": last_kill,
                 "last_report": last_report}

            r.append(d)

    return r


def last_kill(config_fname, token_fname):

    pass
