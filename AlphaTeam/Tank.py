from Server import *
from Utils import *

class Tank:

    target = (0,0)
    nearestHPack = (0, 0)
    nearestAPack = (0, 0)
    snitchLocation = (0,0)
    ammo = 10
    health = 5
    nearest_enemy = None
    pos = (0,0)

    stateLock = False
    STATES = ['PATROL','ATTACK', 'GOHEALTH','GOAMMO', 'BANK', 'SNITCH']  # fill this in as i figure out required states
    state = 'PATROL'

    def __init__(self, ServerDeetz, ourTeam, Name):

        self.behaviours = {
            "PATROL": self.patrol,
            "ATTACK": self.attack,
            "GOHEALTH": self.goHealth,
            "GOAMMO": self.goAmmo,
            "BANK": self.bank,
            "SNITCH": self.snitch
        }

        self.name = ourTeam.getName() + ":" + Name
        self.team = ourTeam
        self.GameServer = ServerComms(ServerDeetz.hostname, ServerDeetz.port)

        # Spawn our tank with starting state
        # logging.info("Creating tank with name '{}'".format(args.name))
        self.GameServer.sendMessage(
            ServerMessageTypes.CREATETANK, {'Name': self.name})

    def evalChance(self, player, enemy):
        if enemy == None:
            return False

        myHealth = player["Health"]
        enemyHealth = enemy["Health"]
        myAmmo = player["Ammo"]
        enemyAmmo = enemy["Ammo"]

        if getDistance(self.pos, (self.nearest_enemy['X'], self.nearest_enemy['Y'])) > 50:
            return False

        if myAmmo < enemyHealth:
            return False
        elif myHealth < enemyAmmo and myHealth == 1 and enemyHealth > 1:
            return False
        else:
            return True

    def goGoals(self):
        if getDistance(self.pos, p2=(0, 100)) > 122:
            self.target = (0, -100)
        else:
            self.target = (0, 100)
        self.turnTo(self.target)
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

    #turns bot to point towards x,y
    def turnTurret(self, point):

        self.GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING,
            {
                'Amount': getAng(self.pos, point)
            })

    #turns bot to point towards x,y
    def turnTo(self, point):
        self.GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING,
            {
                'Amount': getAng(self.pos, point)
            })

    def setState(self, state):
        if self.stateLock:
            print("{}".format(self.name))
            print("State locked")
            return
        if state not in self.STATES:
            print("{} not in states".format(state))
        else:
            if state == "BANK" or state == "SNITCH":
                self.stateLock = True
            print("{}".format(self.name))
            print("Transition: {} => {}".format(self.state, state))
            self.state = state


    def snitch(self):
        snitch = self.team.findNearestSnitch(self.pos)
        if snitch:
            self.snitchLocation = (snitch["X"], snitch["Y"])
        self.turnTo(self.snitchLocation)
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

    def patrol(self):
        self.turnTo((0,0))
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLETURRETRIGHT)
        self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

    def attack(self):
        self.GameServer.sendMessage(ServerMessageTypes.STOPTURRET)
        if self.nearest_enemy:
            print("{} attack -> {}".format(self.name, self.nearest_enemy['Name']))
            self.target = (self.nearest_enemy['X'], self.nearest_enemy['Y'])
            self.GameServer.sendMessage(ServerMessageTypes.STOPMOVE)
            self.turnTurret(self.target)
            self.shoot()
        else:
            self.turnTo((0,0))
            self.setState("PATROL")


    def goHealth(self):
        hpack = self.team.findNearestHealth(self.pos)
        if hpack:
            self.nearestHPack = (hpack["X"],hpack["Y"])
            self.target = self.nearestHPack
            self.turnTo(self.target)
            self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)
        else:
            self.turnTo((0,0))
            self.setState("PATROL")

    def goAmmo(self):
        apack = self.team.findNearestAmmo(self.pos)
        if apack:
            self.nearestAPack = (apack["X"],apack["Y"])
            self.target = self.nearestAPack
            self.turnTo(self.target)
            self.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)
        else:
            self.turnTo((0,0))
            self.setState("PATROL")

    def bank(self):
        #TODO:Lock this state
        self.goGoals()

    def shoot(self):
        self.GameServer.sendMessage(ServerMessageTypes.FIRE)

    #NOTE: need to work out how to transition to attack state
    def getInfo(self):
        messageType, messagePayload = self.GameServer.readMessage()

        #if we pick up snitch, ammo, health or get a kill set state accordingly
        if messageType == ServerMessageTypes.SNITCHPICKUP:
            self.stateLock = False
            if messagePayload['Id'] == self.AlphaID:
                self.setState("BANK")
            else:
                self.setState("ATTACK")
                # TODO: Implement this
                # if not friendly
                #       Attack payload id
                # else
                #       Defend teammate with snitch (Low priority)

        if messageType == ServerMessageTypes.KILL:
            self.setState("BANK")
        elif messageType == ServerMessageTypes.HEALTHPICKUP \
            or messageType == ServerMessageTypes.AMMOPICKUP:
                self.nearestHPack = (0, 0)
                self.nearestAPack = (0, 0)
                self.setState("PATROL")
        elif messageType == ServerMessageTypes.ENTEREDGOAL \
            or messageType == ServerMessageTypes.DESTROYED:
            self.stateLock = False
            self.setState("PATROL")

        if messageType == ServerMessageTypes.SNITCHAPPEARED:
            self.setState("SNITCH")

        self.nearest_enemy = self.team.findNearestTank(self.pos)
        #if recieving an object update
        if messageType == ServerMessageTypes.OBJECTUPDATE:
            #if data is about the tank
            if messagePayload["Name"] == self.name:

                #update the class attributes
                self.AlphaID = messagePayload["Id"]
                self.pos = (messagePayload["X"], messagePayload["Y"])
                self.ammo = messagePayload["Ammo"]
                self.health = messagePayload["Health"]


                #transition to health/ammo states if either are low
                if self.ammo < 4 and self.health > 1:
                    self.setState("GOAMMO")
                elif self.nearest_enemy != 0 and self.evalChance({"Health": self.health, "Ammo": self.ammo}, self.nearest_enemy):
                    self.setState("ATTACK")
                elif self.health == 1:
                    self.setState("GOHEALTH")

            return messagePayload
        else:
            return None

    def update(self):
        if(self.pos[1] > 100 or self.pos[1] < -100):
            self.setState('PATROL')
        behaviour = self.behaviours[self.state]
        behaviour()
