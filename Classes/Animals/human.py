from Classes.Organisms.animal import Animal
from Classes.world import *
from Classes.collisionResults import CollisionResults


class Human(Animal):
    def __init__(self, positionX, positionY, world):
        super().__init__(5, 4, positionX, positionY, world, PhotoImage(file="Img/czlowiek.png"), "Human")
        self.specialAbilityRound = 0

    def TakeAction(self):
        self.NextSpecialAbilityRound()

        move = [self.x, self.y]
        if self.world.nextHumanMoveText.get() == "Right" and self.x < self.world.width:
            move = [self.x + 1, self.y]
        if self.world.nextHumanMoveText.get() == "Left" and self.x > 0:
            move = [self.x - 1, self.y]
        if self.world.nextHumanMoveText.get() == "Up" and self.y > 0:
            move = [self.x, self.y - 1]
        if self.world.nextHumanMoveText.get() == "Down" and self.y < self.world.height:
            move = [self.x, self.y + 1]
        if move == [self.x, self.y]:
            self.actionMade = True
            return

        collisionResult = 0

        for organism in self.world.organisms:
            if organism.x == move[0] and organism.y == move[1]:
                collisionResult = organism.Collision(self)
                break

        if collisionResult == CollisionResults.AttackedReflects:
            self.age += 1
            self.actionMade = True
        if collisionResult == CollisionResults.AttackedDies or collisionResult == CollisionResults.AttackedEscapes \
                or collisionResult == CollisionResults.PlantIsEaten or collisionResult == 0:
            self.age += 1
            self.x = move[0]
            self.y = move[1]
            self.actionMade = True

    def StartSpecialAbility(self):
        if self.strength > 10:
            tkinter.messagebox.showerror(message="A human is too strong")
            self.world.specialAbility.forget()
            return False
        else:
            if self.specialAbilityRound == 0:
                self.specialAbilityRound = 1
                self.strength = 10
                self.world.AddLogInfo("Magic potion - round no. 1")
                return True
            if self.specialAbilityRound > 5:
                tkinter.messagebox.showerror(message="Magic potion can't be activated")
                self.world.specialAbility.forget()
                return False

    def NextSpecialAbilityRound(self):
        if self.specialAbilityRound == 0:
            return
        else:
            self.specialAbilityRound += 1
            self.strength -= 1
            if self.specialAbilityRound > 5:
                if self.specialAbilityRound == 6:
                    self.world.specialAbility.forget()
                    self.world.AddLogInfo("Magic potion - finish")
                if self.specialAbilityRound == 10:
                    self.specialAbilityRound = 0
                    self.strength += 1
            else:
                self.world.AddLogInfo("Magic potion - round no. " + str(self.specialAbilityRound))
