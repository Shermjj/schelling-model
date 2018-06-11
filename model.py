from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
import types
import matplotlib.pyplot as plt


class VariableSchelModel(Model):
    def __init__(self, density, width, height, satisfaction_ratio=[0.5, 0.5], group_count=2, group_pct=[0.5]):
        """
        Schelling's Model with a variable number of 'groups'

        :param density: density of the total number of agents, expressed as a percentage of size of model
        :param width: width of the model
        :param height: height of the model
        :param group_count: number of 'groups'
        :param satisfaction_ratio: satisfaction ratios for the different groups, takes an array of length equivalent
                                    to the number of 'groups'
        :param group_pct: group population size as a percentage of total number of agents, takes an array of length one less
                            than the number of groups. Last group percentage is calculated automatically
        """

        if isinstance(density, str):
            print('string')
        if group_count < 2:
            raise ValueError('Group Count cannot be less than 2!')
        if group_count - 1 != len(group_pct):
            raise ValueError('Group Percentages and Group Count mismatch! '
                             'Group percentages should be 1 less than the number of groups')
        if len(satisfaction_ratio) != group_count:
            raise ValueError('Satisfaction ratio should be a list with length equivalent to the group count')

        self.num_agents = int(density * (width * height))
        self.running = True
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.satisfaction_ratio = satisfaction_ratio
        self.reached_equilibrium = False
        self.agents = []
        self.ratio_sum = 0
        self.lowest_ratio = 1
        self.mean_ratio = 0

        id_offset = 0
        for group in range(group_count):
            if group == group_count - 1:
                # Final count (Percentage isn't explicit, have to calculate,i.e., group_pct length doesnt match ratio)
                pct = 1 - sum(group_pct)
                for i in range(id_offset, id_offset + int(pct * self.num_agents)):
                    a = SchelAgent(i, self, group)
                    self.agents.append(a)
                    id_offset += 1
                    self.schedule.add(a)
                    self.grid.place_agent(a, self.grid.find_empty())
            else:
                for i in range(id_offset, id_offset + int(group_pct[group] * self.num_agents)):
                    a = SchelAgent(i, self, group)
                    self.agents.append(a)
                    id_offset += 1
                    self.schedule.add(a)
                    self.grid.place_agent(a, self.grid.find_empty())

        self.data_collector = DataCollector(
            model_reporters={"mean ratio value": lambda model: model.mean_ratio,
                             "lowest ratio value": lambda model: model.lowest_ratio},
            agent_reporters={"coordinates": lambda agent: agent.pos,
                             "group": lambda agent: agent.group,
                             "satisfaction": lambda agent: agent.satisfied,
                             "agent ratio value": lambda agent: agent.ratio}
        )
        self.data_collector.collect(self)

    def step(self):
        self.ratio_sum = 0
        self.lowest_ratio = 1.0
        self.reached_equilibrium = True
        self.schedule.step()
        self.mean_ratio = self.ratio_sum / self.num_agents
        self.data_collector.collect(self)
        # Debugging for server charts
        # print(self.mean_ratio)
        # print(self.lowest_ratio)

        # Stops model if model reached equilibrium
        self.running = False if self.reached_equilibrium is True else True


class FixedSchelModel(VariableSchelModel):
    def __init__(self, density, width, height, satisfaction_ratio, minority_pct):
        """
        Same as the variable schelling model, but the group is fixed to 2
        See above
        """

        super().__init__(density=density, width=width, height=height,
                         satisfaction_ratio=[satisfaction_ratio, satisfaction_ratio], group_pct=[minority_pct])


class SchelAgent(Agent):
    def __init__(self, unique_id, model, group):
        """
        Agent class for the model
        Agent will relocate based on the group's satisfaction ratio
        i.e., if the ratio (given as the fraction of same group neightbours over total neightbours) is
        less than the ratio (or no neighbours), the agent will relocate

        :param unique_id: Each agent contains a unique id
        :param model: model for the agent
        :param group: group for the agent
        """

        super().__init__(unique_id, model)
        self.ratio = 0.0
        self.group = group
        self.satisfied = False

    def calculate_ratio(self):
        same_group_neighbors = len([neighbor for neighbor in self.model.grid.get_neighbors(self.pos, moore=True)
                                    if self.group == neighbor.group])
        diff_group_neighbors = len([neighbor for neighbor in self.model.grid.get_neighbors(self.pos, moore=True)
                                    if self.group != neighbor.group])

        if same_group_neighbors + diff_group_neighbors > 0:
            ratio = same_group_neighbors / (same_group_neighbors + diff_group_neighbors)
            return ratio
        else:
            # No neighbors
            return 0.0

    def step(self):
        self.ratio = self.calculate_ratio()
        self.model.ratio_sum += self.ratio

        if self.ratio < self.model.lowest_ratio:
            self.model.lowest_ratio = self.ratio

        if self.ratio < self.model.satisfaction_ratio[self.group]:
            self.model.grid.move_to_empty(self)
            self.model.reached_equilibrium = False
        else:
            self.satisfied = True
