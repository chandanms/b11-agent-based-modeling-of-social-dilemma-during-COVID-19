import numpy as np


actions = ["stay_in", "go_out_grocery", "go_out_party", "go_out_help_elderly"]
actions_probability = {"stay_in" : 0.25, "go_out_grocery" : 0.25, "go_out_party" : 0.25, "go_out_help_elderly" : 0.25}
actions_payoff = {"stay_in" :0.5, "go_out_grocery" : 0.6, "go_out_party" : 0.7, "go_out_help_elderly" : 0.6}

aspiration = 0.5
learning_rate = 0.01
habituation = 0.4

for i in range(1000) :
	action_chosen = np.random.choice(list(actions_probability.keys()), p = list(actions_probability.values()))
	print (action_chosen)
	action_chosen_payoff = actions_payoff[action_chosen]
	stimulus = action_chosen_payoff - aspiration

	aspiration = aspiration*(1 - habituation) + habituation*action_chosen_payoff

	actions_probability_old = actions_probability[action_chosen]

	if stimulus > 0 :
		actions_probability[action_chosen] = actions_probability[action_chosen] + (1 - actions_probability[action_chosen])*learning_rate*stimulus
	else :
		actions_probability[action_chosen] = actions_probability[action_chosen] + actions_probability[action_chosen]*learning_rate*stimulus

	actions_probability_difference = actions_probability[action_chosen] - actions_probability_old


	actions_probability_difference_each = actions_probability_difference/3

	for key in list(actions_probability.keys()):
		if key != action_chosen :
			actions_probability[key] = actions_probability[key] - actions_probability_difference_each

	print (actions_probability)