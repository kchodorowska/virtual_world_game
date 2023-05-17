from Classes.Organisms.animal import Animal
from Classes.world import *
from Classes.collisionResults import CollisionResults


class Cybersheep(Animal):
    def __init__(self, positionX, positionY, world):
        super().__init__(11, 4, positionX, positionY, world, PhotoImage(file="Img/cyberowca.png"), "Cybersheep")

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
        if collisionResult == CollisionResults.AttackedDies or collisionResult == CollisionResults.AttackedEscapes \
                or collisionResult == CollisionResults.PlantIsEaten or collisionResult == 0:
            self.age += 1
            self.x = possibleMoves[move][0]
            self.y = possibleMoves[move][1]
            self.actionMade = True

    def FindPlaceToMove(self):
        numberOfMoves = 0
        nearestHogweed = None
        for organism in self.world.organisms:
            if organism.name == "Sosnowsky's Hogweed":
                verticalNumber = abs(organism.y - self.y)
                horizontalNumber = abs(organism.x - self.x)
                if numberOfMoves > (horizontalNumber + verticalNumber) or numberOfMoves == 0:
                    numberOfMoves = horizontalNumber + verticalNumber
                    nearestHogweed = organism
        possibleMoves = []
        if nearestHogweed is None:
            if self.y > 0:
                possibleMoves.append([self.x, self.y - 1])
            if self.x > 0:
                possibleMoves.append([self.x - 1, self.y])
            if self.y < self.world.height:
                possibleMoves.append([self.x, self.y + 1])
            if self.x < self.world.width:
                possibleMoves.append([self.x + 1, self.y])
        else:
            if nearestHogweed.y > self.y:
                possibleMoves.append([self.x, self.y + 1])
            if nearestHogweed.y < self.y:
                possibleMoves.append([self.x, self.y - 1])
            if nearestHogweed.x > self.x:
                possibleMoves.append([self.x + 1, self.y])
            if nearestHogweed.x < self.x:
                possibleMoves.append([self.x - 1, self.y])

        return possibleMoves
