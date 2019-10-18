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
from Utils import *

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


# Connect to game server
GameServer = ServerComms(args.hostname, args.port)

# Spawn our tank
logging.info("Creating tank with name '{}'".format(args.name))
GameServer.sendMessage(ServerMessageTypes.CREATETANK, {'Name': args.name})
            
def evalChance(HDat,ODat):
        HHealth = HDat["Health"]
        OHealth = ODat["Health"]

        HAmmo = HDat["Ammo"]
        OAmmo = ODat["Ammo"]

        if HAmmo<OHealth:
                return(False)
        elif HHealth<OAmmo and HHealth == 1 and OHealth>1:
                return(False)
        else:
                return(True)

def goGoals(cur_x,cur_y):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        targ_x = 0
        if getDistance(cur_x,cur_y,0,100)>122:
                targ_y = -100
        else:
                targ_y = 100


def shoot(cur_x,cur_y,tar_x,tar_y):
    #Turn turret to tar x tary
    #shoot

    distance = getDistance(cur_x,cur_y,tar_x,tar_y)

    if (distance < 50):
        direction = getAng(cur_x, cur_y, targ_x, targ_y)
        GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {'Amount': direction})
        GameServer.sendMessage(ServerMessageTypes.FIRE)


#id 556


        
                                
# Main loop - read game messages, ignore them and randomly perform actions
targ_x = 0
targ_y = 0
snitch_present = 0
bank = 0
busy = False
nearestHPack = [0,0]
nearestAPack = [0,0]
ammo = 10
health = 5
nearest_enemy = 0
cur_x = 0
cur_y = 0
while True:
        data = GameServer.readMessage() 
        GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

        if not(data == None):
                print(data)
                if(len(data)>1):
                        print(data)
                        if (data["Name"] == "HIVEbot"):
                                HiveID = data["Id"]
                                cur_x= data["X"]
                                cur_y = data["Y"]
                                ammo = data["Ammo"]
                                health = data["Health"]
                                if(cur_y> 100 or cur_y<-100):
                                        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                                        bank = False
                                
                        if len(data) == 1 and data["Id"] == HiveID:
                                GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING,{'Amount':getAng(cur_x,cur_y,0,100)})
                                time.sleep(15)
                                targ_x = 0
                                targ_y = 0
                        if not(nearest_enemy == 0):
                                if nearest_enemy["Health"] == 0:
                                        print("HERERERERERERERERERRERERERERERERERER")
                                        bank = True
                                        nearest_enemy["Health"] = 5
                                        GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING,{'Amount':getAng(cur_x,cur_y,0,100)})
                                        time.sleep(15)
                                        targ_x = 0
                                        targ_y = 0
                        if data["Type"] == "Tank" and not(data["Name"] == "HIVEbot"):
                                if not((nearest_enemy) == 0):
                                        if getDistance(cur_x,cur_y,nearest_enemy["X"],nearest_enemy["X"])>getDistance(cur_x,cur_y,data["X"],data["Y"]):
                                                nearest_enemy = data
                                else:
                                        nearest_enemy = data
                        if data["Type"] == "AmmoPickup":
                                nearestAPack[0] = (data["X"])
                                nearestAPack[1] = (data["Y"])
                                print(nearestAPack)
                        if data["Type"] == "HealthPickup":
                                nearestHPack[0] = (data["X"])
                                nearestHPack[1] =(data["Y"])

        if bank == True:
                GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING,{'Amount':getAng(cur_x,cur_y,0,100)})
                goGoals(cur_x,cur_y)
        else:
                if ammo < 4 and health > 1:
                        if len(nearestAPack) > 0:
                                targ_x = nearestAPack[0]
                                targ_y = nearestAPack[1]
                elif not(nearest_enemy == 0):
                        if evalChance({"Health":health,"Ammo":ammo},nearest_enemy):
                                targ_x = nearest_enemy["X"]
                                targ_y = nearest_enemy["Y"]
                else:
                        if len(nearestHPack) > 0:
                                targ_x = nearestHPack[0]
                                targ_y = nearestHPack[1]
        print(targ_x,targ_y)
        
             
        GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING,{'Amount':getAng(cur_x,cur_y,targ_x,targ_y)})                
        GameServer.sendMessage(ServerMessageTypes.FIRE)                       







	


    
