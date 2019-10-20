from Tank import *
import logging
import datetime

class Team:

    tanks = []
    teamKnowledge = {}
    ammoIDs = set()
    tankIDs = set()
    healthIDs = set()
    snitchIDs = set()

    def __init__(self, servDeetz, teamName, tankNames):
        self.teamName = teamName
        for tankName in tankNames:
            self.tanks.append(Tank(servDeetz, self, tankName))

    def getName(self):
        return self.teamName

    def update(self):
        for tank in self.tanks:
            tank.update()

    def getTeamKnowledge(self):
        for tank in self.tanks:
            currentData = tank.getInfo()
            # currentTime = time.ctime(time.time()) ## 'time': 'Sat Oct 19 15:51:23 2019'}
            # currentTime = time.localtime(time.time()) ## 'time': time.struct_time(tm_year=2019, tm_mon=10, tm_mday=19, tm_hour=15, tm_min=48, tm_sec=32, tm_wday=5, tm_yday=292, tm_isdst=1)}}
            currentTime = datetime.datetime.now()
            if currentData:
                currentData["Time"] = currentTime
                self.teamKnowledge[currentData["Id"]] = currentData

                if currentData["Name"].startswith(self.teamName) == False:
                    if currentData["Type"] == "Tank":
                        self.tankIDs.add(currentData["Id"])
                    elif currentData["Type"] == "AmmoPickup":
                        self.ammoIDs.add(currentData["Id"])
                    elif currentData["Type"] == "HealthPickup":
                        self.healthIDs.add(currentData["Id"])
                    elif currentData["Type"] == "Snitch":
                        self.snitchIDs.add(currentData["Id"])

                # logging.info(self.teamKnowledge)
                # logging.info(self.entityTypes)

    def findNearestFromSet(self, idSet, currentPos):
        if len(idSet) == 0:
            return None

        closestEnt = None
        closestEntCoord = (-10000, -100000)

        for ID in idSet:
            entry = self.teamKnowledge[ID]
            currentTime = datetime.datetime.now()
            if currentTime - entry["Time"] > datetime.timedelta(seconds=6):
                continue

            currentEnt = (entry["X"], entry["Y"])
            if getDistance(currentPos, currentEnt) < getDistance(currentPos, closestEntCoord):
                closestEntCoord = currentEnt
                closestEnt = entry

        return closestEnt

    def findNearestTank(self,currentPos):
        return self.findNearestFromSet(self.tankIDs, currentPos)

    def findNearestAmmo(self, currentPos):
        return self.findNearestFromSet(self.ammoIDs, currentPos)

    def findNearestHealth(self,currentPos):
        return self.findNearestFromSet(self.healthIDs, currentPos)
