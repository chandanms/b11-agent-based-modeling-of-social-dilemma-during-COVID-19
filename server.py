from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import MainModel, InfectionState , QuarentineState

class InfectedTextElement(TextElement) :
	def __init__(self) :
		pass

	def render(self, model) :
		infected_number = model.get_infection_number()
		return "Infected Agents : " + str(infected_number)

class RecoveredTextElement(TextElement) :
	def __init__(self) :
		pass

	def render(self, model) :
		recovered_number = model.get_recovered_number()
		return "Recovered Agents : " + str(recovered_number)

class DeadTextElement(TextElement) :
	def __init__(self) :
		pass

	def render(self, model) :
		dead_number = model.get_dead_number()
		return "Dead Agents : " + str(dead_number)

def draw(agent) :
	if agent is None :
		return

	portrayal = {"Shape" : "circle", "r" : 0.5, "Filled" : "true", "Layer" : 0}

	if agent.state == InfectionState.CLEAN :		
		portrayal["Color"] = ["#0000FF", "#9999FF"]
	elif agent.state == QuarentineState.FREE :
		portrayal["Color"] = ["#32CD32", "#7FFF00"]   #green
	elif agent.state == QuarentineState.QUARENTINE :
		portrayal["Color"] = ["#FF9000", "#FF7B00"]   #orange
	else :
		portrayal["Color"] = ["#FF0000", "#FF9999"]
		

	return portrayal


infected_number_text_element = InfectedTextElement()
recovered_number_text_element = RecoveredTextElement()
dead_number_text_element = DeadTextElement()
canvas_element = CanvasGrid(draw, 20, 20, 500, 500)

model_params = {
    "height": 20,
    "width": 20,
    "population_density" : UserSettableParameter("slider", "Population Density", 0.5, 0.1, 0.8, 0.1),
    "death_rate" : 0.02,
    #"transfer_rate" : 0.3,
    "transfer_rate" : UserSettableParameter("slider", "Virus Transfer Rate", 0.3, 0.1, 0.6, 0.1),
    #"initial_infection_rate" : 0.02,
    "initial_infection_rate" : UserSettableParameter("slider", "Initial Infection Rate", 0.02, 0.01, 0.08, 0.01)
}

server = ModularServer(MainModel,
                       [canvas_element, infected_number_text_element, recovered_number_text_element, dead_number_text_element],
                       "Infection Model", model_params)