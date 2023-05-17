from Classes.organism import Organism
from abc import abstractmethod, ABC
import random
from Classes.collisionResults import CollisionResults


class Plant(Organism, ABC):
    def TakeAction(self):
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
        self.world.organisms.remove(self)
        return CollisionResults.PlantIsEaten

    def IsAttackRepealed(self):
        return False

    def FindFreePlace(self):
        freeSpace = []
        if self.y > 0:
            if self.world.IsFieldEmpty(self.x, self.y - 1):
                freeSpace.append([self.x, self.y - 1])
        if self.x > 0:
            if self.world.IsFieldEmpty(self.x - 1, self.y):
                freeSpace.append([self.x - 1, self.y])
        if self.y < self.world.height:
            if self.world.IsFieldEmpty(self.x, self.y + 1):
                freeSpace.append([self.x, self.y + 1])
        if self.x < self.world.width:
            if self.world.IsFieldEmpty(self.x + 1, self.y):
                freeSpace.append([self.x + 1, self.y])

        return freeSpace
