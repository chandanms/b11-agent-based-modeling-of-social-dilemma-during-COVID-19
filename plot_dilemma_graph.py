import csv
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import numpy as np


'''
TO DO : Give the csv and filesave name as arguments, automate the xaxis range.
'''

x_axis = []

# Give the range of the steps to plot

x = range(4, 19)

for i in x :
	x_axis.append(i)

stay_in_list = []
party_list = []
grocery_list = []
elderly_list = []

for i in  x :
	actions_list = []

	# Name of the csv file
	with open('simulations/dilemma_stringent_5.csv', newline='') as file :
		reader = csv.reader(file)
		for row in reader :
			if (int(row[0]) == i) :
				actions_list.append(row[1])

		stay_in_count = actions_list.count('Stay In')
		party_count = actions_list.count('Party')
		grocery_count = actions_list.count('Buy grocery')
		elderly_count = actions_list.count('Help elderly')

		print (stay_in_count, party_count, grocery_count, elderly_count)
		stay_in_list.append(stay_in_count)
		party_list.append(party_count)
		grocery_list.append(grocery_count)
		elderly_list.append(elderly_count)

print (stay_in_list, party_list, grocery_list, elderly_list)

plt.figure(figsize=[15, 10])

plt.xlabel('Steps')
plt.ylabel('Number of agents taking the action')


plt.plot(x_axis, stay_in_list, color='green', label="Stay In")
plt.plot(x_axis, party_list, color='red', label="Go party")
plt.plot(x_axis, grocery_list, color='blue', label="Go grocery")
plt.plot(x_axis, elderly_list, color='orange', label="Go help elderly")


# Name of the file saved

plt.legend()
plt.savefig('dilemma_stringent_5.pdf', bbox_inches='tight')
plt.show()



		