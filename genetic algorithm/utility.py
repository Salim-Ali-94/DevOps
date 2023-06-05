import random
import os
from constants import CHARACTERS


def evolve(target, parameters = None):

	population, \
	generations, \
	mutation_rate, \
	display, \
	loop, \
	fitnessFunction, \
	dominanceFilter, \
	matchingProcedure, \
	memberEvolution, \
	mutation = extractParameters(target, parameters)
	portfolio = evaluateFitness(population, fitnessFunction, target)
	alpha = max(portfolio, key = lambda data: data["fitness"])
	initial = alpha.copy()
	generation = 0

	if loop:

		check = (generation < generations)

	else:

		check = (alpha["chromosome"] != target)

	os.system("cls")
	print()

	while check:

		report = evaluateFitness(population, fitnessFunction, target)
		DNA_pool = dominanceFilter(report)
		cluster = matchingProcedure(DNA_pool)
		replication = memberEvolution(cluster)
		evolution = mutate(mutation, mutation_rate, replication)
		portfolio = evaluateFitness(evolution, fitnessFunction, target)
		alpha = max(portfolio, key = lambda data: data["fitness"])
		population = evolution.copy()
		generation += 1

		if loop:

			check = (generation < generations)

		else:

			check = (alpha["chromosome"] != target)

		if (alpha["chromosome"] == target):

			break

		if display:

			print(f"\nGeneration: { generation }")
			print(f"Best candidate: { alpha['chromosome'] }")
			print(f"Fitness: { alpha['fitness'] }")
			print(f"Population fitness: { sum([member['fitness'] for member in portfolio]) / len(portfolio) }")

	return alpha, generation, initial


def extractParameters(target, parameters):

	hyperparameters = { "population_size": 100,
					    "function": wordScore,
					    "category": "number",
					    "genotype": "base",
					    "generations": 1000,
					    "mutation_rate": 0.1,

					    "funnel": { "function": randomSelection,
					    			"arguments": { "duplication_indicator": True,
								    			   "clone_flag": False,
								    			   "group_size": 2 } },

					    "pairing": { "function": symbolMatching,
					    			 "arguments": { "group_size": 2,
					    			 				"strategy": "random",
					    			 				"chaos": False } },

					    "mutator": { "function": randomMutation,
					    			 "arguments": { "mutation_number": 1 } },

					    "combination": { "function": linearAverage,
					    				 "arguments": None },
					    "loop": True,
					    "display": False }

	if parameters is None:

		parameters = hyperparameters

	else:

		parameters = { **hyperparameters, **parameters }

	if (parameters["population_size"] <= 1):

		parameters["population_size"] = 2

	population = generatePopulation(chromosome_length = len(target),
								    population_size = parameters["population_size"],
								    category = parameters["category"],
								    genotype = parameters["genotype"])

	fitnessFunction = parameters["function"]

	if parameters["funnel"]["arguments"] is not None:

		dominanceFilter = lambda generation: parameters["funnel"]["function"](generation, **parameters["funnel"]["arguments"])

	else:

		dominanceFilter = lambda generation: parameters["funnel"]["function"](generation)

	if parameters["pairing"]["arguments"] is not None:

		matchingProcedure = lambda generation: parameters["pairing"]["function"](generation, **parameters["pairing"]["arguments"])

	else:

		matchingProcedure = lambda generation: parameters["pairing"]["function"](generation, **parameters["pairing"]["arguments"])

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
		    fitnessFunction,
		    dominanceFilter,
		    matchingProcedure,
		    memberEvolution,
		    mutation]


def evaluateFitness(population, fitness, target = None):

	portfolio = []

	for member in population:

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

			mutant = member[:]

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


def symbolMatching(dna,
				   strategy = "random",
				   group_size = 2,
				   chaos = False):

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


def pointCrossOver(cluster):

	generation = []

	for group in cluster:

		point = random.randint(0, len(group[0]) - 1)

		if (len(group) == 1):

			clone = forcedMutation(group[0])
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


