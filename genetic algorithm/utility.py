import random
import os
import numpy as np
from constants import CHARACTERS


def evolve(parameters = None):

	population, \
	generations, \
	mutation_rate, \
	display, \
	loop, \
	horizon, \
	target, \
	task, \
	objective, \
	fitnessFunction, \
	dominanceFilter, \
	matchingProcedure, \
	memberEvolution, \
	mutation = extractParameters(parameters)
	portfolio = evaluateFitness(population, fitnessFunction, target)
	generation = 0
	repeat = 0

	if (objective == "maximize"):

		alpha = max(portfolio, key = lambda data: data["fitness"])

	else:

		alpha = min(portfolio, key = lambda data: data["fitness"])

	if loop:

		check = (generation < generations)

	else:

		if target is not None:

			check = (alpha["chromosome"] != target)

		else:

			check = (repeat < horizon["window"])

	if (task == "search"):

		beta = alpha.copy()

	initial = alpha.copy()
	os.system("cls")
	print()

	while check:

		report = evaluateFitness(population, fitnessFunction, target)
		DNA_pool = dominanceFilter(report)
		if matchingProcedure is not None: cluster = matchingProcedure(DNA_pool)
		else: cluster = evaluateFitness(DNA_pool, fitnessFunction, target)
		replication = memberEvolution(cluster)
		evolution = mutate(mutation, mutation_rate, replication)
		portfolio = evaluateFitness(evolution, fitnessFunction, target)
		population = evolution.copy()
		generation += 1

		if (objective == "maximize"):

			alpha = max(portfolio, key = lambda data: data["fitness"])

		else:

			alpha = min(portfolio, key = lambda data: data["fitness"])

		if loop:

			check = (generation < generations)

			if target is not None:

				if (alpha["chromosome"] == target):

					break

		else:

			if target is not None:

				check = (alpha["chromosome"] != target)

			else:

				if (abs(alpha["fitness"] - beta["fitness"]) <= horizon["tolerance"]):

					repeat += 1

				else:

					repeat = 0

				beta = alpha.copy()
				check = (repeat < horizon["window"])

		if display:

			print(f"\nGeneration: { generation }")
			print(f"Best candidate: { alpha['chromosome'] }")
			print(f"Fitness: { alpha['fitness'] }")
			print(f"Population fitness: { sum([member['fitness'] for member in portfolio]) / len(portfolio) }")

	return alpha, generation, initial


