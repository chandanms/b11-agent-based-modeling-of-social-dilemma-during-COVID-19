from mesa import Agent
import numpy as np

import enum


class InfectionState(enum.IntEnum):
    """Infected states to keep track"""
    CLEAN = 0
    INFECTED = 1
    RECOVERED = 2


class QuarantineState(enum.IntEnum):
    """Quarantine states to keep track"""
    QUARANTINE = 3
    FREE = 4


class MainAgent(Agent):
    def __init__(self, unique_id, model, pos):
        """Agent class which has all the parameters and functions

        Parameters:
            self.infectionstate: indicates the state of infection in an agent
            self.quarantinestate: indicates the state of quarantine of an agent
            self.aspiration: indicates the aspiration of an agent, initialized with global aspiration from the mainmodel
            self.habituation: indicates the habituation level of an agent
            self.action_payoff: payoff for each action chosen by an agent
            self.action_prob: probability of choosing an action, go out is divided into 3 sub actions

        """
        super().__init__(unique_id, model)  # inherit the parent class
        self.infectionstate = InfectionState.CLEAN
        self.quarantinestate = QuarantineState.FREE
        self.infected_time = 0

        self.aspiration = self.model.global_aspiration
        self.habituation = self.model.habituation
        self.action_payoff = {
            "Stay In": 0.4,
            "Party": 0.7,
            "Buy grocery": 0.5,
            "Help elderly": 0.5
        }

        self.action_prob = {
            "Stay In": 0.5,
            "Party": 0.5 / 3,
            "Buy grocery": 0.5 / 3,
            "Help elderly": 0.5 / 3
        }

        self.stimulus = list()
        self.action_done = list()

    def action_picker(self):
        """Agent chooses an action to do in the current step of the simulation and appends it
        to the list of action done.
        """

        if self.model.lockdown==True:
            action_probability_stayin_t0 = self.action_prob['Stay In']

            # Add effect of government stringent to the action probabilities
            action_probability_stayin_t1 = self.action_prob['Stay In'] + (
                self.model.government_stringent / 100)

            action_probability_adjust = (
                action_probability_stayin_t1 - action_probability_stayin_t0) / 3

            probability_error = False  # Check that there is no probability goes below 0

            for key in list(self.action_prob.keys()):
                if key != 'Stay In':
                    if ((self.action_prob[key] -
                         action_probability_adjust) < 0):
                        probability_error = True
                        break

            if probability_error is False:
                self.action_prob['Stay In'] = self.action_prob['Stay In'] + \
                    (self.model.government_stringent / 100)
                for key in list(self.action_prob.keys()):
                    if key != 'Stay In':
                        self.action_prob[key] = self.action_prob[key] - \
                            action_probability_adjust

        if (self.quarantinestate == QuarantineState.QUARANTINE):
            action = "Stay In"
        else:
            action = np.random.choice(  # Agent picks an action to perform.
                list(
                    self.action_prob.keys()), p=list(
                    self.action_prob.values()))

        # Append the action chosen by the agent
        self.action_done.append(action)

    def action_outcome_spread(self):
        """Agent spreads the virus depending on the state of himself and his neighbours
        """

        possible_spread_list = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)

        for neighbour in possible_spread_list:
            if ((self.model.grid.is_cell_empty(neighbour) is False) and (
                    self.model.grid.get_cell_list_contents(neighbour)[0].infectionstate == InfectionState.INFECTED)):
                action_performed = self.action_done[-1]

                if (self.random.random() <= self.model.action_infection_prob[action_performed] and
                        (self.infectionstate == InfectionState.CLEAN)):
                    self.infectionstate = InfectionState.INFECTED
                    self.infected_time = self.model.schedule.time

                    # A fraction of agents choose to self quarantine on being
                    # infected
                    if (self.random.random() <= self.model.quarantine_prob):
                        self.quarantinestate = QuarantineState.QUARANTINE

    def social_dilemma_influence(self):
        """Updation of aspiration for the agent based on his
        previous action and payoff
        """

        if self.model.lockdown == True:

	        payoff = 0
	        action_performed = self.action_done[-1]

	        if (self.infectionstate == InfectionState.INFECTED and self.model.schedule.time -
	                self.infected_time == 0):  # Agent recieves no payoff on being infected.
	            payoff = 0
	        else:
	            payoff = self.action_payoff[action_performed]
	        stimulus = payoff - self.aspiration

	        if (stimulus < 0 and self.infectionstate != InfectionState.INFECTED):
	            """if the agent isn't infected but recieves a pay off lower than the
	            aspiration, the agent explores other action
	            """
	            self.randomizer()
	        else:
	            self.aspiration = self.aspiration * \
	                (1 - self.habituation) + self.habituation * payoff
	            action_probability_t0 = self.action_prob[action_performed]
	            action_probability_t1 = 0

	            if (stimulus > 0):  # Update probability of doing an action
	                action_probability_t1 = action_probability_t0 + \
	                    (1 - action_probability_t0) * \
	                    self.model.learning_rate * stimulus
	                self.aspiration = self.aspiration * \
	                    (1 - self.habituation) + self.habituation * payoff
	            elif (stimulus <= 0):
	                action_probability_t1 = action_probability_t0 + \
	                    action_probability_t0 * self.model.learning_rate * stimulus
	                self.aspiration = self.aspiration * \
	                    (1 - self.habituation) - self.habituation * payoff

	            probability_adjust = (  # Adjust probability of actions since sum of all should be 1
	                action_probability_t1 - action_probability_t0) / (self.model.action_count - 1)

	            probability_error = False
	            for key in list(self.action_prob.keys(
	            )):  # Ensure the probability for actions are never negative
	                if (key != action_performed):
	                    if ((self.action_prob[key] - probability_adjust) < 0):
	                        probability_error = True
	                        break

	            if (probability_error is False):
	                self.action_prob[action_performed] = action_probability_t1
	                for key in list(self.action_prob.keys()):
	                    if (key != action_performed):
	                        self.action_prob[key] = (
	                            self.action_prob[key] - probability_adjust)

    def move(self):
        """If the agent is not staying in, move to an empty cell
        """

        if (self.action_done[-1] != "Stay In"):
            self.model.grid.move_to_empty(self)

    def update_status(self):
        """Update agents from:
        infected -> quarantine,
        infected/quarantine -> dead,
        infected -> recover,
        quarantine -> free
        """

        if ((self.infectionstate == InfectionState.INFECTED) and
                ((self.model.schedule.time - self.infected_time) > self.model.recovery_days * 0.666) and
                ((self.model.schedule.time - self.infected_time) < self.model.recovery_days)):

            if (np.random.choice([0, 1], p=[
                    1 - self.model.death_rate, self.model.death_rate]) == 1):
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                self.model.dead_agents_number = self.model.dead_agents_number + 1
        elif (self.model.recovery_days < (self.model.schedule.time - self.infected_time)
              and self.infectionstate == InfectionState.INFECTED):
            self.infectionstate = InfectionState.RECOVERED
            self.quarantinestate = QuarantineState.FREE
        else:
            pass

    def randomizer(self):
        """Set equal probabilities of performaing an action to make agent pick
        a different action to avaoid SCE
        """
        for key in self.action_prob.keys():
            if (key == self.action_done[-1]):
                self.action_prob[key] = 0.1
            else:
                self.action_prob[key] = 0.3

    def step(self):
        self.action_picker()
        self.move()
        self.action_outcome_spread()
        self.social_dilemma_influence()
        self.update_status()

        self.model.dilemma_list.append(
            [int(self.model.schedule.time), self.action_done[-1]])
