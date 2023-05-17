from Classes.Organisms.plant import Plant
from Classes.world import *
from Classes.collisionResults import CollisionResults


class Guarana(Plant):
    def __init__(self, positionX, positionY, world):
        super().__init__(0, 0, positionX, positionY, world, PhotoImage(file="Img/guarana.png"), "Guarana")

    def Collision(self, attacker):
        attacker.strength += 3
        self.world.AddLogInfo(attacker.name + " has just eaten " + self.name)
        self.world.organisms.remove(self)
        return CollisionResults.PlantIsEaten
