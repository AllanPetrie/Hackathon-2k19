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

    def __init__(self, Team, Name, ServerDeetz):
        self.name = Team + ":" + Name
        self.GameServer = ServerComms(ServerDeetz.hostname, ServerDeetz.port)
        # Spawn our tank
        # logging.info("Creating tank with name '{}'".format(args.name))
        self.GameServer.sendMessage(
            ServerMessageTypes.CREATETANK, {'Name': self.name})

    def evalChance(HDat, ODat):
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

    def goGoals(self, cur_x, cur_y):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        targ_x = 0
        if getDistance(cur_x, cur_y, 0, 100) > 122:
            targ_y = -100
        else:
            targ_y = 100

    def update(self):
        data = self.GameServer.readMessage()
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

        if not(data == None):
            print(data)
            if(len(data) > 1):
                print(data)
                if (data["Name"] == self.name):
                    HiveID = data["Id"]
                    self.cur_x = data["X"]
                    self.cur_y = data["Y"]
                    self.ammo = data["Ammo"]
                    self.health = data["Health"]
                    if(cur_y > 100 or cur_y < -100):
                        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                        bank = False

                if len(data) == 1 and data["Id"] == HiveID:
                    self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
                        'Amount': getAng(self.cur_x, self.cur_y, 0, 100)})
                    self.targ_x = 0
                    self.targ_y = 0
                if not(nearest_enemy == 0):
                    if nearest_enemy["Health"] == 0:
                        print("HERERERERERERERERERRERERERERERERERER")
                        bank = True
                        nearest_enemy["Health"] = 5
                        GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
                            'Amount': getAng(cur_x, cur_y, 0, 100)})
                        targ_x = 0
                        targ_y = 0
                if data["Type"] == "Tank" and not(data["Name"] == "HIVEbot"):
                    if not((nearest_enemy) == 0):
                        if getDistance(cur_x, cur_y, nearest_enemy["X"], nearest_enemy["X"]) > getDistance(cur_x, cur_y, data["X"], data["Y"]):
                            nearest_enemy = data
                    else:
                        nearest_enemy = data
                if data["Type"] == "AmmoPickup":
                    nearestAPack[0] = (data["X"])
                    nearestAPack[1] = (data["Y"])
                    print(nearestAPack)
                if data["Type"] == "HealthPickup":
                    nearestHPack[0] = (data["X"])
                    nearestHPack[1] = (data["Y"])

        if bank == True:
            self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
                'Amount': getAng(self.cur_x, self.cur_y, 0, 100)})
            self.goGoals(cur_x, cur_y)
        else:
            if ammo < 4 and health > 1:
                if len(nearestAPack) > 0:
                    targ_x = nearestAPack[0]
                    targ_y = nearestAPack[1]
            elif not(nearest_enemy == 0):
                if evalChance({"Health": health, "Ammo": ammo}, nearest_enemy):
                    targ_x = nearest_enemy["X"]
                    targ_y = nearest_enemy["Y"]
            else:
                if len(nearestHPack) > 0:
                    targ_x = nearestHPack[0]
                    targ_y = nearestHPack[1]
        print(targ_x, targ_y)

        self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {
            'Amount': getAng(cur_x, cur_y, targ_x, targ_y)})
        self.GameServer.sendMessage(ServerMessageTypes.FIRE)
