from Classes.Organisms.animal import Animal
from Classes.world import *
from Classes.collisionResults import CollisionResults


class Antelope(Animal):
    def __init__(self, positionX, positionY, world):
        super().__init__(4, 4, positionX, positionY, world, PhotoImage(file="Img/antylopa.png"), "Antelope")

    def TakeAction(self):
        possibleMoves = self.FindPlaceToMove()
        move = random.randint(0, len(possibleMoves) - 1)
        collisionResult = 0

        for organism in self.world.organisms:
            if organism.x == possibleMoves[move][0] and organism.y == possibleMoves[move][1]:
                collisionResult = organism.Collision(self)
                break

        if collisionResult == CollisionResults.AttackedReflects or collisionResult == CollisionResults.AnimalCreation:
            self.actionMade = True
        if collisionResult == CollisionResults.AttackerEscapes:
            freePlaces = self.FindFreePlace()
            move = random.randint(0, len(freePlaces) - 1)
            self.x = freePlaces[move][0]
            self.y = freePlaces[move][1]
            self.age += 1
            self.actionMade = True
        if collisionResult == CollisionResults.AttackedDies or collisionResult == 0 or \
                collisionResult == CollisionResults.PlantIsEaten:
            self.x = possibleMoves[move][0]
            self.y = possibleMoves[move][1]
            self.age += 1
            self.actionMade = True

    def IsAttackRepealed(self):
        escape = random.randint(0, 1)
        if escape == 0:
            if len(self.FindFreePlace()) != 0:
                return True
            else:
                return False
        else:
            return False

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
            if self.IsAttackRepealed():
                self.world.AddLogInfo(attacker.name + " tried to attack " + self.name + ", but it escaped")
                freePlaces = self.FindFreePlace()
                move = random.randint(0, len(freePlaces) - 1)
                self.x = freePlaces[move][0]
                self.y = freePlaces[move][1]
                return CollisionResults.AttackedEscapes
            if attacker.strength >= self.strength:
                self.world.AddLogInfo(attacker.name + " has just murdered " + self.name)
                self.world.organisms.remove(self)
                return CollisionResults.AttackedDies
            else:
                self.world.AddLogInfo(self.name + " has just murdered " + attacker.name)
                self.world.organisms.remove(attacker)
                return CollisionResults.AttackerDies

    def FindPlaceToMove(self):
        possibleMoves = []
        if self.y > 0:
            possibleMoves.append([self.x, self.y - 1])
        if self.x > 0:
            possibleMoves.append([self.x - 1, self.y])
        if self.y < self.world.height:
            possibleMoves.append([self.x, self.y + 1])
        if self.x < self.world.width:
            possibleMoves.append([self.x + 1, self.y])
        if self.y > 1:
            possibleMoves.append([self.x, self.y - 2])
        if self.x > 1:
            possibleMoves.append([self.x - 2, self.y])
        if self.y < self.world.height - 1:
            possibleMoves.append([self.x, self.y + 2])
        if self.x < self.world.width - 1:
            possibleMoves.append([self.x + 2, self.y])

        return possibleMoves