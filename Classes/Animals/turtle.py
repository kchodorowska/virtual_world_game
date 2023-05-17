from Classes.Organisms.animal import Animal
from Classes.world import *
from Classes.collisionResults import CollisionResults


class Turtle(Animal):
    def __init__(self, positionX, positionY, world):
        super().__init__(2, 1, positionX, positionY, world, PhotoImage(file="Img/zolw.png"), "Turtle")

    def TakeAction(self):
        stay = random.randint(0, 3)
        if stay == 0:
            Animal.TakeAction(self)
        self.age += 1
        self.actionMade = True

    def Collision(self, attacker):
        if type(attacker) == type(self):
            freeSpace = self.FindFreePlace() + attacker.FindFreePlace()

            if len(freeSpace) != 0:
                self.world.AddLogInfo("Pair of " + self.name + "s" + " made a baby")
                newOrganismPosition = random.randint(0, len(freeSpace) - 1)
                x = freeSpace[newOrganismPosition][0]
                y = freeSpace[newOrganismPosition][1]
                self.world.organisms.append(attacker(x, y, self.world))

            return CollisionResults.AnimalCreation
        else:
            if self.IsAttackReflected(attacker):
                return CollisionResults.AttackedReflects
            if attacker.IsAttackRepealed():
                self.world.AddLogInfo(attacker.name + " tried to attack " + self.name + ", but attacker escaped")
                return CollisionResults.AttackerEscapes
            if attacker.strength >= self.strength:
                self.world.AddLogInfo(attacker.name + " has just murdered " + self.name)
                self.world.organisms.remove(self)
                return CollisionResults.AttackedDies
            else:
                self.world.AddLogInfo(self.name + " has just murdered " + attacker.name)
                self.world.organisms.remove(attacker)
                return CollisionResults.AttackerDies

    def IsAttackReflected(self, attacker):
        if attacker.strength < 5:
            return True
        else:
            return False
