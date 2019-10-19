from Tank import *
import logging
import datetime


class Team:

    tanks = []
    teamKnowledge = {}
    entityTypes = {}

    def __init__(self, servDeetz, teamName, tankNames):
        self.teamName = teamName
        for tankName in tankNames:
            self.tanks.append(Tank(servDeetz, teamName, tankName))

    def update(self):
        for tank in self.tanks:
            tank.update()

    def getTeamKnowledge(self):
        self.findNearestTank(0,0)
        for tank in self.tanks:
            currentData = tank.getInfo()
            #currentTime = time.ctime(time.time()) ## 'time': 'Sat Oct 19 15:51:23 2019'}
            #currentTime = time.localtime(time.time()) ## 'time': time.struct_time(tm_year=2019, tm_mon=10, tm_mday=19, tm_hour=15, tm_min=48, tm_sec=32, tm_wday=5, tm_yday=292, tm_isdst=1)}}
            currentTime = datetime.datetime.now()
            if currentData:
                currentData["Time"] = currentTime
                self.teamKnowledge[currentData["Id"]] = currentData

                if self.teamName not in currentData["Name"]:
                    self.entityTypes[currentData["Id"]] = currentData["Type"]

                #logging.info(self.teamKnowledge)
                #logging.info(self.entityTypes)


    def findNearestTank(self,x,y):
        tankIDs = []
        currestPos = (x,y)
        closestTank = self.teamKnowledge[0]
        for entity in self.entityTypes:
            if entity[value] == "Tank":
                tankIDs.append(entity[key])

        for entry in self.teamKnowledge:
            closestTankCoord = (closestTank["X"], closestTank["Y"])
            # currentTime = datetime.datetime.now()
            # if currentTime - entry["time"] > 5:
            #     del self.teamKnowledge[entry]

            if entry["Id"] in tankIDs:
                currentTank = (entry["X"], entry["Y"])
                if getDistance(currentPos, currentTank) < getDistance(currentPos, closestTankCoord):
                    closestTank = entry

        print(closestTank)
        return closestTank

    def findNearestAmmo(x,y):
        return closestAmmo


    def findNearestHealth(x,y):
        return closestHealth

