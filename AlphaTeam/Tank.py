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

    def __init__(self, ServerDeetz, Team, Name):
        self.name = Team + ":" + Name
        self.GameServer = ServerComms(ServerDeetz.hostname, ServerDeetz.port)
        # Spawn our tank
        # logging.info("Creating tank with name '{}'".format(args.name))
        self.GameServer.sendMessage(
            ServerMessageTypes.CREATETANK, {'Name': self.name})

    def evalChance(self, HDat, ODat):
        HHealth = HDat["Health"]
        OHealth = ODat["Health"]

        HAmmo = HDat["Ammo"]
        OAmmo = ODat["Ammo"]

        if HAmmo < OHealth:
            return(False)
        elif HHealth < OAmmo and HHealth == 1 and OHealth > 1:
            return(False)
        else:
            return(True)

    def goGoals(self):
        self.target[0] = 0
        if getDistance(self.pos, p2=(0, 100)) > 122:
            self.target[1] = -100
        else:
            self.target[1] = 100

    #turns bot to point towards x,y
    def turnTo(self, point):
        self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING,
            {
                'Amount': getAng(self.pos, point)
            })
 
    def update(self):
        data = self.GameServer.readMessage()
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

        if data and len(data) > 1 and data["Name"] == self.name:
            self.HiveID = data["Id"]
            self.pos = (data["X"], data["Y"])
            self.ammo = data["Ammo"]
            self.health = data["Health"]
            if(self.pos[1] > 100 or self.pos[1] < -100):
                self.bank = False

            if len(data) == 1 and data["Id"] == self.HiveID:
                self.turnTo((0, 100))
                self.target = (0,0)

                if not(self.nearest_enemy == 0) and self.nearest_enemy["Health"] == 0:
                    print("HERERERERERERERERERRERERERERERERERER")
                    self.bank = True
                    self.nearest_enemy["Health"] = 5

            if data["Type"] == "Tank" and not(data["Name"] == self.name):
                if not((self.nearest_enemy) == 0):
                    p1 = self.pos

                    enemy = self.nearest_enemy
                    p2 = (enemy["X"], enemy["Y"])
                    d1 = getDistance(p1, p2)

                    p2 = (data["X"], data["Y"])
                    d2 = getDistance(p1, p2)
                    
                    if d1 > d2:
                        self.nearest_enemy = data
                else:
                    self.nearest_enemy = data
                if data["Type"] == "AmmoPickup":
                    self.nearestAPack = (data["X"], data["Y"])
                    print(self.nearestAPack)
                if data["Type"] == "HealthPickup":
                    self.nearestHPack = (data["X"], data["Y"])

        if self.bank == True:
            self.turnTo(0,100)
            self.goGoals()
        else:
            if self.ammo < 4 and self.health > 1 and len(self.nearestAPack) > 0:
                self.target = self.nearestAPack
            elif not(self.nearest_enemy == 0) and self.evalChance({"Health": self.health, "Ammo": self.ammo}, self.nearest_enemy):
                self.target = self.nearest_enemy
            elif len(self.nearestHPack) > 0:
                self.target = self.nearestHPack
        print(self.target)

        self.turnTo(self.target)
        self.GameServer.sendMessage(ServerMessageTypes.FIRE)
