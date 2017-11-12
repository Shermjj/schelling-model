from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import SchelModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5,
                 #"text":str(agent.unique_id),
                 #"text_color":"yellow"
                 }
    if(agent.race == 1):
        portrayal["Color"] = "red"
    elif(agent.race == 2):
        portrayal["Color"] = "blue"


    return portrayal

grid = CanvasGrid(agent_portrayal,50,50)

chart1 = ChartModule([
    {"Label":"mean ratio","Color":"Black"}],
    data_collector_name="datacollector"
)
chart2 = ChartModule([
    {"Label":"lowest ratio","Color":"Black"}],
    data_collector_name="datacollector"
)
param = {"N":UserSettableParameter("slider","Number of Agents",value=500,min_value=2,max_value=2500,step=100),"width":50,"height":50,
         "satisfaction_ratio":UserSettableParameter("slider","Satisfaction ratio",value=0.5,min_value=0,max_value=1,step=0.1)}

server = ModularServer(SchelModel,[grid,chart1,chart2],"Schelling Model",param)

server.port = 8521

def start():
    server.launch()

if __name__ == "__main__":
    start()