def extractParameters(parameters):

	hyperparameters = { "population_size": 100,
					    "function": wordScore,
					    "category": "number",
					    "genotype": "base",
					    "chromosome_length": 2,
					    "gene_width": 1,
					    "generations": 1000,
					    "mutation_rate": 0.1,
						"target": None,
						"task": "evolve",
						"objective": "maximize",

					    "horizon": { "window": 10,
									 "tolerance": 1e-2 },

					    "domain": { "minimum": -1,
					    			"maximum": 1 },

					    "funnel": { "function": randomSelection,
					    			"arguments": { "duplication_indicator": True,
								    			   "clone_flag": False,
								    			   "group_size": 2 } },

					    "pairing": { "function": None,
					    			 "arguments": { "group_size": 2,
					    			 				"strategy": "random",
					    			 				"chaos": False } },

					    "mutator": { "function": randomMutation,
					    			 "arguments": { "mutation_number": 1,
					    			 				"domain": None,
					    			 				"chromosome_length": 1 } },

					    "combination": { "function": linearAverage,
					    				 "arguments": { "chromosome_length": 1 } },
					    "loop": True,
					    "display": False }

	if parameters is None:

		parameters = hyperparameters

	else:

		parameters = { **hyperparameters, **parameters }

	if (parameters["population_size"] <= 1):

		parameters["population_size"] = 2

	population = generatePopulation(chromosome_length = len(parameters["target"]) if (parameters["target"] is not None) else parameters["chromosome_length"],
								    population_size = parameters["population_size"],
								    category = parameters["category"],
								    genotype = parameters["genotype"],
								    gene_width = parameters["gene_width"],
								    domain = parameters["domain"])

	fitnessFunction = parameters["function"]

	if parameters["funnel"]["arguments"] is not None:

		dominanceFilter = lambda generation: parameters["funnel"]["function"](generation, **parameters["funnel"]["arguments"])

	else:

		dominanceFilter = lambda generation: parameters["funnel"]["function"](generation)

	if parameters["pairing"]["arguments"] is not None:

		matchingProcedure = lambda generation: parameters["pairing"]["function"](generation, **parameters["pairing"]["arguments"])

	else:

		if parameters["pairing"]["function"] is not None:

			matchingProcedure = lambda generation: parameters["pairing"]["function"](generation, **parameters["pairing"]["arguments"])

		else:

			matchingProcedure = parameters["pairing"]["function"]

	if parameters["combination"]["arguments"] is not None:

		memberEvolution = lambda generation: parameters["combination"]["function"](generation, **parameters["combination"]["arguments"])

	else:

		memberEvolution = lambda generation: parameters["combination"]["function"](generation)

	if parameters["mutator"]["arguments"] is not None:

		mutation = lambda generation: parameters["mutator"]["function"](generation, **parameters["mutator"]["arguments"])

	else:

		mutation = lambda generation: parameters["mutator"]["function"](generation, **parameters["mutator"]["arguments"])

	return [population,
		    parameters["generations"],
		    parameters["mutation_rate"],
		    parameters["display"],
		    parameters["loop"],
		    parameters["horizon"],
		    parameters["target"],
		    parameters["task"],
		    parameters["objective"],
		    fitnessFunction,
		    dominanceFilter,
		    matchingProcedure,
		    memberEvolution,
		    mutation]


def evaluateFitness(population, fitness, target = None):

	portfolio = []

	for member in population:

		if target is None:

			score = fitness(member)

		else:

			score = fitness(member, target)

		portfolio.append({ "chromosome": member,
						   "fitness": score })

	return portfolio


def mutate(mutationFunction, mutation_rate, population):

	generation = []

	for member in population:

		if (random.random() < mutation_rate):

			mutant = mutationFunction(member)

		else:

			if (type(member) in (tuple, list, str)):

				mutant = member[:]

			else:

				mutant = member

		generation.append(mutant)

	return generation


def generatePopulation(chromosome_length = 2, population_size = 5, category = "number", genotype = "encoded", gene_width = 1, domain = None):

	if (domain is None):

		domain = { "minimum": -10,
	   			   "maximum": 10 }

	population = []
	random.shuffle(CHARACTERS)
	symbol = ("character", "binary")
	# random.seed(42)

	while (len(population) < population_size):

		if (genotype == "encoded"):

			if (category in symbol):

				chromosome = ""
				gene = ""

			else:

				chromosome = ()

			while (len(chromosome) < chromosome_length):

				if (category == "integer"):

					gene = random.randint(domain["minimum"], domain["maximum"])

				elif (category == "character"):

					while (len(gene) < gene_width):

						gene += random.choice(CHARACTERS)

				elif (category == "binary"):

					while (len(gene) < gene_width):

						gene += random.choice(("0", "1"))

				else:

					gene = random.uniform(domain["minimum"], domain["maximum"])

				chromosome = (*chromosome, gene)

		else:

			if (category in symbol):

				chromosome = ""

			if (category == "integer"):

				chromosome = random.randint(domain["minimum"], domain["maximum"])

			elif (category == "character"):

				while (len(chromosome) < chromosome_length):

					chromosome += random.choice(CHARACTERS)

			elif (category == "binary"):

				while (len(chromosome) < chromosome_length):

					chromosome += random.choice(("0", "1"))

			else:

				chromosome = random.uniform(domain["minimum"], domain["maximum"])

		population.append(chromosome)

	return population


