from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np
from mesa.batchrunner import BatchRunner
import numpy as np
import pandas as pd
from agent import MainAgent

import enum
import csv
import os

"""infection and quarantine states"""


class InfectionState(enum.IntEnum):
    """Infected states to keep track"""
    CLEAN = 0
    INFECTED = 1
    RECOVERED = 2
    DEAD = 3


class QuarantineState(enum.IntEnum):
    """Quarantine states to keep track"""
    QUARANTINE = 3
    FREE = 4


def get_susceptible_number(model):
    """Get number of susceptible agents

    Returns: total number of susceptible agents
    """
    susceptible_agents = [
        a for a in model.schedule.agents if a.infectionstate == InfectionState.CLEAN]
    return len(susceptible_agents)


def get_infected_number(model):
    """Get number of infected agents

    Returns: total number of infected agents
    """
    infected_agents = [
        a for a in model.schedule.agents if a.infectionstate == InfectionState.INFECTED]
    return len(infected_agents)


def get_recovered_number(model):
    """Get number of recovered agents

    Returns: total number of recovered agents
    """
    recovered_agents = [
        a for a in model.schedule.agents if a.infectionstate == InfectionState.RECOVERED]
    return len(recovered_agents)


def get_dead_number(model):
    """Get number of dead agents

    Returns : total number of dead agents
    """
    return model.dead_agents_number


def get_stay_in(model):
    """Get number of agents that are staying in

    Returns: Total number of agents that are staying in at current step
    """
    try:
        stay_in_number = [
            a for a in model.schedule.agents if a.action_done[-1] == 'Stay In']
        return len(stay_in_number)
    except Exception:
        return 0


def get_go_out(model):
    """Get number of agents that go out

    Returns: Total number of agents that go out at current step
    """
    try:
        go_out_number = [
            a for a in model.schedule.agents if a.action_done[-1] != 'Stay In']
        return len(go_out_number)
    except Exception:
        return 0


def get_average_aspiration(model):
    """Get the average aspiration of the population

    Returns: average aspiration of all the agents in population
    """
    aspiration_list = []
    for i, a in enumerate(model.schedule.agents):
        aspiration_list.append(a.aspiration)
    return (sum(aspiration_list) / i)


def get_average_stay_in(model):
    """Get the average probability of staying in

    Returns: average probability of all agents who are staying in
    """
    stay_in_list = []
    for i, a in enumerate(model.schedule.agents):
        stay_in_list.append(a.action_prob["Stay In"])

    return (sum(stay_in_list) / i)


def get_average_go_out(model):
    """Get the average probability of going out

    Returns: average action probability of all agents of the action going out
    """
    go_out_list = []
    for i, a in enumerate(model.schedule.agents):
        go_out_list.append(
            (a.action_prob["Party"] +
             a.action_prob["Help elderly"] +
             a.action_prob["Buy grocery"]))

    return (sum(go_out_list) / i)


