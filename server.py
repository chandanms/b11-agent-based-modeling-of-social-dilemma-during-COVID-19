from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement, BarChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import MainModel, InfectionState, QuarantineState
from agent import MainAgent

clean_color = "#00008b"
recovered_color = "#008000"
quarantine_color = "#FFA500"
infected_color = "#FF0000"

# Text elements to Display

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

class AgentsLegend(TextElement) :
	def __init__(self) :
		pass

	def render (self, model) :
		return "Agent colors - Susceptible: Blue, Quarantine: Orange, Infected: Red, Recovered: Green"

# Color coding of different states, to improve - add colorcoding to mix of two states. ex : Infected and Quarantine

def draw(agent) :
	if agent is None :
		return

	portrayal = {"Shape" : "circle", "r" : 0.5, "Filled" : "true", "Layer" : 0}

	if agent.infectionstate == InfectionState.CLEAN :		
		portrayal["Color"] = clean_color
	elif agent.infectionstate == InfectionState.RECOVERED :
		portrayal["Color"] = recovered_color #green
	elif agent.quarantinestate == QuarantineState.QUARANTINE :
		portrayal["Color"] = quarantine_color   #orange
	elif agent.infectionstate == InfectionState.INFECTED :
		portrayal["Color"] = infected_color
		

	return portrayal


infected_number_text_element = InfectedTextElement()
recovered_number_text_element = RecoveredTextElement()
dead_number_text_element = DeadTextElement()
agent_legend_element = AgentsLegend()
canvas_element = CanvasGrid(draw, 40, 40, 600, 600)

line_chart = ChartModule(
	[
		{"Label" : "Susceptible", "Color": clean_color},
		{"Label" : "Recovered", "Color" : recovered_color},
		{"Label" : "Quarantine and Infected", "Color" : quarantine_color},
		{"Label" : "Out and Infected", "Color" : infected_color},
	]
)

bar_chart = BarChartModule(
	[
		{"Label" : "Stay In", "Color" : "#3349FF"},
		{"Label" : "Go Out", "Color" : "#FF3C33"},
	]
)

# Declare model parameters

model_params = {
    "height": 40,
    "width": 40,
    "population_density" : UserSettableParameter("slider", "Population Density", 0.5, 0.1, 0.8, 0.1),
    "death_rate" : 0.02,
    #"transfer_rate" : 0.3,
    "transfer_rate" : UserSettableParameter("slider", "Virus Transfer Rate", 0.3, 0.1, 0.6, 0.1),
    #"initial_infection_rate" : 0.02,
    "initial_infection_rate" : UserSettableParameter("slider", "Initial Infection Rate", 0.02, 0.01, 0.08, 0.01),
    "government_stringent" : UserSettableParameter("slider", "Government Strictness", 0.5, 0.1, 0.9, 0.1),
    "government_action_threshold" : UserSettableParameter("slider", "Government Action Threshold", 0.3, 0.1, 0.9, 0.1)
}

server = ModularServer(MainModel,
                       [canvas_element, line_chart, bar_chart, infected_number_text_element, recovered_number_text_element, dead_number_text_element, agent_legend_element],
                       "Infection Model", model_params)