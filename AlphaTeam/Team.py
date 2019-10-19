from Tank import *

class Team:

	tanks = []

	def __init__(self, servDeetz, teamName, tankNames):
		for tankName in tankNames:
			self.tanks.append(Tank(servDeetz, teamName, tankName))

	def update(self):
		for tank in self.tanks:
			tank.update()