class MainModel(Model):

    def __init__(self, government_stringent, global_aspiration, population_density=0.3, death_rate=0.02, transfer_rate=0.3,
                 initial_infection_rate=0.02, width=40, height=40,
                 government_action_threshold=0.3, recovery_days=11, habituation=0.1,
                 learning_rate=0.1):
        """Model class which has all the model paramaters and functions

        Parameters:
            self.population_density: Population density defines the density of population in simulation.
            self.death_rate: Death rate defines the death rate of the virus spreading in the simulation
            self.width: width of the simulation
            self.height: height of the simulation
            self.transfer_rate: Transfer rate of the svirus in the simulation
            self.initial_infection_rate: Total number of agents who are infected at the start of the simulation
            self.recovery_days: Number of days taken by an agent to recover if he gets infected
            self.dead_agents_number: variable to hold the total number of dead agents

            self.government_action_threshold: A threshold of infection rate after which the government imposes lockdown
            self.government_stringent: The strictness of the government after imposing lockdown

            self.quarantine_prob: The probability of an agent to quarantine after he gets infected

            self.habituation: the habituation of the agents - sensitivity to the change in stimulus of action
            self.learning_rate: learning rate of the agents - controls rate of change of aspiration level
            self.global_aspiration: initial global aspiration of the population
            self.action_infection_prob: Probability of getting infected for a particular action
        """
        self.population_density = 0.3
        self.death_rate = 0.02
        self.width = width
        self.height = height
        self.transfer_rate = 0.3
        self.initial_infection_rate = 0.02
        self.recovery_days = recovery_days
        self.dead_agents_number = 0

        self.government_action_threshold = government_action_threshold
        self.government_stringent = government_stringent

        self.lockdown = False

        self.quarantine_prob = 0.3

        self.habituation = habituation
        self.learning_rate = learning_rate
        self.global_aspiration = global_aspiration
        self.action_count = 4
        self.action_infection_prob = {
            "Stay In": 0.1,
            "Party": 0.7,
            "Buy grocery": 0.5,
            "Help elderly": 0.5
        }

        """graphing parameters"""

        self.step_counter = 0
        self.dilemma_list = []
        self.stay_in_list = []
        self.stay_out_list = []
        self.steps_list = []
        self.aspiration_list = []
        self.infection_list = []

        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        i = 0

        """Get all the cells in SingleGrid"""
        for cell in self.grid.coord_iter():
            x, y = cell[1], cell[2]

            """Add agents and infect them with initial infection rate"""

            if self.random.random() < self.population_density:
                agent = MainAgent(i, self, (x, y))

                if (np.random.choice([0, 1], p=[
                        1 - self.initial_infection_rate, self.initial_infection_rate])) == 1:
                    agent.infectionstate = InfectionState.INFECTED
                    agent.quarantinestate = QuarantineState.FREE
                    agent.infected_time = self.schedule.time

                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)
                i = i + 1

        self.total_population = i

        self.running = True

        self.datacollector = DataCollector(
            model_reporters={
                "Infected": get_infected_number,
                "Recovered": get_recovered_number,
                "Dead": get_dead_number,
                "Stay In": get_stay_in,
                "Go Out": get_go_out,
                "Susceptible": get_susceptible_number,
                "Aspiration": get_average_aspiration,
                "Average Aspiration": get_average_aspiration,
                "Average Stay In": get_average_stay_in,
                "Average Get Out": get_average_go_out,

            },

            agent_reporters={
                "QuarantineState": "quarantinestate",
                "InfectionState": "infectionstate",
            },
        )

    def save_csv(self, stay_in_list, stay_out_list,
                 steps_list, aspiration_list, infection_list):
        """Saves the CSVs for creating graphs.

        Returns : CSV for comparing aspiration and government strictness with columns
                steps, number of agents staying in, number of agents going out

                CSV for comparing infection numbers and strictness with columns
                steps, infection rate
        """
        if not os.path.exists('simulation'):
            os.makedirs('simulation')

        with open("simulation/dilemma_" + "aspiration_" + str(self.global_aspiration) + "_" + "stringent" + "_" + str(self.government_stringent) + ".csv", "w", newline='') as file:
            writer = csv.writer(file)
            rows = zip(steps_list, stay_in_list, stay_out_list)

            for row in rows:
                writer.writerow(row)

        with open("simulation/infection_number_" + "stringent_" + str(self.government_stringent) + ".csv", "w", newline='') as file:
            writer = csv.writer(file)
            rows = zip(steps_list, infection_list)

            for row in rows:
                writer.writerow(row)

    def step(self):
        """Runs the step function of simulation and stores the parameter values to save for CSV
        """

        self.step_counter = self.step_counter + 1

        self.datacollector.collect(self)
        self.schedule.step()

        stay_in_each_step = self.get_stay_in_number()
        stay_out_each_step = self.get_stay_out_number()
        avg_aspiration_each_step = self.get_avg_aspiration()
        infection_number_each_step = self.get_infection_number() / self.total_population

        if ((self.get_infection_number() / self.total_population)
                > self.government_action_threshold):

            self.lockdown = True

            self.stay_in_list.append(stay_in_each_step)
            self.stay_out_list.append(stay_out_each_step)
            self.steps_list.append(self.step_counter)
            self.aspiration_list.append(avg_aspiration_each_step)
            self.infection_list.append(infection_number_each_step)

        if ((self.get_recovered_number() + self.get_dead_number() + self.get_susceptible_number())
                == self.total_population):
            self.running = False
            self.save_csv(
                self.stay_in_list,
                self.stay_out_list,
                self.steps_list,
                self.aspiration_list,
                self.infection_list)

    def get_stay_in_number(self):
        """Get number of staying in agents, used for graphing and visualization

        Returns: the number of agents staying in at that particular step
        """
        try:
            stay_in_list = [
                a for a in self.schedule.agents if a.action_done[-1] == "Stay In"]
            return len(stay_in_list)
        except Exception:
            return 0

    def get_stay_out_number(self):
        """Get number of agents going out, used for graphing and visualization

        Returns: the number of agents going out at that particular step
        """
        try:
            stay_out_list = [
                a for a in self.schedule.agents if a.action_done[-1] != "Stay In"]
            return len(stay_out_list)
        except Exception:
            return 0

    def get_avg_aspiration(self):
        """Get average aspiration of the population, used for graphing and visualization

        Returns: the average population of the agents at that particular step
        """
        try:
            total_aspiration = 0
            for i, a in enumerate(self.schedule.agents):
                total_aspiration = total_aspiration + a.aspiration
            return (total_aspiration / i)
        except Exception:
            return 0

    def get_susceptible_number(self):
        """Get the number of agents that are susceptible to the virus, used for graphing and visualization

        Returns: number of agents that are susceptible to the virus until that step
        """
        susceptible_number = 0
        for cell in self.grid.coord_iter():
            if (cell[0] is not None):
                agent = cell[0]
                if (agent.infectionstate == InfectionState.CLEAN):
                    susceptible_number = susceptible_number + 1
        return susceptible_number

    def get_infection_number(self):
        """Get the number of agents that are infected to the virus, used for graphing and visualization

        Returns: number of agents that are infected to the virus until that step
        """

        infected_number = 0
        for cell in self.grid.coord_iter():
            if (cell[0] is not None):
                agent = cell[0]
                if (agent.infectionstate == InfectionState.INFECTED):
                    infected_number = infected_number + 1
        return infected_number

    def get_recovered_number(self):
        """Get the number of agents who recovered from the virus, used for graphing and visualization

        Returns: number of agents that recovered from the virus until that step
        """

        recovered_number = 0
        for cell in self.grid.coord_iter():
            if (cell[0] is not None):
                agent = cell[0]
                if (agent.infectionstate == InfectionState.RECOVERED):
                    recovered_number = recovered_number + 1
        return recovered_number

    def get_dead_number(self):
        """Get the number of agents who died from the virus, used for graphing and visualization

        Returns: number of agents that died from the virus until that step
        """
        return self.dead_agents_number


br_params = {
    "global_aspiration": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    "government_stringent": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
}

br = BatchRunner(
    MainModel,
    br_params,
    iterations=1,
    max_steps=1000,
)

if __name__ == "__main__":
    br.run_all()
