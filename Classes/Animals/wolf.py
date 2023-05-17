from Classes.Organisms.animal import Animal
from Classes.world import *


class Wolf(Animal):
    def __init__(self, positionX, positionY, world):
        super().__init__(9, 5, positionX, positionY, world, PhotoImage(file="Img/wilk.png"), "Wolf")
