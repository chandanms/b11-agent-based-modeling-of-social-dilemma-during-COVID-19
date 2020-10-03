from mesa import Agent, Model
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

import enum


## Declare the Main Model of parameters

class MainModel(Model) :
	def __init__(self, population_density, death_rate, transfer_rate, initial_infection_rate, width, height, recovery_days = 11, habituation=0.1, learning_rate=0.3, global_aspiration=0.4) :

		self.population_density = population_density
		self.death_rate = death_rate
		self.width = width
		self.height = height
		self.transfer_rate = transfer_rate
		self.initial_infection_rate = initial_infection_rate
		self.recovery_days=recovery_days
		self.dead_agents_number = 0
		# parameter for the government actions

		self.governement_action_threshold = 0.3  #After this threshold, government imposes lockdown and self quarantine rules.
		self.lockdown = False
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
		self.datacollector = DataCollector(agent_reporters={"QuarantineState": "quarantinestate", "InfectionState" : "infectionstate"})

	#Get number of susceptible agents

	def get_susceptible_number(self):
		susceptible_number = 0
		for cell in self.grid.coord_iter() :
			if (cell[0] != None) :
				agent = cell[0]
				if agent.infectionstate == InfectionState.CLEAN :
					susceptible_number = susceptible_number + 1
		return susceptible_number

	# Get number of infected agents

	def get_infection_number(self) :
		infected_number = 0
		for cell in self.grid.coord_iter() :
			if (cell[0] != None) :
				agent = cell[0]
				if agent.infectionstate == InfectionState.INFECTED :
					infected_number = infected_number + 1
		return infected_number


	# Get number of recovered agents

	def get_recovered_number(self) :
		recovered_number = 0
		for cell in self.grid.coord_iter() :
			if (cell[0] != None) :
				agent = cell[0]
				if agent.infectionstate == InfectionState.RECOVERED :
					recovered_number = recovered_number + 1
		return recovered_number

	# Get total dead agents

	def get_dead_number(self) :
		return self.dead_agents_number
				

	def step(self) :

		self.datacollector.collect(self)
		self.schedule.step()

		if (self.get_infection_number()/self.total_population) > 0.4 :
			self.lockdown = True

		# Stop the simulation if entire population gets infected
		
		if (self.get_recovered_number() + self.get_dead_number() + self.get_susceptible_number()) == self.total_population :
		 	self.running = False



'''Infection states. I havent added the state SUSCEPTIBLE since everyone is susceptible to covid19 
(Age, asymptomatic parameters will be added in later versions)
'''

class InfectionState(enum.IntEnum) :
	CLEAN = 0
	INFECTED = 1
	RECOVERED = 2
	
class QuarantineState(enum.IntEnum) :
	QUARANTINE = 3
	FREE = 4

