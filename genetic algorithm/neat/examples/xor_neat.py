import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utility


if __name__ == "__main__":

	table = { (0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0 }
	performance = lambda decision, sensor: 1 - (decision - table[sensor])**2
	task = lambda decision, fitnessFunction, data: fitnessFunction(decision[0], data)

	structure = { "output_neurons": 1,
				  "input_neurons": 2,
				  "output_function": "step",
				  "maximum_layers": 0,
				  "minimum_layers": 0,
				  "maximum_weight": 2,
				  "minimum_weight": -2,
				  "maximum_neurons": 0,
				  "minimum_neurons": 0 }

	parameters = { "bias_rate": 0.5,
				   "connection_rate": 0.75,
				   "active_rate": 0.75,
				   "recurrent_rate": 0,
				   "skip_rate": 0.5,
				   "recurrent": False,
				   "skip": True }

	size = 50
	cluster = int(size / 10) if (size >= 20) else 2
	threshold = random.randint(10, 20)
	delta = threshold / 10**len(str(threshold))
	population = utility.initializeGeneration(size, structure, parameters)
	data = random.choice([(0, 0), (0, 1), (1, 0), (1, 1)])
	utility.evaluateFitness(population, data, task, performance)
	species = utility.speciation(population, threshold)
	if (len(species) < cluster): threshold -= delta
	elif (len(species) > cluster): threshold += delta
	else: delta = 0
	x = utility.crossover(species)
