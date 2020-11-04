from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import TextElement
from mesa.visualization.UserParam import UserSettableParameter
from Visualizatons_module.CanvasGridVisualization import CanvasGrid
from Visualizatons_module.ChartVisualization import ChartModule
from Visualizatons_module.TextDisplay import TextDisplay

from model import MainModel, InfectionState, QuarantineState

"""Declare colorcodes for different agent states"""

clean_color = "#00008b"
recovered_color = "#008000"
quarantine_color = "#FFA500"
infected_color = "#FF0000"
dead_color = "#000000"


class SpaceTextElement(TextElement):
    """Text element to add space

    Returns: A line break to add space for visualization
    """

    def __init__(self):
        pass

    def render(self, model):
        return "\n"


class AgentsLegend(TextElement):
    """Text element to add legend of agents

    Returns: Colors of the agents as legend
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Agent colors - Susceptible: Blue, Quarantine: Orange, Infected: Red, Recovered: Green"


def draw(agent):
    """Function to draw agents on the layout of visualization

    Parameters: agent

    Returns: A dictionary of agent shape, radius and color
    """
    if agent is None:
        return

    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.infectionstate == InfectionState.CLEAN:
        portrayal["Color"] = clean_color
    elif agent.infectionstate == InfectionState.RECOVERED:
        portrayal["Color"] = recovered_color  # green
    elif agent.quarantinestate == QuarantineState.QUARANTINE:
        portrayal["Color"] = quarantine_color  # orange
    elif agent.infectionstate == InfectionState.INFECTED:
        portrayal["Color"] = infected_color

    return portrayal


space_text_element = SpaceTextElement()
agent_legend_element = AgentsLegend()
canvas_element = CanvasGrid(draw, 40, 40, 400, 400)


"""Module for line chart one"""

line_chart = ChartModule([{"Label": "Susceptible",
                           "Color": clean_color},
                          {"Label": "Recovered",
                           "Color": recovered_color},
                          {"Label": "Infected",
                           "Color": infected_color},
                          ],
                         canvas_width=20,
                         canvas_height=10,
                         pos_top=16,
                         pos_left=-550,
                         title='"Compare clean-infected-recovered"')

"""Module for line chart two"""

line_chart_aspiration_comparision = ChartModule([{"Label": "Aspiration",
                                                  "Color": "#9400D3"},
                                                 {"Label": "Stay In",
                                                  "Color": "#FFA500"},
                                                 {"Label": "Go Out",
                                                  "Color": "#E033ff"},
                                                 ],
                                                canvas_width=100,
                                                canvas_height=50,
                                                pos_top=-350,
                                                pos_left=200,
                                                title='"Compare aspiration-Stay In numbers-Get out numbers"')

model_legend = TextDisplay()

"""Model parameters are passed to the server"""


model_params = {
    "height": 40,
    "width": 40,
    "population_density": UserSettableParameter("slider", "Population Density", 0.5, 0.1, 0.8, 0.1),
    "death_rate": 0.02,
    "transfer_rate": UserSettableParameter("slider", "Virus Transfer Rate", 0.3, 0.1, 0.6, 0.1),
    "initial_infection_rate": UserSettableParameter("slider", "Initial Infection Number", 0.02, 0.01, 0.08, 0.01),
    "government_stringent": UserSettableParameter("slider", "Government Strictness", 0.5, 0.0, 0.9, 0.1),
    "government_action_threshold": UserSettableParameter("slider", "Government Action Threshold", 0.3, 0.1, 0.9, 0.1),
    "global_aspiration": UserSettableParameter("slider", "Global Aspiration", 0.3, 0.1, 0.9, 0.1)
}

server = ModularServer(MainModel,
                       [canvas_element,
                        model_legend,
                        space_text_element,
                        line_chart,
                        line_chart_aspiration_comparision],
                       "Infection Model",
                       model_params)
