from Server import *
from Utils import *

class Tank:

    target = (0,0)
    snitch_present = 0
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

        self.behaviours = {
            "PATROL": self.patrol,
            "ATTACK": self.attack,
            "GOHEALTH": self.goHealth,
            "GOAMMO": self.goAmmo,
            "BANK": self.bank
        }

        self.name = Team + ":" + Name
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

    def goGoals(self):
        if getDistance(self.pos, p2=(0, 100)) > 122:
            self.target = (0, -100)
        else:
            self.target = (0, 100)
        self.turnTo(self.target)

    def updateNearestEnemy(self, data):
        if self.nearest_enemy != 0:
            player = self.pos
            currEnemy = (self.nearest_enemy["X"], self.nearest_enemy["Y"])
            newEnemy = (data["X"], data["Y"])
            if getDistance(player, currEnemy) > getDistance(player, newEnemy):
                self.nearest_enemy = data
        else:
            self.nearest_enemy = data

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
            self.target = (self.nearest_enemy['X'], self.nearest_enemy['Y'])
        elif len(self.nearestHPack) > 0:
            self.target = self.nearestHPack

    # bank = true when called by bank state update
    def setState(self, state, bank=False):
        if not bank:
            if state not in self.STATES:
                return
            else:
                print("Transition: {} => {}".format{self.state, state})
                self.state = state

    def patrol(self):
        pass

    def attack(self):
        pass

    def goHealth(self):
        self.target = self.nearestHPack
        self.turnTo(self.target)

    def goAmmo(self):
        self.target = self.nearestAPack
        self.turnTo(self.target)

    def bank(self):
        # Lock this state
        #TODO: Go to closest goal
        self.turnTo((0, 100))
        self.target = (0,0)
        #If we are killed or score go to patrol

    def shoot(self):
        self.GameServer.sendMessage(ServerMessageTypes.FIRE)

    #NOTE: need to work out how to transition to attack state
    def getInfo(self):
        messageType, messagePayload = self.GameServer.readMessage()

        #if we pick up snitch, ammo, health or get a kill set state accordingly
        if messageType == ServerMessageTypes.SNITCHPICKUP:
            if messagePayload['Id'] == self.AlphaID:
                self.setState("BANK")
            else:
                # if not friendly
                #       Attack payload id
                # else
                #       Defend teammate with snitch (Low priority)
                continue
                
        if messageType == ServerMessageTypes.KILL:
            self.setState("BANK")
        elif messageType == ServerMessageTypes.HEALTHPICKUP or messageType == ServerMessageTypes.AMMOPICKUP:
            self.setState("PATROL")

        #if recieving an object update
        if messageType == ServerMessageTypes.OBJECTUPDATE:

            #if data is about the tank
            if messagePayload["name"] = self.name:    
                
                #update the class attributes
                self.AlphaID = messagePayload["Id"]
                self.pos = (messagePayload["X"], messagePayload["Y"])
                self.ammo = messagePayload["Ammo"]
                self.health = messagePayload["Health"]

                #transition to health/ammo states if either are low
                if self.health <= 2:
                    self.setState("GOHEALTH")
                if self.ammo <= 2:
                    self.setState("GOAMMO")

        return messagePayload

    def update(self):
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

        if data and len(data) > 1:
            if :

                if(self.pos[1] > 100 or self.pos[1] < -100):
                    self.setState('PATROL')

                if len(data) == 1 and data["Id"] == self.AlphaID:
                    

        behaviour = self.behaviours[self.state]
        behaviour()

        if self.state == 'BANK':
            self.turnTo((0,100))
            self.goGoals()
        else:
            self.selectTarget()

            self.turnTo(self.target)
            self.shoot()
