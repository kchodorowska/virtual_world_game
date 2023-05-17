from Classes.world import *
from abc import ABC, abstractmethod


class Organism(ABC):
    def __init__(self, strength, initiative, x, y, world, img, name, age=0, actionMade=True):
        self.strength = strength
        self.initiative = initiative
        self.x = x
        self.y = y
        self.world = world
        self.img = img
        self.name = name
        self.age = age
        self.actionMade = actionMade

    @abstractmethod
    def TakeAction(self):
        pass

    @abstractmethod
    def Collision(self, attacker):
        pass

    @abstractmethod
    def IsAttackRepealed(self, attacker):
        pass

    def Draw(self):
        self.world.board.create_image(self.x * 32, self.y * 32, image=self.img, anchor=NW)

    @abstractmethod
    def FindFreePlace(self):
        pass
