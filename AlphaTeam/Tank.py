from Server import *
from Utils import *

class Tank:

    target = (0,0)
    snitch_present = 0
    bank = 0
    busy = False
    nearestHPack = (0, 0)
    nearestAPack = (0, 0)
    ammo = 10
    health = 5
    nearest_enemy = 0
    pos = (0,0)

    STATES = ['PATROL','ATTACK', 'GOHEALTH','GOAMMO', 'BANK']  # fill this in as i figure out required states
    state = 'PATROL'

    def __init__(self, ServerDeetz, Team, Name):
        self.name = Team + ":" + Name
        self.state = 'IDLE'
        self.GameServer = ServerComms(ServerDeetz.hostname, ServerDeetz.port)

        # Spawn our tank with starting state
        # logging.info("Creating tank with name '{}'".format(args.name))
        self.GameServer.sendMessage(
            ServerMessageTypes.CREATETANK, {'Name': self.name})

    def evalChance(self, player, enemy):
        myHealth = player["Health"]
        enemyHealth = enemy["Health"]

        myAmmo = player["Ammo"]
        enemyAmmo = enemy["Ammo"]

        if myAmmo < enemyHealth:
            return(False)
        elif myHealth < enemyAmmo and myHealth == 1 and enemyHealth > 1:
            return(False)
        else:
            return(True)

    def shoot(self):
        self.GameServer.sendMessage(ServerMessageTypes.FIRE)

    def getInfo(self):
        return self.GameServer.readMessage()

    def goGoals(self):
        if getDistance(self.pos, p2=(0, 100)) > 122:
            self.target = (0, -100)
        else:
            self.target[1] = (0, 100)
        self.turnTo(target)

    def updateNearestEnemy(self, data):
        if self.nearest_enemy != 0:
            player = self.pos
            currEnemy = (self.nearest_enemy["X"], self.nearest_enemy["Y"])
            newEnemy = (data["X"], data["Y"])
            if getDistance(player, currEnemy) > getDistance(player, newEnemy):
                self.nearest_enemy = data
        else:
            self.nearest_enemy = data

    def pickTarget(self):
        if self.ammo < 4 and self.health > 1 and len(self.nearestAPack) > 0:
            self.target = self.nearestAPack
        elif self.nearest_enemy != 0 and self.evalChance({"Health": self.health, "Ammo": self.ammo}, self.nearest_enemy):
            self.target = self.nearest_enemy
        elif len(self.nearestHPack) > 0:
            self.target = self.nearestHPack
    #pickTarget
    #shoot at
    #follow snitch
    #turns bot to point towards x,y
    def turnTo(self, point):

        self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING,
            {
                'Amount': getAng(self.pos, point)
            })

    #will select the target
    def selectTarget(self):
        if self.ammo < 4 and self.health > 1 and len(self.nearestAPack) > 0:
            self.target = self.nearestAPack
        elif self.nearest_enemy != 0 and self.evalChance({"Health": self.health, "Ammo": self.ammo}, self.nearest_enemy):
            self.target = self.nearest_enemy
        elif len(self.nearestHPack) > 0:
            self.target = self.nearestHPack

    def setState(self, state):
        if state not in self.STATES:
            return
        else:
            self.state = state
 
    def update(self):
        data = self.getInfo()
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

        if data and len(data) > 1 and data["Name"] == self.name:
            self.AlphaID = data["Id"]
            self.pos = (data["X"], data["Y"])
            self.ammo = data["Ammo"]
            self.health = data["Health"]

            if(self.pos[1] > 100 or self.pos[1] < -100):
                self.setState('PATROL')

            if len(data) == 1 and data["Id"] == self.AlphaID:
                self.turnTo((0, 100))
                self.target = (0,0)

                if not(self.nearest_enemy == 0) and self.nearest_enemy["Health"] == 0:
                    print("HERERERERERERERERERRERERERERERERERER")
                    self.setState('BANK')
                    self.nearest_enemy["Health"] = 5

            if data["Type"] == "Tank" and data["Name"] != self.name:
                self.updateNearestEnemy(data)
            if data["Type"] == "AmmoPickup":
                self.nearestAPack = (data["X"], data["Y"])
            if data["Type"] == "HealthPickup":
                self.nearestHPack = (data["X"], data["Y"]

        if self.state == 'BANK':
            self.turnTo(0,100)
            self.goGoals()
        else:
            self.selectTarget()

        self.turnTo(self.target)
        self.shoot()