def neuralNetwork(architecture):

	network = []

	for layer in range(len(architecture) - 1):

		flag = architecture[layer + 1]["bias"]
		forward = architecture[layer + 1]["nodes"]
		current = architecture[layer]["nodes"]
		if flag: current += 1
		weights = np.random.uniform(-2, 2, (forward, current))
		network.append(weights)

	return network


def matchBranches(genome, threshold):

	matrix_a = random.choice(genome)
	clone = genome.copy()
	clone.remove(matrix_a)
	matrix_b = random.choice(clone)
	branch_a = random.choice(matrix_a)

	while (branch_a["type"] == "bias"):

		branch_a = random.choice(matrix_a)

	while (branch_b := random.choice(matrix_b))["type"] == "bias": pass
	input_node_a = branch_a["input_node"]
	output_node_a = branch_a["output_node"]
	input_node_b = branch_b["input_node"]
	output_node_b = branch_b["output_node"]
	input_layer_a = branch_a["input_layer"]
	output_layer_a = branch_a["output_layer"]
	input_layer_b = branch_b["input_layer"]
	output_layer_b = branch_b["output_layer"]

	if (random.random() < threshold):

		weight_a = branch_a["weight"]
		weight_b = branch_b["weight"]
		weight = weight_a*weight_b + weight_a + weight_b
		branch_a["active"] = False
		branch_b["active"] = False

	else:

		weight = random.uniform(-2, 2)

	return [genome,
			weight,
			input_node_a,
		    input_layer_a,
		    output_node_a,
		    output_layer_a,
		    input_node_b,
		    input_layer_b,
		    output_node_b,
		    output_layer_b]


def matchNodes(genome, cascade, threshold = 0.25):

	genome, \
	weight, \
	input_node_a, \
	input_layer_a, \
	output_node_a, \
	output_layer_a, \
	input_node_b, \
	input_layer_b, \
	output_node_b, \
	output_layer_b = matchBranches(genome, threshold)

	if (len(cascade) > 0):

		while any((((synapse["input_node"] == input_node_a) and (synapse["output_node"] == output_node_b)) or
				   ((synapse["input_node"] == input_node_b) and (synapse["output_node"] == output_node_a)) or
				   ((synapse["input_node"] == output_node_a) and (synapse["output_node"] == input_node_b)) or
				   ((synapse["input_node"] == output_node_b) and (synapse["output_node"] == input_node_a))) for synapse in cascade):

			genome, \
			weight, \
			input_node_a, \
			input_layer_a, \
			output_node_a, \
			output_layer_a, \
			input_node_b, \
			input_layer_b, \
			output_node_b, \
			output_layer_b = matchBranches(genome, threshold)

	output_layer = max(output_layer_a, output_layer_b)
	input_layer = min(input_layer_a, input_layer_b)
	output_node = output_node_a if (output_layer == output_layer_a) else output_node_b
	input_node = input_node_a if (input_layer == input_layer_a) else input_node_b
	return genome, input_node, input_layer, output_node, output_layer, weight


def modifyGenome(genome, topology, threshold = 0.25, recurrent = False):

	if (len(genome) > 1):

		size = sum(len(gene) for gene in genome)
		cascade = tuple()

		for index in range(size):

			if (random.random() < threshold):

				genome, \
				input_node, \
				input_layer, \
				output_node, \
				output_layer, \
				weight = matchNodes(genome, cascade, threshold)

				if (recurrent & (random.random() < threshold)):

					variable = output_layer
					output_layer = input_layer
					input_layer = variable
					variable = output_node
					output_node = input_node
					input_node = variable

				branch = ({ "input_node": input_node,
						    "output_node": output_node,
						    "input_layer": input_layer,
						    "output_layer": output_layer,
						    "weight": weight,
						    "type": "synapse",
						    "connection": "skip" if (abs(output_layer - input_layer) > 1) else "consecutive",
						    "direction": "inverse" if (output_layer < input_layer) else "forward",
						    "active": True},)

				cascade += branch

		genome.append(cascade)

	for matrix in genome:

		for dna in matrix:

			if (random.random() < threshold):

				dna["active"] = False

			if ((random.random() < threshold) and
				(dna["type"] == "synapse") and
				recurrent):

				dna["direction"] = "inverse"
				variable = dna["input_node"]
				dna["input_node"] = dna["output_node"]
				dna["output_node"] = variable
				variable = dna["input_layer"]
				dna["input_layer"] = dna["output_layer"]
				dna["output_layer"] = variable

	return genome


