from Server import *
from Utils import *


class Tank:

    targ_x = 0
    targ_y = 0
    snitch_present = 0
    bank = 0
    busy = False
    nearestHPack = [0, 0]
    nearestAPack = [0, 0]
    ammo = 10
    health = 5
    nearest_enemy = 0
    cur_x = 0
    cur_y = 0

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
        self.targ_x = 0
        if getDistance(self.cur_x, self.cur_y, 0, 100) > 122:
            self.targ_y = -100
        else:
            self.targ_y = 100

    def update(self):
        data = self.GameServer.readMessage()
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

        if data and len(data) > 1 and data["Name"] == self.name:
            self.HiveID = data["Id"]
            self.cur_x = data["X"]
            self.cur_y = data["Y"]
            self.ammo = data["Ammo"]
            self.health = data["Health"]
            if(self.cur_y > 100 or self.cur_y < -100):
                self.bank = False

            if len(data) == 1 and data["Id"] == self.HiveID:
                self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
                    'Amount': getAng(self.cur_x, self.cur_y, 0, 100)})
                self.targ_x = 0
                self.targ_y = 0
                if not(self.nearest_enemy == 0) and self.nearest_enemy["Health"] == 0:
                    print("HERERERERERERERERERRERERERERERERERER")
                    self.bank = True
                    self.nearest_enemy["Health"] = 5
                    GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
                        'Amount': getAng(self.cur_x, self.cur_y, 0, 100)})
                    self.targ_x = 0
                    self.targ_y = 0
            if data["Type"] == "Tank" and not(data["Name"] == self.name):
                if not((self.nearest_enemy) == 0):
                    x1 = self.cur_x
                    y1 = self.cur_y
                    x2 = self.nearest_enemy["X"]
                    y2 = self.nearest_enemy["Y"]
                    d1 = getDistance(x1, y1, x2, y2)

                    x2 = data["X"]
                    x2 = data["Y"]
                    d2 = getDistance(x1, y1, x2, y2)
                    
                    if d1 > d2:
                        self.nearest_enemy = data
                else:
                    self.nearest_enemy = data
                if data["Type"] == "AmmoPickup":
                    self.nearestAPack[0] = (data["X"])
                    self.nearestAPack[1] = (data["Y"])
                    print(self.nearestAPack)
                if data["Type"] == "HealthPickup":
                    self.nearestHPack[0] = (data["X"])
                    self.nearestHPack[1] = (data["Y"])

        if self.bank == True:
            self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
                'Amount': getAng(self.cur_x, self.cur_y, 0, 100)})
            self.goGoals()
        else:
            if self.ammo < 4 and self.health > 1 and len(self.nearestAPack) > 0:
                self.targ_x = self.nearestAPack[0]
                self.targ_y = self.nearestAPack[1]
            elif not(self.nearest_enemy == 0) and self.evalChance({"Health": self.health, "Ammo": self.ammo}, self.nearest_enemy):
                self.targ_x = self.nearest_enemy["X"]
                self.targ_y = self.nearest_enemy["Y"]
            elif len(self.nearestHPack) > 0:
                self.targ_x = self.nearestHPack[0]
                self.targ_y = self.nearestHPack[1]
        print(self.targ_x, self.targ_y)

        self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
            'Amount': getAng(self.cur_x, self.cur_y, self.targ_x, self.targ_y)})
        self.GameServer.sendMessage(ServerMessageTypes.FIRE)
