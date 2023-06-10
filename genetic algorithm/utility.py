import random
import os
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

		if (target != None):

			check = (alpha["chromosome"] != target)

		else:

			check = (repeat < horizon["window"])

	if (task == "evolve"):

		initial = alpha.copy()

	else:

		beta = alpha.copy()

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

			if (target != None):

				if (alpha["chromosome"] == target):

					break

		else:

			if (target != None):

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

	if (task == "evolve"):

		data = [alpha, generation, initial]

	else:

		data = [alpha, generation]

	return data


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

	population = generatePopulation(chromosome_length = len(parameters["target"]) if (parameters["target"] != None) else parameters["chromosome_length"],
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

		if (target == None):

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


def generatePopulation(chromosome_length = 2,
					   population_size = 5,
					   category = "number",
					   genotype = "encoded",
					   gene_width = 1,
					   domain = None):

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

		if (mutation_number > len(chromosome)):

			mutation_number = len(chromosome)

	else:

		if (mutation_number > chromosome_length):

			mutation_number = chromosome_length

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


def heuristicAverage(dna, objective = "maximize"):

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