def encodeNetwork(network, architecture, topology, history = [], initialize = False):

	branch = tuple()
	genome = []

	for index, matrix in enumerate(network):

		for row in range(matrix.shape[0]):

			for column in range(matrix.shape[1]):

				weight = { "input_node": topology[index][column]["node"],
						   "output_node": topology[index + 1][row]["node"],
						   "weight": matrix[row, column],
						   "active": True,
						   "direction": "forward",
						   "connection": "consecutive",
						   "type": "bias" if (architecture[index + 1]["bias"] and (column == matrix.shape[1] - 1)) else "synapse",
						   "input_layer": index,
						   "output_layer": index + 1 }

				if initialize:

					history, identity = manageHistory(history, weight)
					weight["innovation"] = identity

				branch += (weight,)

		genome.append(branch)
		branch = tuple()

	return genome


def populateLUT(genome):

	history = []

	for index, matrix in enumerate(genome):

		for weight in matrix:

			history, innovation = manageHistory(history, weight)
			weight["innovation"] = innovation

	return history, genome


def manageHistory(history, weight):

	innovation = len(history)
	fields = ("input_node", "output_node", "type", "active", "direction", "connection", "innovation")

	if (len(history) > 0):

		if "innovation" not in weight:

			if not any(((synapse["input_node"] == weight["input_node"]) and
						(synapse["output_node"] == weight["output_node"]) and
						(synapse["connection"] == weight["connection"]) and
						(synapse["type"] == weight["type"]) and
						(synapse["active"] == weight["active"]) and
						(synapse["direction"] == weight["direction"])) for synapse in history):

				candidate = { key: value for key, value in weight.items() if key in fields }
				innovation = len(history) + 1
				# innovation = max(history, key = lambda gene: gene["innovation"]) + 1
				candidate["innovation"] = innovation
				history.append(candidate)

		else:

			if not any((synapse["innovation"] == weight["innovation"]) for synapse in history):

				candidate = { key: value for key, value in weight.items() if key in fields }
				history.append(candidate)

	else:

		innovation = 1
		candidate = { key: value for key, value in weight.items() if key in fields }
		candidate["innovation"] = innovation
		history.append(candidate)

	# history = sorted(history, key = lambda dna: dna["innovation"])
	return history, innovation


def decodeGenome(genome, architecture, topology):

	network = []
	groups = []
	consecutive = genome[:-1]

	for index, layer in enumerate(consecutive):

		current = architecture[index]["nodes"]
		forward = architecture[index + 1]["nodes"]
		bias = architecture[index + 1]["bias"]
		vector = [gene["weight"] for gene in layer]
		if bias: current += 1
		matrix = np.reshape(vector, (forward, current))
		network.append(matrix)

	if (len(genome) > len(architecture) - 1):

		skip = genome[-1]

		for synapse in skip:

			if (synapse["type"] != "bias"):

				if (len(groups) > 0):

					if any(((synapse["input_layer"] == weight["input_layer"]) and
							(synapse["output_layer"] == weight["output_layer"])) for weight in groups):

						group = next((weight for weight in groups if ((weight["input_layer"] == synapse["input_layer"]) and (weight["output_layer"] == synapse["output_layer"]))), None)
						group["weights"].append(synapse)

					else:

						branch = { "input_layer": synapse["input_layer"],
								   "output_layer": synapse["output_layer"],
								   "weights": [synapse] }

						groups.append(branch)

				else:

					branch = { "input_layer": synapse["input_layer"],
							   "output_layer": synapse["output_layer"],
							   "weights": [synapse] }

					groups.append(branch)

		for index, group in enumerate(groups):

			input_layer = group["input_layer"]
			output_layer = group["output_layer"]
			output_size = len(topology[output_layer])
			input_size = len(topology[input_layer])

			if any((node["type"] == "bias") for node in topology[input_layer]):

				input_size -= 1

			if any((node["type"] == "bias") for node in topology[output_layer]):

				output_size -= 1

			matrix = np.zeros((output_size, input_size))

			for weight in group["weights"]:

				row = next((position for position, neuron in enumerate(topology[output_layer]) if (neuron["node"] == weight["output_node"])), None)
				column = next((position for position, neuron in enumerate(topology[input_layer]) if (neuron["node"] == weight["input_node"])), None)
				matrix[row, column] = weight["weight"]

			network.append(matrix)

	return network


