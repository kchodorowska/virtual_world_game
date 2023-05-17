from Classes.Organisms.plant import Plant
from Classes.world import *


class Grass(Plant):
    def __init__(self, positionX, positionY, world):
        super().__init__(0, 0, positionX, positionY, world, PhotoImage(file="Img/trawa.png"), "Grass")
