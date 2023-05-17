from Classes.Organisms.plant import Plant
from Classes.world import *


class SowThistle(Plant):
    def __init__(self, positionX, positionY, world):
        super().__init__(0, 0, positionX, positionY, world, PhotoImage(file="Img/mlecz.png"), "Sow Thistle")

    def TakeAction(self):
        n = 0
        freePlaces = []
        for i in range(0, 2):
            sow = random.randint(0, 99)
            if sow < 15:
                freePlaces = self.FindFreePlace()
                if len(freePlaces) != 0:
                    newOrganismPosition = random.randint(0, len(freePlaces) - 1)
                    x = freePlaces[newOrganismPosition][0]
                    y = freePlaces[newOrganismPosition][1]
                    self.world.organisms.append(type(self)(x, y, self.world))
                    n = n + 1
                else:
                    break
        if n == 1:
            self.world.AddLogInfo(self.name + " spread 1 time")
        if n > 1:
            self.world.AddLogInfo(self.name + " spread " + str(n) + " time(s)")

        self.age += 1
        self.actionMade = True