def networkStructure(architecture):

	topology = []

	for layer in range(len(architecture)):

		if (len(topology) == 0):

			nodes = tuple({ "node": node + 1, "type": "neuron" } for node in range(architecture[layer]["nodes"]))

		else:

			nodes = tuple({ "node": topology[-1][-1]["node"] + node + 1, "type": "neuron" } for node in range(architecture[layer]["nodes"]))

		if (layer < len(architecture) - 1):

			if architecture[layer + 1]["bias"]:

				nodes += ({ "node": nodes[-1]["node"] + 1, "type": "bias" },)

		topology.append(nodes)

	return topology


def feedForward(data, network, architecture):

	activity = data.copy()

	for layer, neuron in enumerate(network):

		flag = architecture[layer + 1]["bias"]

		if flag:

			activity = np.vstack((activity, 1))

		output = neuron.dot(activity)
		activity = activation(output, architecture[layer + 1]["function"])

	return activity


def processor(data, network, architecture):

	activity = data.copy()

	for layer, neuron in enumerate(network):

		flag = architecture[layer + 1]["bias"]

		if flag:

			activity = np.vstack((activity, 1))

		output = neuron.dot(activity)
		activity = activation(output, architecture[layer + 1]["function"])

	return activity


def activation(data, function = "sigmoid"):

	if (function.lower().lstrip().rstrip() == "sigmoid"):

		return 1 / (1 + np.exp(-data))

	elif (function.lower().lstrip().rstrip() == "tanh"):

		return np.tanh(data)

	elif (function.lower().lstrip().rstrip() == "relu"):

		return np.maximum(data, 0)

	elif (function.lower().lstrip().rstrip() == "step"):

		return np.sign(data)

	return data


def wordScore(chromosome, target):

	wordAssertion(chromosome, target)
	delta = len(chromosome) - len(target)
	score = 0

	if (delta == 0):

		for gene, character in zip(chromosome, target):

			if (gene == character):

				score += 1

	return score**2


def randomSelection(generation,
					duplication_indicator = True,
					clone_flag = False,
					group_size = 2):

	random.shuffle(generation)
	candidate_pool = generation.copy()
	suspend = 0
	table = []

	if not(duplication_indicator):

		table = candidate_pool.copy()

	else:

		while (len(table) < len(generation)):

			candidate = random.choice(candidate_pool)
			table.append(candidate)

			if not(clone_flag):

				if (suspend < group_size):

					candidate_pool.remove(candidate)
					suspend += 1

				else:

					suspend = 0

					for parent in table[-group_size:]:

						candidate_pool.append(parent)

	return table


def symbolMatching(dna, strategy = "random", group_size = 2, chaos = False):

	mixing_cluster = []
	group_number = len(dna) // group_size
	DNA = dna.copy()

	if (not(chaos) and (strategy == "random")):

		random.shuffle(DNA)

	while (len(mixing_cluster) < group_number):

		if (chaos and (strategy == "random")):

			random.shuffle(DNA)

		mixing_cluster.append(DNA[0:group_size])
		DNA = DNA[group_size:]

	if (len(DNA) > 0):

		mixing_cluster.append(DNA.copy())

	return mixing_cluster


