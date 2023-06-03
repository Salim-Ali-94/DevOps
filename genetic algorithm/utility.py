import random
from constants import CHARACTERS


def initializePopulation(chromosome_length, encoding = "number", domain = { "minimum": -100, "maximum": 100 }, population_size = 100):

	population = generatePopulation(population_size, chromosome_length, encoding, domain)
	return population


def generatePopulation(population_size, chromosome_length, encoding, domain):

	population = []

	for i in range(population_size):

		if ((encoding == "character") or 
			(encoding == "binary")):

			chromosome = ""

		else:

			chromosome = ()

		for j in range(chromosome_length):

			if (encoding == "integer"):

				gene = random.randint(domain["minimum"], domain["maximum"])

			elif (encoding == "character"):

				random.shuffle(CHARACTERS)
				gene = random.choice(CHARACTERS)

			elif (encoding == "bit"):

				gene = random.randint(0, 1)

			elif (encoding == "binary"):

				gene = random.choice(["0", "1"])

			else:

				gene = random.uniform(domain["minimum"], domain["maximum"])

			if ((encoding == "character") or 
				(encoding == "binary")):

				chromosome += gene

			else:

				chromosome = (*chromosome, gene)

		population.append(chromosome)

	return population
