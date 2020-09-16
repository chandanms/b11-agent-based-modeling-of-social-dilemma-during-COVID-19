from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import MainModel, InfectionState

class InfectedTextElement(TextElement) :
	def __init__(self) :
		pass

	def render(self, model) :
		infected_number = model.get_infection_number()
		return "Infected Agents : " + str(infected_number)

def draw(agent) :
	if agent is None :
		return

	portrayal = {"Shape" : "circle", "r" : 0.5, "Filled" : "true", "Layer" : 0}

	if agent.state == InfectionState.CLEAN :		
		portrayal["Color"] = ["#0000FF", "#9999FF"]
	else :
		portrayal["Color"] = ["#FF0000", "#FF9999"]
		

	return portrayal


infected_number_text_element = InfectedTextElement()
canvas_element = CanvasGrid(draw, 20, 20, 500, 500)

model_params = {
    "height": 20,
    "width": 20,
    "population_density" : 0.5,
    "death_rate" : 0.02,
    "transfer_rate" : 0.3,
    "initial_infection_rate" : 0.02
}

server = ModularServer(MainModel,
                       [canvas_element, infected_number_text_element],
                       "Infection Model", model_params)