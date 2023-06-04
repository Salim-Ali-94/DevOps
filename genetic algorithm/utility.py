import random
from constants import CHARACTERS


def generatePopulation(chromosome_length = 2,
					   population_size = 5,
					   encoding = None,
					   category = "number",
					   genotype = "base",
					   gene_width = 1,
					   domain = None):

	if (domain is None):

		domain = { "minimum": -10,
	   			   "maximum": 10 }

	population = []
	random.shuffle(CHARACTERS)
	symbol = ("character", "binary")
	number = ("number", "integer")
	# random.seed(42)

	while (len(population) < population_size):

		# if (encoding == "digital"):

		# 	chromosome = binaryConverter()

		# elif (encoding == "one-hot"):

		# 	chromosome = oneHotEncoding()

		# elif (encoding == "hex"):

		# 	chromosome = hexConverter()

		# elif (genotype == "encoded"):
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
	score = 0

	for gene, character in zip(chromosome, target):

		if (gene == character):

			score += 1

	return score**2


def randomSelection(population,
					duplication_indicator = True,
					clone_flag = False,
					group_size = 2):

	random.shuffle(population)
	candidate_pool = population.copy()
	suspend = 0
	table = []

	if not(duplication_indicator):

		table = candidate_pool.copy()

	else:

		while (len(table) < len(population)):

			candidate_member = random.choice(candidate_pool)
			table.append(candidate_member)

			if not(clone_flag):

				if (suspend < group_size):

					candidate_pool.remove(candidate_member)
					suspend += 1

				else:

					suspend = 0

					for parent in table[-group_size:]:

						candidate_pool.append(parent)

	return table


def randomMatching(dna,
				   group_size = 2,
				   chaos = False):

	mixing_cluster = []
	group_number = len(dna) // group_size
	DNA = dna.copy()
	if not(chaos): random.shuffle(DNA)

	while (len(mixing_cluster) < group_number):

		if chaos: random.shuffle(DNA)
		mixing_cluster.append(DNA[0:group_size])
		DNA = DNA[group_size:]

	if (len(DNA) > 0):

		mixing_cluster.append(DNA.copy())

	return mixing_cluster


def sequentialMatching(dna, group_size = 2):

	mixing_cluster = []
	remainder = len(dna) % group_size
	DNA = dna.copy()

	while (len(DNA) >= group_size):

		mixing_cluster.append(DNA[0:group_size])
		DNA = DNA[group_size:]

	if (remainder > 0):

		mixing_cluster.append(dna[-remainder:])

	return mixing_cluster


def pointCrossOver(cluster):

	population = []

	for group in cluster:

		point = random.randint(0, len(group[0]) - 1)

		if (len(group) == 1):

			clone = forcedMutation(group[0])
			population.append(clone)

		else:

			clones = swapAllele(group, point)
			population.extend(clones)

	return population


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


def forcedMutation(member):

	return rotateMutation(member)


def rotateMutation(chromosome):

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

	if (type(chromosome) == str):

		chromosome = "".join(buffer)

	else:

		chromosome = type(chromosome)(buffer)

	return chromosome


# def randomMutation(chromosome, mutation_number = 1):

# 	if (mutation_number > len(chromosome)):

# 		mutation_number = len(chromosome)

# 	defects = random.sample(range(0, len(chromosome)), mutation_number)
	
# 	if (type(chromosome) == str):

# 		buffer = list(chromosome)

# 		for index in defects:

# 			value = random.choice(CHARACTERS)

# 			while (value == buffer[index]):

# 				value = random.choice(CHARACTERS)

# 			buffer[index] = value

# 		chromosome = "".join(buffer)

# 	else:

# 		encoding = identifyEncoding(chromosome)

# 		for index in defects:

# 			value = random.uniform(min(chromosome), max(chromosome))
# 			value = random.randint(0, 1)
# 			value = random.randint(0, 1)


# def identifyEncoding(chromosome):

# 	if (type(chromosome[0]) == float):

# 		encoding = "number"

# 	elif (type(chromosome[0]) == int):

# 		if all(value in (0, 1) for value in chromosome):

# 			encoding = "bit"

# 		else:

# 			encoding = "integer"

# 	elif (type(chromosome) == str):

# 		if all(value in ("0", "1") for value in chromosome):

# 			encoding = "binary"

# 		else:

# 			encoding = "character"

# 	else:

# 		encoding = "character"

# 	return encoding


def wordAssertion(chromosome, target):

	allowed = (str, list, tuple)

	assert ((type(chromosome) in allowed) and
			(type(target) in allowed)), \
			f"Both the input string and the target word must be of type 'str', 'list' or 'tuple', but got '{type(chromosome).__name__}' and '{type(target).__name__}'."
