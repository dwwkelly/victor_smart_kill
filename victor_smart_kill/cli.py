# -*- coding: utf-8 -*-

"""Console script for victor_smart_kill."""
import os
import sys
import json
import time
import click
import requests


API_AUTH = 'https://www.victorsmartkill.com/api-token-auth/'
API_TRAPS = 'https://www.victorsmartkill.com/traps/'
API_MOBILEAPPS = 'https://www.victorsmartkill.com/mobileapps/'
API_OPERATORS = 'https://www.victorsmartkill.com/operators/2/'
API_USERS =  'https://www.victorsmartkill.com/users/'


@click.command()
@click.option('-c', '--config', 'config_fname', default=os.path.expanduser("~/.victorsmartkill/config.json"), help='Config file to use')
@click.option('-t', '--token', 'token_fname', default=os.path.expanduser("~/.victorsmartkill/token.json"), help='JSON file to store token in')
def main(config_fname, token_fname):

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
        token = {}
        token['current'] = {}
        token['old'] = []
        data = {"username": config['username'],
                "password": config['password']}
        response = requests.post(API_AUTH, data)
        token['current']['token'] = response.json()['token']
        token['current']['request_date'] = time.time()
        token['current']['experation_date'] = -1.0

        with open(token_fname, 'w') as fd:
            fd.write(json.dumps(token))


    headers = {'Host' : 'www.victorsmartkill.com',
               'Connection':'keep-alive',
               'Accept':'*/*',
               'User-Agent':'Victor/1.7 (com.victor.victorsmartkill; build:10; iOS 12.4.0) Alamofire/4.7.0',
               'Accept-Language':'en-US;q=1.0',
               'Authorization':'Token {0}'.format(token['current']['token']),
               'Accept-Encoding':'gzip;q=1.0, compress;q=0.5',
               'content-length': '0'
               }
    response = requests.get(API_TRAPS, headers=headers)
    print(json.dumps(response.json()))


    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
