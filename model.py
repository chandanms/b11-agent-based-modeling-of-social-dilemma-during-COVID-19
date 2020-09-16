from mesa import Agent, Model
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

import enum


## Declare the Main Model of parameters

class MainModel(Model) :
	def __init__(self, population_density, death_rate, transfer_rate, initial_infection_rate, width, height) :

		self.population_density = population_density
		self.death_rate = death_rate
		self.width = width
		self.height = height
		self.transfer_rate = transfer_rate
		self.initial_infection_rate = initial_infection_rate


		self.grid = SingleGrid(width, height, True)
		self.schedule = RandomActivation(self)

		i = 0

		# Get all the cells in SingleGrid

		for cell in self.grid.coord_iter() :
			x, y = cell[1], cell[2]

			# Add agents and infect them with initial infection rate
			
			if self.random.random() < self.population_density :
				agent = MainAgent(i, self, (x, y))

				if (np.random.choice([0, 1], p = [1 - self.initial_infection_rate, self.initial_infection_rate])) == 1 :
					agent.state = InfectionState.INFECTED

				self.grid.position_agent(agent, (x,y))
				self.schedule.add(agent)
				i = i + 1

		print ("Total population is : ", i)

		self.running = True
		self.datacollector = DataCollector(agent_reporters={"State": "state"})

	def get_infection_number(self) :
		infected_number = 0
		for cell in self.grid.coord_iter() :
			if (cell[0] != None) :
				agent = cell[0]
				if agent.state == InfectionState.INFECTED :
					infected_number = infected_number + 1
		return infected_number

				

	def step(self) :

		self.datacollector.collect(self)
		self.schedule.step()
		self.get_infection_number()


# Infection states. I havent added the state SUSCEPTIBLE since everyone is susceptible to covid19 (Age, asymptomatic parameters will be added in later versions)

class InfectionState(enum.IntEnum) :
	CLEAN = 0
	INFECTED = 1

class MainAgent(Agent) :
	def __init__(self, unique_id, model, pos) :
		super().__init__(unique_id, model)
		self.state = InfectionState.CLEAN

	# def move(self) :
	# 	possible_steps_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
	# 	for possible_step in possible_steps_list :
	# 		if (self.model.grid.is_cell_empty(possible_step) == False) and (self.random.random() < self.model.transfer_rate) :
	# 			agent = self.model.grid.get_cell_list_contents(possible_step)[0]
	# 			if (agent.state == InfectionState.CLEAN) :
	# 				agent.state = InfectionState.INFECTED



	# Spreading the virus based on contact with nearby cells

	def spread(self) :
		possible_spread_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

		# If the nearby cell is not empty and transfer probability is below the predefined value, infect the neighbour

		for possible_spread in possible_spread_list :
			if (self.model.grid.is_cell_empty(possible_spread) == False) and (self.random.random() < self.model.transfer_rate) :
				agent = self.model.grid.get_cell_list_contents(possible_spread)[0]
				if (agent.state == InfectionState.CLEAN) :
					agent.state = InfectionState.INFECTED				

		

	def step(self) :
		self.spread()

# model = MainModel(population_density, death_rate, transfer_rate, initial_infection_rate, width, height)

# steps = 10

# for i in range(steps) :
# 	model.step()