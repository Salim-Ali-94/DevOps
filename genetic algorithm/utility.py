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
	random.seed(42)

	for _ in range(population_size):

		if (encoding in ("character", "binary")):

			chromosome = ""

		else:

			chromosome = ()

		for _ in range(chromosome_length):

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

	allowed = ("str", "list", "tuple")
	assert ((type(chromosome).__name__ in allowed) and (type(target).__name__ in allowed)), f"Both the input string and the target word must be of type 'str' or of type 'list', but got {type(chromosome).__name__} and {type(target).__name__}."
	score = 0

	for gene, character in zip(chromosome, target):

		if (gene == character):

			score += 1

	return score**2
