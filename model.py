from mesa import Model,Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import random
import numpy as np

class SchelModel(Model):
    def __init__(self,N,width,height,satisfaction_ratio):
        self.numagents = N
        self.running = True
        self.grid = SingleGrid(width,height,True)
        self.schedule = RandomActivation(self)
        self.ratio = satisfaction_ratio
        self.reached_equilibrium = False

        self.meanratio = 0
        self.meanratiosum = 0
        self.lowestratio = 1

        for i in range(N):
            a = SchelAgent(i,self,random.randrange(1,3))
            self.schedule.add(a)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            placed = False
            while(placed != True):
                try:
                    self.grid.place_agent(a, (x, y))
                    placed = True
                except Exception:
                    x = random.randrange(self.grid.width)
                    y = random.randrange(self.grid.height)

        self.datacollector = DataCollector(
            model_reporters={"mean ratio": lambda a: a.meanratio,
                            "lowest ratio": lambda a: a.lowestratio},
            agent_reporters={"coordinates":lambda j:j.pos,
                             "race":lambda j:j.race}
        )
        self.datacollector.collect(self)


    def step(self):
        self.meanratiosum = 0
        self.meanratio = 0
        self.lowestratio = 1
        self.reached_equilibrium = True
        self.schedule.step()
        if(self.reached_equilibrium == True):
            self.running = False
        self.meanratio = self.meanratiosum/self.numagents
        self.datacollector.collect(self)





class SchelAgent(Agent):
    def __init__(self,unique_id,model,race):
        super().__init__(unique_id,model)
        self.ratio = -1
        self.race = race

    def get_samerace(self):
        mates = self.model.grid.get_neighbors(self.pos,moore=True)
        same_race_list = [x for x in mates if x.race == self.race]
        return len(same_race_list)

    def get_diffrace(self):
        mates = self.model.grid.get_neighbors(self.pos,moore=True)
        diff_race_list = [x for x in mates if x.race != self.race]
        return len(diff_race_list)

    def get_ratio(self):
        numadjsamerace = self.get_samerace()
        numadjdiffrace = self.get_diffrace()
        if(numadjsamerace + numadjdiffrace > 0):
            ratio = numadjsamerace / (numadjsamerace + numadjdiffrace)
            return ratio
        else:
            return -1

    def move(self):
        x = random.randrange(self.model.grid.width)
        y = random.randrange(self.model.grid.height)
        placed = False
        while (placed != True):
            try:
                self.model.grid.move_agent(self, (x, y))
                placed = True
            except Exception:
                x = random.randrange(self.model.grid.width)
                y = random.randrange(self.model.grid.height)

    def step(self):
        self.ratio = self.get_ratio()
        self.model.meanratiosum += self.ratio
        if(self.ratio < self.model.lowestratio):
            self.model.lowestratio = self.ratio
        if(self.ratio < self.model.ratio):
            self.move()
            if(self.model.reached_equilibrium == True):
                self.model.reached_equilibrium = False

if(__name__ == "__main__"):
    test = SchelModel(70,10,10,0.5)

