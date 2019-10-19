from Tank import *
import logging


class Team:

    tanks = []
    teamKnowledge = {}

    def __init__(self, servDeetz, teamName, tankNames):
        for tankName in tankNames:
            self.tanks.append(Tank(servDeetz, teamName, tankName))

    def update(self):
        for tank in self.tanks:
            tank.update()

    def getTeamKnowledge(self):
        for tank in self.tanks:
            currentData = tank.getInfo()
            if currentData and len(currentData) > 1:
                self.teamKnowledge[currentData["Id"]] = currentData
                logging.info(self.teamKnowledge)

