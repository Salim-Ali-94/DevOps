from models.network import Network


def initializeGeneration(population_size, architecture, parameters):

	population = []

	while (len(population) < population_size):

		gene = Network(architecture,
					   bias_rate = parameters["bias_rate"],
					   connection_rate = parameters["connection_rate"],
					   active_rate = parameters["active_rate"],
					   skip_rate = parameters["skip_rate"],
					   recurrent_rate = parameters["recurrent_rate"],
					   recurrent = parameters["recurrent"],
					   skip = parameters["skip"])

		while (all(not(dna.active) for dna in gene.genome) or
			  (len(gene.genome) == 0)):

			gene = Network(architecture,
						   bias_rate = parameters["bias_rate"],
						   connection_rate = parameters["connection_rate"],
						   active_rate = parameters["active_rate"],
						   skip_rate = parameters["skip_rate"],
						   recurrent_rate = parameters["recurrent_rate"],
						   recurrent = parameters["recurrent"],
						   skip = parameters["skip"])

		population.append(gene)

	return population


def evaluateFitness(population, sensor, action, function):

	for chromosome in population:

		decision = chromosome.propagate(sensor)
		chromosome.fitness = action(decision, function, sensor)


def speciation(population, threshold = 0.3, c1 = 1, c2 = 1, c3 = 0.4):

	species = []

	for (group, chromosome_a) in enumerate(population[:-1]):

		if not any(chromosome_a in dna["members"] for dna in species):

			chromosome_a.species = group + 1
			species.append({ "group": group + 1,
							 "members": [chromosome_a],
							 "group_size": 1,
							 "group_fitness": chromosome_a.fitness,
							 "distributed_fitness": 0 })

			for chromosome_b in population[group + 1:]:

				if not any(chromosome_b in dna["members"] for dna in species):

					pairs = alignGenes(chromosome_a.genome, chromosome_b.genome)
					disjoint_a = countUnpaired(chromosome_a.genome, chromosome_b.genome)
					disjoint_b = countUnpaired(chromosome_b.genome, chromosome_a.genome)
					excess_a = countOffset(chromosome_a.genome, chromosome_b.genome)
					excess_b = countOffset(chromosome_b.genome, chromosome_a.genome)
					weight = sum(abs(pair[0].weight - pair[1].weight) for pair in pairs) / (len(pairs) if (len(pairs) > 0) else 1)
					disjoint = disjoint_a + disjoint_b
					excess = excess_a + excess_b
					factor = max(sum(1 for gene in chromosome_a.genome if gene.active), sum(1 for gene in chromosome_b.genome if gene.active))
					compatibility = disjoint*c1 / factor + excess*c2 / factor + weight*c3

					if (compatibility < threshold):

						species[group]["members"].append(chromosome_b)
						species[group]["group_size"] += 1
						species[group]["group_fitness"] = sum(chromosome.fitness for chromosome in species[group]["members"]) / species[group]["group_size"]
						chromosome_b.species = group + 1

					if (group == len(population) - 2):

						if not any(chromosome_b in dna["members"] for dna in species):

							chromosome_b.species = group + 2
							species.append({ "group": len(species) + 1,
											 "members": [chromosome_b],
											 "group_size": 1,
											 "group_fitness": chromosome_b.fitness,
											 "distributed_fitness": 0 })

	modifyFitness(species)
	return species


def modifyFitness(species):

	global_fitness = 0
	size = 0

	for group in species:

		for chromosome in group["members"]:

			chromosome.modified_fitness = chromosome.fitness / group["group_size"]
			group["distributed_fitness"] += chromosome.modified_fitness
			global_fitness += chromosome.modified_fitness

		group["distributed_fitness"] /= group["group_size"]
		size += group["group_size"]

	global_fitness /= size

	for group in species:

		limit = round(group["group_size"]*group["distributed_fitness"] / global_fitness)
		group["group_limit"] = max(limit, 1)


def alignGenes(genome_a, genome_b):

	group = []

	for a in genome_a:

		for b in genome_b:

			if ((a.innovation == b.innovation) and
				(a.active and b.active)):

				group.append((a, b))

	return group


def countUnpaired(genome_a, genome_b):

	count = 0
	maximum_b = genome_b[-1].innovation

	for a in genome_a:

		if (a.active and
		   ((a.innovation < maximum_b) and
		   	not any(b.innovation == a.innovation for b in genome_b) or
		   	any((a.innovation == b.innovation) and
				(not b.active and a.active) for b in genome_b))):

			count += 1

	return count


def countOffset(genome_a, genome_b):

	count = 0
	maximum_b = genome_b[-1].innovation

	for a in genome_a:

		if (a.active and
		   ((a.innovation > maximum_b) and
			not any(b.innovation == a.innovation for b in genome_b) or
			any((not b.active and (a.innovation == b.innovation)) for b in genome_b))):

			count += 1

	return count

def rouletteWheelSelection(group):

	absolute_fitness = group["distributed_fitness"]*group["group_size"]
	cumulative_fitness = 0
	theta = random.random()

	for chromosome in group["members"]:

		cumulative_fitness += chromosome.modified_fitness

		if (cumulative_fitness >= theta):

			return chromosome

	maximum = max(dna.fitness for dna in gene["members"])
	candidate = next((gene for gene in group["members"] if (gene.fitness == maximum)), None)
	return candidate
