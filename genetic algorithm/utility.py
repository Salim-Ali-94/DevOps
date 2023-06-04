import random
from constants import CHARACTERS


def generatePopulation(chromosome_length = 2,
					   population_size = 5,
					   encoding = "number",
					   domain = None):

	if (domain is None):

		domain = { "minimum": -10,
	   			   "maximum": 10 }

	population = []
	# random.seed(42)

	# for _ in range(population_size):
	while (len(population) < population_size):

		if (encoding in ("character", "binary")):

			chromosome = ""

		else:

			chromosome = ()

		# for _ in range(chromosome_length):
		while (len(chromosome) < chromosome_length):

			if (encoding == "integer"):

				gene = random.randint(domain["minimum"], domain["maximum"])

			elif (encoding == "character"):

				random.shuffle(CHARACTERS)
				gene = random.choice(CHARACTERS)

			elif (encoding == "bit"):

				gene = random.randint(0, 1)

			elif (encoding == "binary"):

				gene = random.choice(("0", "1"))

			else:

				gene = random.uniform(domain["minimum"], domain["maximum"])

			if (encoding in ("character", "binary")):

				chromosome += gene

			else:

				chromosome = (*chromosome, gene)

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

		# for _ in population:
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

	# mixing_cluster = {}
	mixing_cluster = []
	group_number = len(dna) // group_size
	DNA = dna.copy()
	if not(chaos): random.shuffle(DNA)

	# for index in range(group_number):
	# for _ in range(group_number):
	while (len(mixing_cluster) < group_number):

		# mixing_cluster[str(index + 1)] = DNA[0:group_size]

		# random.shuffle(DNA)
		if chaos: random.shuffle(DNA)
		mixing_cluster.append(DNA[0:group_size])
		DNA = DNA[group_size:]

	if (len(DNA) > 0):

		# last = group_number + 1
		# mixing_cluster[str(last)] = DNA.copy()
		mixing_cluster.append(DNA.copy())

	return mixing_cluster


def sequentialMatching(dna, group_size = 2):

	# mixing_cluster = {}
	mixing_cluster = []
	group_number = len(dna) // group_size
	remainder = len(dna) % group_size
	DNA = dna.copy()

	# for index in range(group_number):
	# while (len(mixing_cluster) < group_number):
	while (len(DNA) >= group_size):

		# start = group_size*index
		# end = group_size*(index + 1)
		# mixing_cluster[str(index + 1)] = dna[start:end]
		mixing_cluster.append(DNA[0:group_size])
		DNA = DNA[group_size:]

	if (remainder > 0):

		# last = group_number + 1
		# mixing_cluster[str(last)] = dna[-remainder:]
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

	return swapMutation(member)


def swapMutation(chromosome):

	point_a = random.randint(0, len(chromosome) - 1)
	gene_a = chromosome[point_a]
	point_b = random.randint(0, len(chromosome) - 1)
	while (point_b == point_a): point_b = random.randint(0, len(chromosome) - 1)
	gene_b = chromosome[point_b]
	buffer = list(chromosome)
	buffer[point_a] = gene_b
	buffer[point_b] = gene_a
	chromosome = type(chromosome)(buffer)
	return chromosome


def wordAssertion(chromosome, target):

	allowed = (str, list, tuple)

	assert ((type(chromosome) in allowed) and
			(type(target) in allowed)), \
			f"Both the input string and the target word must be of type 'str', 'list' or 'tuple', but got '{type(chromosome).__name__}' and '{type(target).__name__}'."



# def wordAssertion(fitness):

# 	def testArguments(chromosome, target):

# 		allowed = (str, list, tuple)

# 		assert ((type(chromosome) in allowed) and
# 				(type(target) in allowed)), \
# 				f"Both the input string and the target word must be of type 'str', 'list' or 'tuple', but got '{type(chromosome).__name__}' and '{type(target).__name__}'."

# 		return fitness(chromosome, target)

# 	return testArguments


# @wordAssertion
# def wordScore(chromosome, target):

# 	score = 0

# 	for gene, character in zip(chromosome, target):

# 		if (gene == character):

# 			score += 1

# 	return score**2
