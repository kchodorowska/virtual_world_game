from Classes.Organisms.plant import Plant
from Classes.world import *
from Classes.collisionResults import CollisionResults


class SosnowskysHogweed(Plant):
    def __init__(self, positionX, positionY, world):
        super().__init__(10, 0, positionX, positionY, world, PhotoImage(file="Img/barszcz.png"), "Sosnowsky's Hogweed")

    def TakeAction(self):
        immediateNeighbor = 0
        possibleNeighbor=[]
        if self.y > 0:
            possibleNeighbor.append([self.x, self.y - 1])
        if self.x > 0:
            possibleNeighbor.append([self.x - 1, self.y])
        if self.y < self.world.height:
            possibleNeighbor.append([self.x, self.y + 1])
        if self.x < self.world.width:
            possibleNeighbor.append([self.x + 1, self.y])
        for neighbor in possibleNeighbor:
            for organism in self.world.organisms:
                if organism.x == neighbor[0] and organism.y == neighbor[1]:
                    if type(organism) != type(self) and organism.name != "Cybersheep":
                        self.world.AddLogInfo(self.name + " poisoned " + organism.name)
                        self.world.organisms.remove(organism)
                    break

        freePlaces = []
        sow = random.randint(0, 99)  #15%
        if sow < 15:
            freePlaces = self.FindFreePlace()
            if len(freePlaces) != 0:
                newOrganismPosition = random.randint(0, len(freePlaces) - 1)
                x = freePlaces[newOrganismPosition][0]
                y = freePlaces[newOrganismPosition][1]
                self.world.organisms.append(type(self)(x, y, self.world))
                self.world.AddLogInfo(self.name + " spread 1 time")
        self.age += 1
        self.actionMade = True

    def Collision(self, attacker):
        self.world.AddLogInfo(attacker.name + " has just eaten " + self.name)
        if (attacker.name == "Cybersheep"):
            self.world.organisms.remove(self)
            return CollisionResults.PlantIsEaten
        else:
            self.world.AddLogInfo("and " + self.name + " poisoned " + attacker.name)
            self.world.organisms.remove(attacker)
            return CollisionResults.PlantKills
