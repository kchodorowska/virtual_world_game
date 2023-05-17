from Classes.Organisms.animal import Animal
from Classes.world import *
from Classes.collisionResults import CollisionResults


class Fox(Animal):
    def __init__(self, positionX, positionY, world):
        super().__init__(3, 7, positionX, positionY, world, PhotoImage(file="Img/lis.png"), "Fox")

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

    def IsPositionSafe(self, positionX, positionY):
        for organism in self.world.organisms:
            if organism.x == positionX and organism.y == positionY and organism.strength > self.strength:
                if organism.strength > self.strength:
                    return False
                else:
                    return True
        return True

    def FindPlaceToMove(self):
        possibleMoves = []
        if self.y > 0 and self.IsPositionSafe(self.x, self.y - 1):
            possibleMoves.append([self.x, self.y - 1])
        if self.x > 0 and self.IsPositionSafe(self.x - 1, self.y):
            possibleMoves.append([self.x - 1, self.y])
        if self.y < self.world.height and self.IsPositionSafe(self.x, self.y + 1):
            possibleMoves.append([self.x, self.y + 1])
        if self.x < self.world.width and self.IsPositionSafe(self.x + 1, self.y):
            possibleMoves.append([self.x + 1, self.y])

        return possibleMoves
