# Agent based modelling of Social Dilemma during Covid19


![screenshot](https://user-images.githubusercontent.com/24457135/98160799-037d0f80-1edf-11eb-8f88-3c8aa1ad8a2d.png)

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Run multiple simulations](#run-multiple-simulations)
  * [Create graphs](#create-graphs)
* [Contact](#contact)
* [Acknowledgements and references](#acknowledgements-and-references)



<!-- ABOUT THE PROJECT -->
## About The Project

This repository is a simulation of social dilemma in covid19 situation. The project is inspired by the paper "[Learning Dynamics in Social dilemma](https://www.pnas.org/content/99/suppl_3/7229)" 

The project runs the agent based simulation of covid19 to analyse the dilemma. We do this by observing the number of agents staying in and going out during the simulation. Here are few of the key aspects we analyse,

* Effect of aspiration levels on agent's action of staying in and going out.
* Effect of involvement of government body on the actions of agents.
* The overall infection spread depending on the strictness of the government.
* Effect of low and high habituation levels of the agents

A list of commonly used resources that we found helpful are listed in the acknowledgements.

### Built With

* [Python 3.6](https://www.python.org/)
* [Mesa](https://mesa.readthedocs.io/en/stable/)


<!-- GETTING STARTED -->
## Getting Started

We used Python 3.6 to run the project.


### Prerequisites

The following libraries are used in Python to run the project


* mesa 0.8.7
* numpy 1.19.1
* csv 1.0
* matplotlib 3.3.1
* seaborn 0.11.0
* pandas 1.1.1


### Installation

1. Clone the repo
```sh
git clone https://github.com/chandanms/b11-agent-based-modeling-of-social-dilemma-during-COVID-19.git
```
2. Alternatively, install the required libraries using requirements text given in the repo.
```sh
pip install -r requirements.txt
```



## Usage

Inside the cloned repo, run

```sh
mesa runserver
```

In the server browser, you can use the slider to give the parameters and observe the change in actions of agents in the graph display of the browser.

### Run multiple simulations

Multiple simulations for varying parameters can be run by,

```sh
python batch_run.py
```

This creates a folder called 'simulation' and stores CSV for graphing.

### Create graphs

Running this file generates 5 graphs.

1. The line plot facet graph for number of agents staying in and going out for aspiration levels of 0.1, 0.5 and 0.9 with no government involvement.
2. The line plot facet graph for number of agents staying in and going out for aspiration levels of 0.1, 0.5 and 0.9 with government strictness of 0.1
3. The line plot facet graph for number of agents staying in and going out for aspiration levels of 0.1, 0.5 and 0.9 with government strictness of 0.5
4. The line plot facet graph for number of agents staying in and going out for aspiration levels of 0.1, 0.5 and 0.9 with government strictness of 0.9
5. Heatmap of infection number for the government strictness ranging from 0 to 0.9 against the steps of simulation.

To obtain the graphs, run 

```sh
python batch_run.py
```
After the CSVs are created, run

```sh
python plot_graph.py
```

<!-- CONTACT -->
## Contact

Anjali Nair - a.nair4@student.rug.nl  
Chandan M S - c.m.sreedhara@student.rug.nl  
Nishchal Madiraju - n.madiraju@student.rug.nl  
Zulaikha Latief - z.latief@student.rug.nl  

Project Link: [https://github.com/chandanms/b11-agent-based-modeling-of-social-dilemma-during-COVID-19](https://github.com/chandanms/b11-agent-based-modeling-of-social-dilemma-during-COVID-19)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements and references
* [Main reference Paper - Learning Dynamics in Social Dilemma](https://www.pnas.org/content/99/suppl_3/7229)
* [Mesa documentations and Tutorials](https://mesa.readthedocs.io/en/stable/tutorials/intro_tutorial.html)
* [Pandas documentation for data storage](https://pandas.pydata.org/docs/)
* [Seaborn documentation for graphing](https://seaborn.pydata.org/)