def forcedMutation(chromosome):

	if (type(chromosome) not in (int, float)):

		if (random.random() >= 0.5):

			variant = shuffleMutation(chromosome)

		else:

			variant = randomMutation(chromosome)

	else:

		variant = randomMutation(chromosome)

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


def randomMutation(chromosome, mutation_number = 1, domain = None):

	if domain is None:

		domain = { "minimum": -1,
				   "maximum": 1 }

	if (mutation_number > len(chromosome)):

		mutation_number = len(chromosome)

	if ((type(chromosome) == str) or
		(type(chromosome[0]) == str)):

		defects = random.sample(range(0, len(chromosome)), mutation_number)

		if (type(chromosome) != list):

			buffer = list(chromosome)

		else:

			buffer = chromosome.copy()

		for index in defects:

			if (chromosome.isdigit() and
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


def linearAverage(cluster):

	generation = []

	for group in cluster:

		if (len(group) > 1):

			gamma = random.random()
			parent_a = group[0]
			parent_b = group[1]
			offspring_a = gamma*parent_a + (1 - gamma)*parent_b
			offspring_b = gamma*parent_b + (1 - gamma)*parent_a
			generation.extend((offspring_a, offspring_b))

		else:

			offspring = randomMutation(group[0])
			generation.append(offspring)

	return generation


def heuristicAverage(dna):

	generation = []

	while (len(generation) < len(dna)):

		if (len(dna) > 1):

			gamma = random.random()
			parent_a = random.choice(dna)
			dna.remove(parent_a)
			parent_b = random.choice(dna)
			dna.append(parent_a)
			offspring = gamma*(parent_a - parent_b) + parent_b
			generation.append(offspring)

		else:

			offspring = randomMutation(dna[0])
			generation.append(offspring)

	return generation


def tournamentSelection(generation, size = 2):

	if all((member["chromosome"] == generation[0]["chromosome"]) for member in generation[1:]):

		table = [forcedMutation(candidate["chromosome"]) for candidate in generation]

	else:

		table = []
		competition = filterDuplicates(generation)

		if (size > len(competition)):

			size = len(competition)

		while (len(table) < len(generation)):

			tournament = random.sample(competition, size)
			candidate = max(tournament, key = lambda chromosome: chromosome["fitness"])
			table.append(candidate["chromosome"])

	return table


def filterDuplicates(population):

	unique = []

	for member in population:

		if member not in unique:

			unique.append(member)

	return unique


def rouletteWheelSelection(generation):

	if (all((member["fitness"] == 0) for member in generation) or
		all((member["chromosome"] == generation[0]["chromosome"]) for member in generation[1:])):

		table = [forcedMutation(candidate["chromosome"]) for candidate in generation]

	else:

		roulette = filterDuplicates(generation)
		roulette = [member for member in roulette if (member["fitness"] > 0)]
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


def splitLine(population):

	line = []
	total = sum([member["fitness"] for member in population])
	initial = 0

	for member in population:

		final = initial + member["fitness"] / total
		line.append({ "chromosome": member["chromosome"],
					  "interval": (initial, final) })
		initial = final

	return line


def proportionalSelection(generation):

	if ((all(member["fitness"] == 0) for member in generation) or
		(all(member["chromosome"] == generation[0]["chromosome"]) for member in generation[1:])):

		table = [forcedMutation(candidate["chromosome"]) for candidate in generation]

	else:

		bag, table = [], []
		sections = filterDuplicates(generation)
		sections = [member for member in sections if (member["fitness"] != 0)]
		minimum = min(sections, key = lambda data: data["fitness"])

		for member in sections:

			factor = member["fitness"] // minimum["fitness"]
			bag.extend([member["chromosome"] for _ in range(factor)])

		while (len(table) < len(generation)):

			candidate = random.choice(bag)
			table.append(candidate)

	return table


def wordAssertion(chromosome, target):

	allowed = (str, list, tuple)

	assert ((type(chromosome) in allowed) and
			(type(target) in allowed)), \
			f"Both the input string and the target word must be of type 'str', 'list' or 'tuple', but got '{type(chromosome).__name__}' and '{type(target).__name__}'."
