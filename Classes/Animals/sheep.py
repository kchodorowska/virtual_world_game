from Classes.Organisms.animal import Animal
from Classes.world import *


class Sheep(Animal):
    def __init__(self, positionX, positionY, world):
        super().__init__(4, 4, positionX, positionY, world, PhotoImage(file="Img/owca.png"), "Sheep")
