from Tank import *

class Team:
<<<<<<< HEAD

=======
	
>>>>>>> a924e0971f1f75c319b2919085f15743b5caed3c
	tanks = []

	def __init__(self, servDeetz, teamName, tankNames):
		for tankName in tankNames:
			self.tanks.append(Tank(servDeetz, teamName, tankName))

	def update(self):
		for tank in self.tanks:
			tank.update()
	


