#!/usr/bin/python

import json
import socket
import logging
import binascii
import struct
import argparse
import random
import time
import math
from time import sleep

from Server import *
from Team import *


# Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true',
                    help='Enable debug output')
parser.add_argument('-H', '--hostname', default='0.0.0.0',
                    help='Hostname to connect to')
parser.add_argument('-p', '--port', default=8052,
                    type=int, help='Port to connect to')
parser.add_argument(
    '-n', '--name', default='AlphaTeam', help='Name of team')
parser.add_argument(
    '-b', '--beta', action='store_true', help='Spawn enemy team')
args = parser.parse_args()

# Set up console logging
if args.debug:
    logging.basicConfig(
        format='[%(asctime)s] %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

ServerDeetz = GameServerDetails(args.hostname, args.port)

team = Team(ServerDeetz, args.name, ["Cheeky", "Absolute", "Gary", "Fish"])
betaTeam = None
if args.beta:
    betaTeam = Team(ServerDeetz, "Beta", ["A", "B", "C", "D"])

while True:
    sleep(0.05)
    team.getTeamKnowledge()
    team.update()
    if args.beta:
        betaTeam.getTeamKnowledge()
        betaTeam.update()
