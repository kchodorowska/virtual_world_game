from Classes.Organisms.plant import Plant
from Classes.world import *
from Classes.collisionResults import CollisionResults


class Belladonna(Plant):
    def __init__(self, positionX, positionY, world):
        super().__init__(99, 0, positionX, positionY, world, PhotoImage(file="Img/jagoda.png"), "Belladonna")

    def Collision(self, attacker):
        self.world.AddLogInfo(attacker.name + " has just eaten " + self.name + " and died")
        self.world.organisms.remove(self)
        self.world.organisms.remove(attacker)
        return CollisionResults.PlantKills
