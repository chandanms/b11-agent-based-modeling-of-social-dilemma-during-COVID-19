import json
from mesa.visualization.ModularVisualization import VisualizationElement
class TextDisplay(VisualizationElement):
    package_includes = []
    
    # Importing the text display javascript file
    local_includes = ["Visualizatons_module\\TextDisplay_base.js"]

    def __init__(self):
        new_element = "new TextDisplay()"
        
        # Appending the text display in the list of visualization elements
        self.js_code = "elements.push(" + new_element + ");"