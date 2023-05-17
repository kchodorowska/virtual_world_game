from enum import Enum


class CollisionResults(Enum):
    AnimalCreation = 1
    AttackerDies = 2
    AttackedDies = 3
    AttackedReflects = 4
    AttackerEscapes = 5
    AttackedEscapes = 6
    PlantIsEaten = 7
    PlantKills = 8
