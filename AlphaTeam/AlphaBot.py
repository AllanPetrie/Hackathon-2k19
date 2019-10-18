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

from Server import *
from Team import *


# Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
parser.add_argument('-H', '--hostname', default='0.0.0.0', help='Hostname to connect to')
parser.add_argument('-p', '--port', default=8052, type=int, help='Port to connect to')
parser.add_argument('-n', '--name', default='AlphaTeam:HIVEbot', help='Name of bot')
args = parser.parse_args()

# Set up console logging
if args.debug:
        logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
else:
	logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

<<<<<<< HEAD
# Connect to game server
=======
>>>>>>> a924e0971f1f75c319b2919085f15743b5caed3c
ServerDeetz = GameServerDetails(args.hostname, args.port)

team = Team(ServerDeetz, "Alpha", ["Cheeky", "Absolute", "Gary", "Fish"])

while True:
	team.update()