def pointCrossOver(cluster, chromosome_length = 1):

	generation = []

	for group in cluster:

		point = random.randint(0, len(group[0]) - 1)

		if (len(group) == 1):

			clone = forcedMutation(group[0], chromosome_length)
			generation.append(clone)

		else:

			clones = swapAllele(group, point)
			generation.extend(clones)

	return generation


def swapAllele(parents, point):

	clones = []
	section = parents[-1][(point + 1):]

	for parent in parents:

		block = parent[0:(point + 1)]
		allele = parent[(point + 1):]
		clone = block + section
		clones.append(clone)
		section = allele

	return clones


def forcedMutation(chromosome, chromosome_length = 1):

	if (type(chromosome) not in (int, float)):

		if (random.random() >= 0.5):

			variant = shuffleMutation(chromosome)

		else:

			variant = randomMutation(chromosome, 1, None, chromosome_length)

	else:

		variant = randomMutation(chromosome, 1, None, chromosome_length)

	return variant


def shuffleMutation(chromosome):

	if (len(chromosome) > 1):

		point_a = random.randint(0, len(chromosome) - 1)
		gene_a = chromosome[point_a]
		point_b = random.randint(0, len(chromosome) - 1)

		while (point_b == point_a):

			point_b = random.randint(0, len(chromosome) - 1)

		gene_b = chromosome[point_b]

		if (type(chromosome) != list):

			buffer = list(chromosome)

		else:

			buffer = chromosome.copy()

		buffer[point_a] = gene_b
		buffer[point_b] = gene_a

		if (type(chromosome) != list):

			if (type(chromosome) == str):

				chromosome = "".join(buffer)

			else:

				chromosome = type(chromosome)(buffer)

		else:

			chromosome = buffer.copy()

	return chromosome


def randomMutation(chromosome, mutation_number = 1, domain = None, chromosome_length = 1):

	if domain is None:

		domain = { "minimum": -1,
				   "maximum": 1 }

	if (type(chromosome) in (tuple, list, str)):

		mutation_number = min(mutation_number, len(chromosome))

	else:

		mutation_number = min(mutation_number, chromosome_length)

	if (type(chromosome) in (str, int, float)):

		condition = (type(chromosome) is str)

	else:

		condition = (type(chromosome[0]) is str)

	if condition:

		defects = random.sample(range(0, len(chromosome)), mutation_number)

		if (type(chromosome) != list):

			buffer = list(chromosome)

		else:

			buffer = chromosome.copy()

		for index in defects:

			if (all(gene.isdigit() for gene in chromosome) and
				all(gene in ("0", "1") for gene in chromosome)):

				bits = ["0", "1"]
				bits.remove(buffer[index])
				value = bits[0]

			else:

				CHARACTERS.remove(buffer[index])
				value = random.choice(CHARACTERS)
				CHARACTERS.append(buffer[index])

			buffer[index] = value

		if (type(chromosome) != list):

			if (type(chromosome) == str):

				chromosome = "".join(buffer)

			else:

				chromosome = type(chromosome)(buffer)

		else:

			chromosome = buffer.copy()

	else:

		if (type(chromosome) == int):

			chromosome += random.randint(domain["minimum"], domain["maximum"])

		elif (type(chromosome) == float):

			chromosome += random.uniform(domain["minimum"], domain["maximum"])

		else:

			defects = random.sample(range(0, len(chromosome)), mutation_number)

			if (type(chromosome) != list):

				buffer = list(chromosome)

			else:

				buffer = chromosome.copy()

			for index in defects:

				if all(isinstance(value, int) for value in chromosome):

					buffer[index] += random.randint(domain["minimum"], domain["maximum"])

				else:

					buffer[index] += random.uniform(domain["minimum"], domain["maximum"])

			if (type(chromosome) != list):

				chromosome = type(chromosome)(buffer)

			else:

				chromosome = chromosome.copy()

	return chromosome


