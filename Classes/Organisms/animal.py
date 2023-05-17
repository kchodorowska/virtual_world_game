import random
from abc import abstractmethod, ABC
from Classes.organism import Organism
from Classes.collisionResults import CollisionResults


class Animal(Organism, ABC):
    def TakeAction(self):
        possibleMoves = self.FindPlaceToMove()
        move = random.randint(0, len(possibleMoves) - 1)
        collisionResult = 0

        for organism in self.world.organisms:
            if organism.x == possibleMoves[move][0] and organism.y == possibleMoves[move][1]:
                collisionResult = organism.Collision(self)
                break

        if collisionResult == CollisionResults.AttackedReflects or collisionResult == CollisionResults.AnimalCreation:
            self.age += 1
            self.actionMade = True
        if collisionResult == CollisionResults.AttackedDies or collisionResult == CollisionResults.AttackedEscapes or \
                collisionResult == CollisionResults.PlantIsEaten or collisionResult == 0:
            self.age += 1
            self.x = possibleMoves[move][0]
            self.y = possibleMoves[move][1]
            self.actionMade = True

    def Collision(self, attacker):
        if type(attacker) == type(self):
            freeSpace = self.FindFreePlace() + attacker.FindFreePlace()

            if len(freeSpace) != 0:
                self.world.AddLogInfo("Pair of " + self.name + "s" + " made a baby")
                newOrganismPosition = random.randint(0, len(freeSpace) - 1)
                x = freeSpace[newOrganismPosition][0]
                y = freeSpace[newOrganismPosition][1]
                self.world.organisms.append(type(attacker)(x, y, self.world))
            return CollisionResults.AnimalCreation

        else:
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

    def FindPlaceToMove(self):
        possibleMoves = []
        if self.y > 0:
            possibleMoves.append([self.x, self.y-1])
        if self.x > 0:
            possibleMoves.append([self.x-1, self.y])
        if self.y < self.world.height:
            possibleMoves.append([self.x, self.y+1])
        if self.x < self.world.width:
            possibleMoves.append([self.x+1, self.y])

        return possibleMoves
