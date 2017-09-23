from mesa import Model,Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random

class SchelModel(Model):
    def __init__(self,N,width,height,satisfaction_ratio):
        self.numagents = N
        self.grid = SingleGrid(width,height,True)
        self.schedule = RandomActivation(self)
        self.ratio = satisfaction_ratio

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
            model_reporters={},
            agent_reporters={"coordinates,race":lambda j:(j.pos,j.race)}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()



class SchelAgent(Agent):
    def __init__(self,unique_id,model,race):
        super().__init__(unique_id,model)
        self.race = race
        self.isunsatisfied = False

    def get_samerace(self):
        mates = self.model.grid.get_neighbors(self.pos,moore=True)
        samerace = 0
        for i in mates:
            if(i.race == self.race):
                samerace += 1
        return samerace

    def get_diffrace(self):
        mates = self.model.grid.get_neighbors(self.pos,moore=True)
        diffrace = 0
        for i in mates:
            if(i.race != self.race):
                diffrace += 1
        return diffrace

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
        numadjsamerace = self.get_samerace()
        numadjdiffrace = self.get_diffrace()
        if(numadjsamerace + numadjdiffrace > 0):
            ratio = numadjsamerace / (numadjsamerace + numadjdiffrace)
            if(ratio < self.model.ratio):
                self.move()





