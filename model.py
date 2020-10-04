from mesa import Agent, Model
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

from agent import MainAgent

import enum
import csv

# infection and quarantine states

class InfectionState(enum.IntEnum) :
	CLEAN = 0
	INFECTED = 1
	RECOVERED = 2

	
class QuarantineState(enum.IntEnum) :
	QUARANTINE = 3
	FREE = 4

## Declare the Main Model of parameters

class MainModel(Model) :
	def __init__(self, population_density, death_rate, transfer_rate, 
				initial_infection_rate, width, height, government_stringent, government_action_threshold, recovery_days = 11, 
				habituation=0.1, learning_rate=0.3, global_aspiration=0.6) :

		self.population_density = population_density
		self.death_rate = death_rate
		self.width = width
		self.height = height
		self.transfer_rate = transfer_rate
		self.initial_infection_rate = initial_infection_rate
		self.recovery_days=recovery_days
		self.dead_agents_number = 0

		# graphing parameters
		self.dilemma_list =[] 


		## Parameters for the government actions

		# After this threshold, government imposes lockdown and self quarantine rules
		self.government_action_threshold = government_action_threshold

		# The strictness of the government
		self.government_stringent = government_stringent

		self.lockdown = False

		# The probability of an agent to self quarentine after he gets infected
		self.quarantine_prob = 0.3

		# parameter setting for the social dilemma problem
		self.habituation = habituation
		self.learning_rate = learning_rate
		self.global_aspiration = global_aspiration
		self.action_count = 4
		self.action_infection_prob = {
			"Stay In": 0.1,
			"Party" : 0.7,
			"Buy grocery" : 0.5,
			"Help elderly" : 0.5
		}

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
					agent.infectionstate = InfectionState.INFECTED
					agent.quarantinestate = QuarantineState.FREE
					agent.infected_time=self.schedule.time   # time of infection is added for every agent

				self.grid.position_agent(agent, (x,y))
				self.schedule.add(agent)
				i = i + 1

		self.total_population = i

		self.running = True
		self.datacollector = DataCollector(agent_reporters={"QuarantineState": "quarantinestate", 
															"InfectionState" : "infectionstate"})

	def get_susceptible_number(self):
		#Get number of susceptible agents

		susceptible_number = 0
		for cell in self.grid.coord_iter() :
			if (cell[0] != None) :
				agent = cell[0]
				if (agent.infectionstate == InfectionState.CLEAN):
					susceptible_number = susceptible_number + 1
		return susceptible_number
	
	def get_infection_number(self) :
		# Get number of infected agents

		infected_number = 0
		for cell in self.grid.coord_iter() :
			if (cell[0] != None):
				agent = cell[0]
				if (agent.infectionstate == InfectionState.INFECTED):
					infected_number = infected_number + 1
		return infected_number

	def get_recovered_number(self) :
		# Get number of recovered agents

		recovered_number = 0
		for cell in self.grid.coord_iter() :
			if (cell[0] != None):
				agent = cell[0]
				if (agent.infectionstate == InfectionState.RECOVERED):
					recovered_number = recovered_number + 1
		return recovered_number

	def get_dead_number(self) :
		# Get total dead agents
		return self.dead_agents_number

	# Save the CSV of the agents action for plotting

	##TO DO : give arguments to server to specify csv name

	def save_csv(self) :
		with open("simulations/dilemma_" + "stringent_" + str(self.government_stringent) + ".csv", "w", newline='') as file :
			writer = csv.writer(file)
			writer.writerows(self.dilemma_list)

	def step(self) :

		self.datacollector.collect(self)
		self.schedule.step()

		if ((self.get_infection_number()/self.total_population) > self.government_action_threshold):
			self.lockdown = True

		# Stop the simulation if the virus is eradicated
		if ((self.get_recovered_number() + self.get_dead_number()) == self.total_population):
		 	self.running = False
		 	self.save_csv()
		 	


'''Infection states. SUSCEPTIBLE state isn't added since everyone is susceptible to covid19 
'''


