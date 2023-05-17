import math
import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename

import random
from Classes.Animals.wolf import Wolf
from Classes.Animals.turtle import Turtle
from Classes.Animals.fox import Fox
from Classes.Animals.sheep import Sheep
from Classes.Animals.cybersheep import Cybersheep
from Classes.Animals.antelope import Antelope
from Classes.Animals.human import Human
from Classes.Plants.sosnowskysHogweed import SosnowskysHogweed
from Classes.Plants.guarana import Guarana
from Classes.Plants.sowThistle import SowThistle
from Classes.Plants.grass import Grass
from Classes.Plants.belladonna import Belladonna


class World:
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Virtual world - Kinga Chodorowska - 184549")
        self.nextHumanMoveText = StringVar()
        self.logField = Text(self.root, height=5)
        self.board = Canvas(self.root, bg="white")
        self.widthEntry = Entry(self.root)
        self.widthEntry.insert(END, '20')
        self.heightEntry = Entry(self.root)
        self.heightEntry.insert(END, '20')
        self.board.config(width=0, height=0)
        self.widthLabel = Label(self.root, text="Provide the width of the world")
        self.heightLabel = Label(self.root, text="Provide the height of the world")
        self.createWorldButton = Button(text='Make world', command=lambda: self.SetWorldSize(self.heightEntry.get(),
                                                                                             self.widthEntry.get(),
                                                                                             True))
        self.frame = Frame(self.root)
        self.buttonsFrame = Frame(self.root)
        self.nextRoundButton = Button(text='Start new round', command=self.NextRound)
        self.saveButton = Button(self.buttonsFrame, text='Save to file', command=self.Save)
        self.loadButton = Button(self.buttonsFrame, text='Load from file', command=self.Load)
        self.specialAbility = Label(self.root, text="Magical potion is enabled")
        Label(self.frame, text="Human's next move: ").pack(side=LEFT)
        Label(self.frame, textvariable=self.nextHumanMoveText).pack(side=RIGHT)
        self.widthLabel.pack()
        self.widthEntry.pack()
        self.heightLabel.pack()
        self.heightEntry.pack()
        self.createWorldButton.pack()
        self.board.pack()
        self.logField.pack()
        self.saveButton.pack(side=LEFT)
        self.loadButton.pack(side=LEFT)
        self.buttonsFrame.pack()
        self.root.bind_all('<Key>', self.KeyPressed)
        self.board.bind("<Button-1>", self.Callback)
        self.addedManuallyX = -1
        self.addedManuallyY = -1
        self.addManualIndex = 0

        self.roundNumber = 0
        self.organisms = []
        self.worldMap = []
        self.width = 0
        self.height = 0

        mainloop()

    def NextRound(self):
        if self.nextHumanMoveText.get() == "":
            tkinter.messagebox.showinfo(message="Determine the next move of the human")
            return

        for organism in self.organisms:
            organism.actionMade = False

        nextOrganism = self.organisms[0]
        while nextOrganism is not None:
            nextOrganism = None
            for organism in self.organisms:
                if not organism.actionMade:
                    if nextOrganism is None:
                        nextOrganism = organism
                    elif organism.initiative > nextOrganism.initiative:
                        nextOrganism = organism
                    elif organism.initiative == nextOrganism.initiative:
                        if organism.age > nextOrganism.age:
                            nextOrganism = organism
            if nextOrganism is not None:
                nextOrganism.TakeAction()

        self.AddLogInfo("Passed round number " + str(self.roundNumber + 1))
        self.roundNumber += 1
        self.nextHumanMoveText.set("")
        self.DrawWorld()

    def IsFieldEmpty(self, x, y):
        for organism in self.organisms:
            if organism.x == x and organism.y == y:
                return False
        return True

    def GenerateRandomCreatures(self):
        worldDensity = 5

        fieldsNumber = self.width * self.height
        creaturesNumber = int(fieldsNumber * worldDensity / 100) + 1

        for i in range(int(math.ceil(creaturesNumber * 10 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Antelope(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 10 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Cybersheep(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 10 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Fox(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 10 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Sheep(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 5 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Wolf(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 10 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Turtle(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 5 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(SosnowskysHogweed(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 5 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Guarana(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 5 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(SowThistle(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 10 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Grass(x, y, self))
        for i in range(int(math.ceil(creaturesNumber * 5 / 100))):
            x, y = self.FindEmptyField()
            self.organisms.append(Belladonna(x, y, self))

        x, y = self.FindEmptyField()
        self.organisms.append(Human(x, y, self))

    def DrawWorld(self):
        self.board.delete("all")
        for i in range(len(self.organisms)):
            self.organisms[i].Draw()

    def Save(self):
        filename = asksaveasfilename()
        f = open(filename, "w")
        f.write(str(self.height + 1) + "," + str(self.width + 1) + "\n")
        for organism in self.organisms:
            if type(organism) is Human:
                f.write(organism.name + "," + str(organism.strength) + "," + str(organism.initiative) + "," + str(
                    organism.x) + "," + str(organism.y) + "," + str(organism.age) + "," + str(
                    organism.specialAbilityRound) + "\n")
            else:
                f.write(organism.name + "," + str(organism.strength) + "," + str(organism.initiative) + "," + str(
                    organism.x) + "," + str(organism.y) + "," + str(organism.age) + "\n")
        f.close()
        tkinter.messagebox.showinfo(message="Saved to file")

    def Load(self):
        filename = askopenfilename()
        f = open(filename, "r")
        lines = f.readlines()
        h = lines[0].split(",")[0]
        w = lines[0].split(",")[1]
        self.SetWorldSize(h, w, False)
        for i in range(1, len(lines)):
            splited = lines[i].split(",")
            organismType = splited[0]
            if organismType == "Antelope":
                self.organisms.append(Antelope(int(splited[3]), int(splited[4]), self))
            elif organismType == "Cybersheep":
                self.organisms.append(Cybersheep(int(splited[3]), int(splited[4]), self))
            elif organismType == "Human":
                self.organisms.append(Human(int(splited[3]), int(splited[4]), self))
            elif organismType == "Fox":
                self.organisms.append(Fox(int(splited[3]), int(splited[4]), self))
            elif organismType == "Sheep":
                self.organisms.append(Sheep(int(splited[3]), int(splited[4]), self))
            elif organismType == "Wolf":
                self.organisms.append(Wolf(int(splited[3]), int(splited[4]), self))
            elif organismType == "Turtle":
                self.organisms.append(Turtle(int(splited[3]), int(splited[4]), self))
            elif organismType == "Sosnowsky's Hogweed":
                self.organisms.append(SosnowskysHogweed(int(splited[3]), int(splited[4]), self))
            elif organismType == "Guarana":
                self.organisms.append(Guarana(int(splited[3]), int(splited[4]), self))
            elif organismType == "Sow Thistle":
                self.organisms.append(SowThistle(int(splited[3]), int(splited[4]), self))
            elif organismType == "Grass":
                self.organisms.append(Grass(int(splited[3]), int(splited[4]), self))
            elif organismType == "Belladonna":
                self.organisms.append(Belladonna(int(splited[3]), int(splited[4]), self))
            organism = self.organisms[len(self.organisms) - 1]
            organism.strength = int(splited[1])
            organism.initiative = int(splited[2])
            organism.age = int(splited[5])
            if type(organism) is Human:
                organism.specialAbilityRound = int(splited[6])
                if organism.specialAbilityRound > 0:
                    self.specialAbility.pack()

        self.DrawWorld()
        tkinter.messagebox.showinfo(message="Loaded from file")

    def KeyPressed(self, event):
        if event.keysym == 'Right':
            self.nextHumanMoveText.set("Right")
        if event.keysym == 'Left':
            self.nextHumanMoveText.set("Left")
        if event.keysym == 'Up':
            self.nextHumanMoveText.set("Up")
        if event.keysym == 'Down':
            self.nextHumanMoveText.set("Down")
        if event.keysym == 's':
            for organism in self.organisms:
                if type(organism) is Human:
                    if organism.StartSpecialAbility():
                        self.specialAbility.forget()
                        self.specialAbility.pack()

    def Callback(self, event):
        x = (event.x - event.x % 32) / 32
        y = (event.y - event.y % 32) / 32
        empty = self.IsFieldEmpty(x, y)
        if x == self.addedManuallyX and y == self.addedManuallyY:
            self.organisms.pop()
            if self.addManualIndex == 0:
                self.organisms.append(Cybersheep(x, y, self))
            if self.addManualIndex == 1:
                self.organisms.append(Fox(x, y, self))
            if self.addManualIndex == 2:
                self.organisms.append(Sheep(x, y, self))
            if self.addManualIndex == 3:
                self.organisms.append(Wolf(x, y, self))
            if self.addManualIndex == 4:
                self.organisms.append(Turtle(x, y, self))
            if self.addManualIndex == 5:
                self.organisms.append(SosnowskysHogweed(x, y, self))
            if self.addManualIndex == 6:
                self.organisms.append(Guarana(x, y, self))
            if self.addManualIndex == 7:
                self.organisms.append(SowThistle(x, y, self))
            if self.addManualIndex == 8:
                self.organisms.append(Grass(x, y, self))
            if self.addManualIndex == 9:
                self.organisms.append(Belladonna(x, y, self))
            if self.addManualIndex == 10:
                self.addManualIndex = -1
                self.addedManuallyX = -1
                self.addedManuallyY = -1

            self.addManualIndex += 1
            self.DrawWorld()
            return
        if not empty:
            tkinter.messagebox.showerror(message="Field is occupied")
        else:
            self.organisms.append(Antelope(x, y, self))
            self.addedManuallyY = y
            self.addedManuallyX = x
            self.DrawWorld()

    def AddLogInfo(self, text):
        self.logField.insert(END, text + "\n")
        self.logField.see(END)

    def FindEmptyField(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        freeSpace = False
        while not freeSpace:
            freeSpace= True
            for i in range(len(self.organisms)):
                if self.organisms[i].x == x and self.organisms[i].y == y:
                    x = random.randint(0, self.width)
                    y = random.randint(0, self.height)
                    freeSpace = False
                    break
        return x, y

    def SetWorldSize(self, h, w, generate):
        try:
            if int(h) < 4:
                tkinter.messagebox.showerror(message="The minimum world height is 4")
                return
            if int(h) > 20:
                tkinter.messagebox.showerror(message="The maximum world height is 20")
                return
        except ValueError:
            tkinter.messagebox.showerror(message="The value entered in the height field is not an integer")
            return
        try:
            if int(w) < 4:
                tkinter.messagebox.showerror(message="The minimum world width is 4")
                return
            if int(w) > 50:
                tkinter.messagebox.showerror(message="The maximum world width is 50")
                return
        except ValueError:
            tkinter.messagebox.showerror(message="The value entered in the width field is not an integer")
            return

        self.width = int(w) - 1
        self.height = int(h) - 1

        self.buttonsFrame.pack_forget()
        self.heightEntry.pack_forget()
        self.heightLabel.pack_forget()
        self.widthEntry.pack_forget()
        self.widthLabel.pack_forget()
        self.createWorldButton.pack_forget()
        self.frame.pack()
        self.nextRoundButton.pack()
        self.buttonsFrame.pack()

        self.board.config(width=32 * int(w), height=32 * int(h))
        self.AddLogInfo("Created world of dimensions: " + w + " x " + h)
        self.logField.config()
        self.organisms.clear()
        if generate:
            self.GenerateRandomCreatures()
        self.DrawWorld()