def linearAverage(cluster, chromosome_length = 1):

	generation = []

	for group in cluster:

		if (len(group) > 1):

			if (type(group[0]) in (int, float)):

				gamma = random.random()
				parent_a = group[0]
				parent_b = group[1]
				offspring_a = gamma*parent_a + (1 - gamma)*parent_b
				offspring_b = gamma*parent_b + (1 - gamma)*parent_a
				generation.extend((offspring_a, offspring_b))

			else:

				parent_a = group[0]
				parent_b = group[1]
				child_a = []
				child_b = []

				for member_a, member_b in zip(parent_a, parent_b):

					gamma = random.random()
					offspring_a = gamma*member_a + (1 - gamma)*member_b
					offspring_b = gamma*member_b + (1 - gamma)*member_a
					child_a.append(offspring_a)
					child_b.append(offspring_b)

				child_a = type(group[0])(child_a)
				child_b = type(group[0])(child_b)
				generation.extend((child_a, child_b))

		else:

			if (type(group[0]) in (tuple, list)):

				offspring = randomMutation(group[0], 1, None, len(group[0]))

			else:

				offspring = randomMutation(group[0], 1, None, chromosome_length)

			generation.append(offspring)

	return generation


def heuristicAverage(dna, objective = "maximize", chromosome_length = 1):

	generation = []

	while (len(generation) < len(dna)):

		if (len(dna) > 1):

			if (type(dna[0]["chromosome"]) in (int, float)):

				gamma = random.random()
				member_a = random.choice(dna)
				dna.remove(member_a)
				member_b = random.choice(dna)
				dna.append(member_a)
				member = [member_a, member_b]

				if (objective == "maximize"):

					parent_b = max(member, key = lambda chromosome: chromosome["fitness"])
					member.remove(parent_b)
					parent_a = member[0]

				else:

					parent_b = min(member, key = lambda chromosome: chromosome["fitness"])
					member.remove(parent_b)
					parent_a = member[0]

				offspring = gamma*(parent_a["chromosome"] - parent_b["chromosome"]) + parent_b["chromosome"]
				generation.append(offspring)

			else:

				gamma = random.random()
				member_a = random.choice(dna)
				dna.remove(member_a)
				member_b = random.choice(dna)
				dna.append(member_a)
				child = []

				for a, b in zip(member_a, member_b):

					member = [a, b]

					if (objective == "maximize"):

						parent_b = max(member, key = lambda chromosome: chromosome["fitness"])
						member.remove(parent_b)
						parent_a = member[0]

					else:

						parent_b = min(member, key = lambda chromosome: chromosome["fitness"])
						member.remove(parent_b)
						parent_a = member[0]

					offspring = gamma*(parent_a["chromosome"] - parent_b["chromosome"]) + parent_b["chromosome"]
					child.append(offspring)

				child = type(member_a["chromosome"])(child)
				generation.append(child)

		else:

			if (type(dna[0]["chromosome"]) in (tuple, list)):

				offspring = randomMutation(dna[0]["chromosome"], 1, None, len(dna[0]["chromosome"]))

			else:

				offspring = randomMutation(dna[0]["chromosome"], 1, None, chromosome_length)

			generation.append(offspring)

	return generation


def tournamentSelection(generation, size = 2, chromosome_length = 1, objective = "maximize"):

	if all((member["chromosome"] == generation[0]["chromosome"]) for member in generation[1:]):

		table = [forcedMutation(candidate["chromosome"], chromosome_length) for candidate in generation]

	else:

		table = []
		competition = filterDuplicates(generation)

		if (size > len(competition)):

			size = len(competition)

		while (len(table) < len(generation)):

			tournament = random.sample(competition, size)

			if (objective == "maximize"):

				candidate = max(tournament, key = lambda chromosome: chromosome["fitness"])

			else:

				candidate = min(tournament, key = lambda chromosome: chromosome["fitness"])

			table.append(candidate["chromosome"])

	return table