class MainAgent(Agent) :
	def __init__(self, unique_id, model, pos) :
		super().__init__(unique_id, model)
		self.infectionstate = InfectionState.CLEAN
		self.quarantinestate = QuarantineState.FREE
		self.infected_time = 0

		#parameters for social dilemma problem
		self.aspiration = self.model.global_aspiration
		self.action_payoff = {
		"Stay In": 0.4,
		"Party": 0.7,
		"Buy grocery": 0.7,
		"Help elderly": 0.7
		}
		self.action_prob = {
		"Stay In": 0.25,
		"Party": 0.25,
		"Buy grocery": 0.25,
		"Help elderly": 0.25
		}

		self.stimulus=list()
		self.action_done=list()
		#self.display_progress("Initial action probabilities: ",self.action_prob)


	def action_picker(self):
		#agent picks an action to perform

		action=np.random.choice(list(self.action_prob.keys()),p = list(self.action_prob.values()))
		self.action_done.append(action)

		# self.display_progress("------------------------------------------------------------------------------------------")
		# self.display_progress("Actions chosen --> ",self.action_done)


	def spread(self) :
		possible_spread_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
		for neighbour in possible_spread_list :
			if (self.model.grid.is_cell_empty(neighbour) == False) and (self.model.grid.get_cell_list_contents(neighbour)[0].infectionstate == InfectionState.INFECTED) and (self.random.random() < self.model.transfer_rate):
				if (self.infectionstate == InfectionState.CLEAN):
					self.infectionstate = InfectionState.INFECTED
					self.infected_time = self.model.schedule.time



	def action_outcome_spread_lockdown(self):
		#spread virus based on the action performed by agent and state of neighbours

		possible_spread_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
		for neighbour in possible_spread_list:
			if (self.model.grid.is_cell_empty(neighbour) == False) and (self.model.grid.get_cell_list_contents(neighbour)[0].infectionstate == InfectionState.INFECTED):
				action_performed=self.action_done[-1]
				if self.random.random()>=self.model.action_infection_prob[action_performed] and (self.infectionstate == InfectionState.CLEAN):
					self.infectionstate = InfectionState.INFECTED
					self.infected_time=self.model.schedule.time

					if self.random.random() >= self.model.quarantine_prob:
						self.quarantinestate=QuarantineState.QUARANTINE
					

					#self.display_progress("Agent gets INFECTED. Incubation period of four days begins.")

	def social_dilemma_influence(self): 
		#updating aspiration and payoff for the agent

		payoff=0
		action_performed=self.action_done[-1]

		'''assign payoff if the current action infected the agent.
		All actions during incuabtion time (self.model.schedule.time-self.infected_time>0) recieve normal payoff.
		'''
		if self.infectionstate == InfectionState.INFECTED and self.model.schedule.time-self.infected_time == 0:
			payoff=0
		else:
			payoff=self.action_payoff[action_performed]
		stimulus = payoff - self.aspiration
		

		#self.display_progress("Agent's aspiration level is ",self.aspiration)
		
		#set new aspiration level
		if stimulus<0 and self.infectionstate != InfectionState.INFECTED :
			self.randomizer()
		else:
			self.aspiration=self.aspiration*(1-self.model.habituation)+self.model.habituation*payoff
			action_probability_t0=self.action_prob[action_performed]
			action_probability_t1=0


		##Changed Stimulus
		#update probability of doing an action
			if stimulus>0 :
				action_probability_t1 = action_probability_t0+(1-action_probability_t0)*self.model.learning_rate*stimulus
				self.aspiration=self.aspiration*(1-self.model.habituation)+self.model.habituation*payoff
			elif stimulus<=0 :
				action_probability_t1 = action_probability_t0+action_probability_t0*self.model.learning_rate*stimulus
				self.aspiration=self.aspiration*(1-self.model.habituation)-self.model.habituation*payoff
		
		#adjust probability of actions since sum of all should be 1	

		
		#self.display_progress("Probability update for {} ".format(action_performed),self.action_prob[action_performed])
		
			probability_adjust = (action_probability_t1 - action_probability_t0)/(self.model.action_count - 1)

			probability_error = False
			for key in list(self.action_prob.keys()):
				if key != action_performed:
					if ((self.action_prob[key] - probability_adjust) < 0) :
						probability_error = True
						break

			if (probability_error == False) :
				self.action_prob[action_performed] = action_probability_t1
				for key in list(self.action_prob.keys()):
					if key != action_performed:
						self.action_prob[key] = (self.action_prob[key] - probability_adjust)
					
				
				#self.display_progress("Probability update for {} is {}".format(key,self.action_prob[key]))
		
		#self.stimulus.append(stimulus)
		if self.unique_id == 4 :
			print (action_performed)
			print (self.action_prob)
			print (self.aspiration)


	def move(self) :
		self.model.grid.move_to_empty(self)


	def move_lockdown(self) :
		# agent moves only if not in quarantine

		if self.action_done[-1] != "Stay In":
			self.model.grid.move_to_empty(self)
			#self.display_progress("Agent moves")
		else:
			# self.quarantinestate = QuarantineState.QUARANTINE
			self.display_progress("Agent doesn't move")


	##Changed - People have chances of death in every step after 2/3rd of recovery time

	def update_status(self) :
		if (self.infectionstate == InfectionState.INFECTED) and ((self.model.schedule.time - self.infected_time) > self.model.recovery_days*0.666) and ((self.model.schedule.time - self.infected_time) < self.model.recovery_days) :
			if np.random.choice([0, 1], p=[1 - self.model.death_rate, self.model.death_rate]) == 1 :
				self.model.grid.remove_agent(self)
				self.model.schedule.remove(self)
				self.model.dead_agents_number = self.model.dead_agents_number + 1
		elif (self.model.recovery_days < (self.model.schedule.time-self.infected_time)) :     #if agent not infected he cant recover
			self.infectionstate = InfectionState.RECOVERED
		else :
			pass

	# update agents from infected/quarantine -> dead, infected/quarantine -> recover, infected -> quarantine
	def update_status_lockdown(self):
		if (self.infectionstate == InfectionState.INFECTED) and ((self.model.schedule.time - self.infected_time) > self.model.recovery_days*0.666) and ((self.model.schedule.time - self.infected_time) < self.model.recovery_days):
			if np.random.choice([0,1], p=[1-self.model.death_rate, self.model.death_rate]) == 1:
				self.model.grid.remove_agent(self)
				self.model.schedule.remove(self)
				self.model.dead_agents_number = self.model.dead_agents_number + 1
				
				#self.display_progress("The Agent is dead")
		elif (self.model.recovery_days < (self.model.schedule.time-self.infected_time)) :
			self.infectionstate = InfectionState.RECOVERED
			self.quarantinestate = QuarantineState.FREE

		else :
			pass
			
			#self.display_progress("The Agent has recovered")
			
			#self.display_progress("Agent is put under Quarantine until recovered")


	def randomizer(self):
		'''set the probabilities of performing an action to make agent pick a different action''' 
		for key in self.action_prob.keys():
			if key == self.action_done[-1] :
				self.action_prob[key] = 0.1
			else :
				self.action_prob[key] = 0.3

	
	def display_progress(self,*args):
		'''track agent 0'''

		if self.unique_id==0:
			#print("({0},{1},{2})".format(self.unique_id,self.action_done,self.stimulus))
			[print(arg,end=" ") for arg in args]
			print("\n")
					
	
	def step(self) :
		if (self.model.lockdown == False) :
			self.move()
			self.spread()
			self.update_status()

		else :

			self.action_picker()
			self.move_lockdown()
			self.action_outcome_spread_lockdown()
			self.social_dilemma_influence()
			self.update_status_lockdown()

'''
model = MainModel(population_density, death_rate, transfer_rate, initial_infection_rate, width, height)

steps = 10

for i in range(steps) :
	model.step()
'''