#!/usr/bin/env python3
import requests
import json
import pprint
import sys
import os
import configparser
import csv

# read configuration file
ENVIRON = 'PROD'
config = configparser.ConfigParser()
config.read('config.ini')

# Read the assetchians.json file
script_dir = os.getcwd()
with open(script_dir + '/assetchains.json') as file:
    assetchains = json.load(file)

# configure pretty printer
pp = pprint.PrettyPrinter(width=41, compact=True)

# get connection options
conn = {}
connection_options = [
    'iguana_ip',
    'iguana_port']
for i in connection_options:
    conn[i] = config[ENVIRON][i]

# define function that posts json data to iguana
def post_rpc(url, payload, auth=None):
    try:
        r = requests.post(url, data=json.dumps(payload), auth=auth)
        return(json.loads(r.text))
    except Exception as e:
        raise Exception("Couldn't connect to " + url + ": ", e)

# define url's
iguana_url = 'http://' + conn['iguana_ip'] + ':' + conn['iguana_port']

# set btcpubkey
btcpubkey = config[ENVIRON]['btcpubkey']

# dpow
def dpow(symbol, freq):
    payload = {
        "agent": "iguana",
        "method": "dpow",
        "symbol": symbol,
        "freq": freq,
        "pubkey": btcpubkey
    }
    response_dpow = post_rpc(iguana_url, payload)
    print('== response_dpow ' + symbol + ' ==')
    pp.pprint(response_dpow)

# dpow assetchains
for chain in assetchains:
    for param, value in chain.items():
        ac_chain = chain['ac_name']
        if param == 'freq':
            ac_freq = chain['freq']
            dpow(ac_chain,ac_freq)
