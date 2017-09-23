from model import SchelModel
import matplotlib.pyplot as plt

fig,(ax1,ax2) = plt.subplots(1,2)
test = SchelModel(30,10,10,1)

for agents in test.schedule.agents:
    if(agents.race == 1):
        x,y = agents.pos
        ax1.scatter(x,y,color="r")
    else:
        x, y = agents.pos
        ax1.scatter(x, y, color="b")

for i in range(100):
    test.step()

for agents in test.schedule.agents:
    if(agents.race == 1):
        x,y = agents.pos
        ax2.scatter(x,y,color="r")
    else:
        x, y = agents.pos
        ax2.scatter(x, y, color="b")

fr = test.datacollector.get_agent_vars_dataframe()
print(fr.axes)
print(fr.head())
print(fr.tail())
print(fr.xs(0,level="AgentID"))
plt.show()
h