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
                 #"text":str(agent.unique_id)
                 #"text_color":"yellow"
                 }
    if(agent.group == 0):
        portrayal["Color"] = "red"
    elif(agent.group == 1):
        portrayal["Color"] = "blue"


    return portrayal

grid = CanvasGrid(agent_portrayal,30,30)

# chart1 = ChartModule([
#     {"Label":"mean calculate_ratio","Color":"Black"}],
#     data_collector_name="data_collector"
# )
# chart2 = ChartModule([
#     {"Label":"lowest calculate_ratio","Color":"Black"}],
#     data_collector_name="data_collector"
# )

param = {}
param = {"density":UserSettableParameter('number','density value',value=0.5),
         "width":30,"height":30}

server = ModularServer(SchelModel,[grid],"Schelling Model",param)

server.port = 8521

def start():
    server.launch()

if __name__ == "__main__":
    start()