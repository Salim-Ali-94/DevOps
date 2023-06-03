import random


def initializePopulation(chromosome_length, encoding = "number", domain = { "min": -100, "max": 100 }, population_size = 100):

	population = generatePopulation(population_size, chromosome_length, encoding, domain)
	return population


def generatePopulation(population_size, chromosome_length, encoding, domain):

	population = []

	for i in range(population_size):

		chromosome = ()

		for j in range(chromosome_length):

			if (encoding == "number"): gene = random.uniform(domain["min"], domain["max"])
			chromosome = (*chromosome, gene)

		population.append(chromosome)

	return population
