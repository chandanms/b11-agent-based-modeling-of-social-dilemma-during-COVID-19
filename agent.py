from mesa import Agent, Model
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

import enum
import csv


class InfectionState(enum.IntEnum) :
	CLEAN = 0
	INFECTED = 1
	RECOVERED = 2

	
class QuarantineState(enum.IntEnum) :
	QUARANTINE = 3
	FREE = 4


#Agents are modelled and perform various actions.
class MainAgent(Agent) :
	def __init__(self, unique_id, model, pos) :

		# inherit the parent class
		super().__init__(unique_id, model)
		self.infectionstate = InfectionState.CLEAN
		self.quarantinestate = QuarantineState.FREE
		self.infected_time = 0

		#parameters to implement the social dilemma problem
		self.aspiration = self.model.global_aspiration
		self.habituation = self.model.habituation
		self.action_payoff = {
			"Stay In": 0.4,
			"Party": 0.7,
			"Buy grocery": 0.7,
			"Help elderly": 0.7
		}

		self.action_prob = {
			"Stay In": 0.5,
			"Party": 0.5/3,
			"Buy grocery": 0.5/3,
			"Help elderly": 0.5/3
		}

		self.stimulus=list()
		self.action_done=list()

		self.display_progress("Initial action probabilities: ",self.action_prob)

	# action picked by agents

	def action_picker(self):
		action_probability_stayin_t0 = self.action_prob['Stay In']

		# Add effect of government stringent to the action probabilities

		action_probability_stayin_t1 = self.action_prob['Stay In'] + (self.model.government_stringent/100)

		action_probability_adjust = (action_probability_stayin_t1 - action_probability_stayin_t0)/3

		# Check that there is no probability goes below 0

		probability_error = False

		for key in list(self.action_prob.keys()):
			if key != 'Stay In':
				if ((self.action_prob[key] - action_probability_adjust) < 0) :
					probability_error = True
					break

		if probability_error == False :
			self.action_prob['Stay In'] = self.action_prob['Stay In'] + (self.model.government_stringent/100)
			for key in list(self.action_prob.keys()) :
				if key != 'Stay In' :
					self.action_prob[key] = self.action_prob[key] - action_probability_adjust

		# Agent picks an action to perform.
		if (self.quarantinestate == QuarantineState.QUARANTINE):
			action= "Stay In"
		else:
			action=np.random.choice(list(self.action_prob.keys()), p = list(self.action_prob.values()))

		self.action_done.append(action)

		self.display_progress("------------------------------------------------------------------------------------------")


	def spread(self) :
		#Spread virus based on the rate of spread and the state of neighbours

		possible_spread_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
		for neighbour in possible_spread_list :
			if ((self.model.grid.is_cell_empty(neighbour) == False) and 
				(self.model.grid.get_cell_list_contents(neighbour)[0].infectionstate == InfectionState.INFECTED) and 
				(self.random.random() < self.model.transfer_rate)):
				
				if (self.infectionstate == InfectionState.CLEAN):
					self.infectionstate = InfectionState.INFECTED
					self.infected_time = self.model.schedule.time
					self.display_progress("Agent is infected")



	def action_outcome_spread_lockdown(self):
		#Spread virus based on the action performed by agent and state of neighbours

		possible_spread_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

		for neighbour in possible_spread_list:
			if ((self.model.grid.is_cell_empty(neighbour) == False) and 
			   (self.model.grid.get_cell_list_contents(neighbour)[0].infectionstate == InfectionState.INFECTED)):
				action_performed=self.action_done[-1]

				if (self.random.random() <= self.model.action_infection_prob[action_performed] and 
					(self.infectionstate == InfectionState.CLEAN)):
					self.infectionstate = InfectionState.INFECTED
					self.infected_time=self.model.schedule.time
					self.display_progress("Agent is INFECTED.")

					#A fraction of agent choose to self quarantine on being infected
					if (self.random.random() <= self.model.quarantine_prob):
						self.quarantinestate=QuarantineState.QUARANTINE
						self.display_progress("Agent self quarantines.")

					

	def social_dilemma_influence(self): 
		#updating aspiration and payoff for the agent

		payoff=0
		action_performed=self.action_done[-1]

		#Agent recieves no payoff on being infected.
		if (self.infectionstate == InfectionState.INFECTED and self.model.schedule.time-self.infected_time == 0):
			payoff=0
		else:
			payoff=self.action_payoff[action_performed]
		stimulus = payoff - self.aspiration
		
		if (stimulus<0 and self.infectionstate != InfectionState.INFECTED):
			#if the agent isn't infected but recieves a pay off lower than the aspiration, the agent explores other action
			self.randomizer()
		else:
			self.aspiration=self.aspiration*(1-self.habituation)+self.habituation*payoff
			action_probability_t0=self.action_prob[action_performed]
			action_probability_t1=0

			#Update probability of doing an action
			if (stimulus>0):
				action_probability_t1 = action_probability_t0+(1-action_probability_t0)*self.model.learning_rate*stimulus
				self.aspiration=self.aspiration*(1-self.habituation)+self.habituation*payoff
			elif (stimulus<=0):
				action_probability_t1 = action_probability_t0+action_probability_t0*self.model.learning_rate*stimulus
				self.aspiration=self.aspiration*(1-self.habituation)-self.habituation*payoff
		
			#Adjust probability of actions since sum of all should be 1	
			probability_adjust = (action_probability_t1 - action_probability_t0)/(self.model.action_count - 1)

			#Ensure the probability for actions are never negative
			probability_error = False
			for key in list(self.action_prob.keys()):
				if (key != action_performed):
					if ((self.action_prob[key] - probability_adjust) < 0) :
						probability_error = True
						break

			if (probability_error == False) :
				self.action_prob[action_performed] = action_probability_t1
				for key in list(self.action_prob.keys()):
					if (key != action_performed):
						self.action_prob[key] = (self.action_prob[key] - probability_adjust)
		
		self.display_progress("Action performed ->",action_performed)
		self.display_progress("Action probability ->",self.action_prob)
		self.display_progress("Agent aspiration ->",self.aspiration)


	def move(self) :
		#Agent moves before lockdown is imposed
		self.model.grid.move_to_empty(self)


	def move_lockdown(self) :
		#Agent moves only if not in quarantine

		if (self.action_done[-1] != "Stay In"):
			self.model.grid.move_to_empty(self)
			self.display_progress("Agent moves")
		else:
			self.display_progress("Agent doesn't move")


	def update_status(self) :
		#Agent state is updated from infected -> dead, infected -> recovered

		if ((self.infectionstate == InfectionState.INFECTED) and 
			((self.model.schedule.time - self.infected_time) > self.model.recovery_days*0.666) and 
			((self.model.schedule.time - self.infected_time) < self.model.recovery_days)):
			#Agent may die at any step after 2/3rd of the recover time
			if (np.random.choice([0, 1], p=[1 - self.model.death_rate, self.model.death_rate]) == 1):
				self.model.grid.remove_agent(self)
				self.model.schedule.remove(self)
				self.model.dead_agents_number = self.model.dead_agents_number + 1
				self.display_progress("Agent dies")

		elif (self.model.recovery_days < (self.model.schedule.time-self.infected_time) and self.infectionstate == InfectionState.INFECTED): 
			 self.infectionstate = InfectionState.RECOVERED
			 self.display_progress("Agent recovers")

		else :
			pass


	def update_status_lockdown(self):
		# update agents from infected -> quarantine, infected/quarantine -> dead, infected -> recover, quarantine -> free

		if ((self.infectionstate == InfectionState.INFECTED) and 
			((self.model.schedule.time - self.infected_time) > self.model.recovery_days*0.666) and 
			((self.model.schedule.time - self.infected_time) < self.model.recovery_days)):

			if (np.random.choice([0,1], p=[1-self.model.death_rate, self.model.death_rate]) == 1):
				self.model.grid.remove_agent(self)
				self.model.schedule.remove(self)
				self.model.dead_agents_number = self.model.dead_agents_number + 1
				self.display_progress("The Agent is dead")
		elif (self.model.recovery_days < (self.model.schedule.time-self.infected_time) and self.infectionstate == InfectionState.INFECTED):
			self.infectionstate = InfectionState.RECOVERED
			self.quarantinestate = QuarantineState.FREE
			self.display_progress("Agent is recovered")
		else :
			pass
			


	def randomizer(self):
		#set the probabilities of performing an action to make agent pick a different action

		for key in self.action_prob.keys():
			if (key == self.action_done[-1]):
				self.action_prob[key] = 0.1
			else :
				self.action_prob[key] = 0.3

	## TO DO : Give arguments to the server to track any agent
	def display_progress(self,*args):
		#track agent 4
		if (self.unique_id==4):
			[print(arg,end=" ") for arg in args]
			print("\n")
					
	
	def step(self) :
		if (self.model.lockdown == False):
			self.move()
			self.spread()
			self.update_status()
		else :
			self.action_picker()
			self.move_lockdown()
			self.action_outcome_spread_lockdown()
			self.social_dilemma_influence()
			self.update_status_lockdown()

			self.model.dilemma_list.append([int(self.model.schedule.time), self.action_done[-1]])