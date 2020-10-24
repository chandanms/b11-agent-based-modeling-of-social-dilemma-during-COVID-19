from mesa import Agent, Model
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

from agent import MainAgent

import enum
import csv
import os

# infection and quarantine states

class InfectionState(enum.IntEnum) :
	CLEAN = 0
	INFECTED = 1
	RECOVERED = 2
	DEAD = 3

	
class QuarantineState(enum.IntEnum) :
	QUARANTINE = 3
	FREE = 4

## Declare the Main Model of parameters


def get_infected_number(model) :
	infected_agents = [a for a in model.schedule.agents if a.infectionstate == InfectionState.INFECTED]
	return len(infected_agents)


def get_recovered_number(model) :
	recovered_agents = [a for a in model.schedule.agents if a.infectionstate == InfectionState.RECOVERED]
	return len(recovered_agents)


def get_dead_number(model) :
	return model.dead_agents_number

def agent_tracking_aspiration(model) :
	try :
		tracked_agent = model.schedule.agents[3]
		return tracked_agent.aspiration
	except Exception as e :
		return "DECEASED"

def agent_tracking_stayin_probability(model) :
	try :
		tracked_agent = model.schedule.agents[3]
		return tracked_agent.action_prob["Stay In"]
	except Exception as e :
		return "DECEASED"

def agent_tracking_goout_probability(model) :
	try :
		tracked_agent = model.schedule.agents[3]
		return tracked_agent.action_prob["Party"] + tracked_agent.action_prob["Help elderly"] + tracked_agent.action_prob["Buy grocery"]
	except Exception as e :
		return "DECEASED"




def get_stay_in(model) :
	try :
		stay_in_number = [a for a in model.schedule.agents if a.action_done[-1] == 'Stay In']
		return len(stay_in_number)
	except Exception as e :
		return 0

def get_go_out(model) :
	try :
		go_out_number = [a for a in model.schedule.agents if a.action_done[-1] != 'Stay In']
		return len(go_out_number)
	except Exception as e :
		return 0


def get_average_aspiration(model) :
	aspiration_list = []
	for i, a in enumerate(model.schedule.agents) :
		aspiration_list.append(a.aspiration)
	return (sum(aspiration_list)/i)

def get_average_stay_in(model) :
	stay_in_list = []
	for i, a in enumerate(model.schedule.agents) :
		stay_in_list.append(a.action_prob["Stay In"])

	return (sum(stay_in_list)/i)

def get_average_go_out(model) :
	go_out_list = []
	for i, a in enumerate(model.schedule.agents) :
		go_out_list.append((a.action_prob["Party"] + a.action_prob["Help elderly"] + a.action_prob["Buy grocery"]))

	return (sum(go_out_list)/i)



class MainModel(Model) :
	
	def __init__(self, population_density, death_rate, transfer_rate, 
				initial_infection_rate, width, height, government_stringent, government_action_threshold, recovery_days = 11, 
				habituation=0.1, learning_rate=0.1, global_aspiration=0.6) :

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

		

		self.datacollector = DataCollector(
			model_reporters = {	
								"Infected" : get_infected_number,
								"Recovered" : get_recovered_number,
								"Dead" : get_dead_number,
								"Stay In" : get_stay_in,
								"Go Out" : get_go_out,
								"Aspiration" : agent_tracking_aspiration,
								"Stay in probability" : agent_tracking_stayin_probability,
								"Go out probability" : agent_tracking_goout_probability,
								"Average Aspiration" : get_average_aspiration,
								"Average Stay In" : get_average_stay_in,
								"Average Get Out" : get_average_go_out,
								
			},

			agent_reporters={
								"QuarantineState": "quarantinestate",
								"InfectionState" : "infectionstate",
							},
		)



	# Save the CSV of the agents action for plotting

	##TO DO : give arguments to server to specify csv name

	def save_csv(self) :
		if not os.path.exists('simulations'):
			os.makedirs('simulations')
		with open("simulations/dilemma_" + "stringent_" + str(self.government_stringent) + ".csv", "w", newline='') as file :
			writer = csv.writer(file)
			writer.writerows(self.dilemma_list)

		# with open("simulations/dilemma_" + "aspiration_" + str(self.global_aspiration) + ".csv", "w", newline='') as file :
		# 	writer = csv.writer(file)
			
		# 	writer.writerows(self.)


	def step(self) :

		self.datacollector.collect(self)
		self.schedule.step()

		if ((self.get_infection_number()/self.total_population) > self.government_action_threshold):
			self.lockdown = True

		# Stop the simulation if the virus is eradicated
		if ((self.get_recovered_number() + self.get_dead_number()) == self.total_population):
		 	self.running = False
		 	self.save_csv()
		
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


	def agent_tracking_infectionstate(self) :
		try :
			tracked_agent = self.schedule.agents[3]
			return tracked_agent.infectionstate.name
		except Exception as e :
			print (e)
			return "DECEASED"

	def agent_tracking_quarantinestate(self) :
		try :
			tracked_agent = self.schedule.agents[3]
			return tracked_agent.quarantinestate.name
		except Exception as e :
			return "DECEASED"


	def agent_tracking_action(self) :
		try :
			tracked_agent = self.schedule.agents[3]
		except Exception as e :
			return "DECEASED"

		try :
			return tracked_agent.action_done[-1]
		except Exception as e :
			return None

