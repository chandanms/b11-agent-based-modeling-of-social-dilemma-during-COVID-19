from mesa import Agent, Model
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

import enum


## Declare the Main Model of parameters

class MainModel(Model) :
	def __init__(self, population_density, death_rate, transfer_rate, initial_infection_rate, width, height,recovery_days=21) :

		self.population_density = population_density
		self.death_rate = death_rate
		self.width = width
		self.height = height
		self.transfer_rate = transfer_rate
		self.initial_infection_rate = initial_infection_rate
		self.recovery_days=recovery_days
		self.incubation_time=4

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
					agent.infected_time=self.schedule.time   # time of infection is added for every agent

				self.grid.position_agent(agent, (x,y))
				self.schedule.add(agent)
				i = i + 1

		self.total_population = i

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

		# Stop the simulation if entire population gets infected
		
		if self.get_infection_number() == self.total_population :
			self.running = False


# Infection states. I havent added the state SUSCEPTIBLE since everyone is susceptible to covid19 (Age, asymptomatic parameters will be added in later versions)

class InfectionState(enum.IntEnum) :
	CLEAN = 0
	INFECTED = 1

class QuarentineState(enum.IntEnum) :
	FREE = 2
	QUARENTINE = 3
	

class MainAgent(Agent) :
	def __init__(self, unique_id, model, pos) :
		super().__init__(unique_id, model)
		self.state = InfectionState.CLEAN
		self.infected_time=0

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
			if (self.model.grid.is_cell_empty(possible_spread) == False) and (self.random.random() < self.model.transfer_rate) and (self.state == InfectionState.INFECTED) :
				agent = self.model.grid.get_cell_list_contents(possible_spread)[0]
				if (agent.state == InfectionState.CLEAN) :
					agent.state = InfectionState.INFECTED
					agent.infected_time=self.model.schedule.time  


	def move(self) :
		# agent moves only if not in quarentine
		if self.state != QuarentineState.QUARENTINE:
			self.model.grid.move_to_empty(self)


	# update agents from infected/quarentine -> dead, infected/quarentine -> free/recover, infceted -> quarentine
	def update_status(self):
		if self.state in [InfectionState.INFECTED,QuarentineState.QUARENTINE] and self.model.recovery_days < self.model.schedule.time-self.infected_time:
			if np.random.choice([0,1], p=[1-self.model.death_rate,self.model.death_rate]) == 1:
				self.model.grid.remove_agent(self)
				self.model.schedule.remove(self)
			self.state = QuarentineState.FREE
		elif self.state == InfectionState.INFECTED and self.model.incubation_time < self.model.schedule.time-self.infected_time:
			self.state = QuarentineState.QUARENTINE

		
	def step(self) :
		self.spread()
		self.move()
		self.update_status()

# model = MainModel(population_density, death_rate, transfer_rate, initial_infection_rate, width, height)

# steps = 10

# for i in range(steps) :
# 	model.step()