def filterDuplicates(population):

	unique = []

	for member in population:

		if member not in unique:

			unique.append(member)

	return unique


def rouletteWheelSelection(generation, chromosome_length = 1):

	if (all((member["fitness"] == 0) for member in generation) or
		all((member["chromosome"] == generation[0]["chromosome"]) for member in generation[1:])):

		table = [forcedMutation(candidate["chromosome"], chromosome_length) for candidate in generation]

	else:

		roulette = filterDuplicates(generation)
		wheel = splitLine(roulette)
		table = []

		while (len(table) < len(generation)):

			point = random.random()

			for index, member in enumerate(wheel):

				if (index == 0):

					if ((point >= member["interval"][0]) and
						(point < member["interval"][1])):

						candidate = member["chromosome"]
						break

				elif (index == len(wheel) - 1):

					if ((point > member["interval"][0]) and
						(point <= member["interval"][1])):

						candidate = member["chromosome"]
						break

				else:

					if ((point > member["interval"][0]) and
						(point < member["interval"][1])):

						candidate = member["chromosome"]
						break

			table.append(candidate)

	return table


def splitLine(participants):

	line, initial = [], 0

	if any((member["fitness"] < 0) for member in participants):

		participants = offsetFitness(participants)

	participants = [member for member in participants if (member["fitness"] > 0)]
	total = sum([member["fitness"] for member in participants])

	for member in participants:

		final = initial + member["fitness"] / total
		line.append({ "chromosome": member["chromosome"],
					  "interval": (initial, final) })
		initial = final

	return line


def proportionalSelection(generation, chromosome_length = 1):

	if (all((member["fitness"] == 0) for member in generation) or
		all((member["chromosome"] == generation[0]["chromosome"]) for member in generation[1:])):

		table = [forcedMutation(candidate["chromosome"], chromosome_length) for candidate in generation]

	else:

		table = []
		participants = filterDuplicates(generation)
		bag = fillBag(participants)

		while (len(table) < len(generation)):

			candidate = random.choice(bag)
			table.append(candidate)

	return table


def fillBag(participants):

	if any((member["fitness"] < 0) for member in participants):

		participants = offsetFitness(participants)

	bag = []
	participants = [member for member in participants if member["fitness"] > 0]
	minimum = min(participants, key = lambda data: data["fitness"])

	for member in participants:

		factor = member["fitness"] / minimum["fitness"]

		if (factor > 50):

			factor = 50

		elif (factor < 1):

			factor = 1

		bag.extend([member["chromosome"] for _ in range(int(abs(factor)))])

	random.shuffle(bag)
	return bag


def offsetFitness(participants):

	minimum = min(participants, key = lambda data: data["fitness"])

	for member in participants:

		member["fitness"] += abs(minimum["fitness"])

		if (member["fitness"] == 0):

			member["fitness"] = 1

	return participants


def normalizeFitness(participants):

	minimum = min(participants, key = lambda data: data["fitness"])
	maximum = max(participants, key = lambda data: data["fitness"])

	for member in participants:

		member["fitness"] = 1 + 99*abs(member["fitness"] - minimum["fitness"]) / abs(maximum["fitness"] - minimum["fitness"])

		if (member["fitness"] > 100):

			member["fitness"] = 100

	return participants


def invertFitness(participants):

	minimum = min(participants, key = lambda data: data["fitness"])
	maximum = max(participants, key = lambda data: data["fitness"])

	for member in participants:

		member["fitness"] = maximum["fitness"] + minimum["fitness"] - member["fitness"]

	return participants


def wordAssertion(chromosome, target):

	allowed = (str, list, tuple)

	assert ((type(chromosome) in allowed) and
			(type(target) in allowed)), \
			f"Both the input string and the target word must be of type 'str', 'list' or 'tuple', but got '{type(chromosome).__name__}' and '{type(target).__name__}'."
