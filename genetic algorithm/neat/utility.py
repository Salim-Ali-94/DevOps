import random
from models.network import Network
from models.node import Node
from models.branch import Branch


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

		if not any(chromosome_a in dna["chromosomes"] for dna in species):

			chromosome_a.species = group + 1
			species.append({ "group": group + 1,
							 "chromosomes": [chromosome_a],
							 "group_size": 1,
							 "group_fitness": chromosome_a.fitness,
							 "distributed_fitness": 0 })

			for chromosome_b in population[group + 1:]:

				if not any(chromosome_b in dna["chromosomes"] for dna in species):

					pairs = alignGenes(chromosome_a.genome, chromosome_b.genome)
					disjoint_a = countUnpaired(chromosome_a.genome, chromosome_b.genome)
					disjoint_b = countUnpaired(chromosome_b.genome, chromosome_a.genome)
					excess_a = countOffset(chromosome_a.genome, chromosome_b.genome)
					excess_b = countOffset(chromosome_b.genome, chromosome_a.genome)
					weight = sum(abs(pair[0].weight - pair[1].weight) for pair in pairs) / (len(pairs) if (len(pairs) > 0) else 1)
					disjoint = disjoint_a + disjoint_b
					excess = excess_a + excess_b
					factor = max(sum(1 for gene in chromosome_a.genome if gene.active), sum(1 for gene in chromosome_b.genome if gene.active), 1)
					compatibility = disjoint*c1 / factor + excess*c2 / factor + weight*c3

					if (compatibility < threshold):

						species[group]["chromosomes"].append(chromosome_b)
						species[group]["group_size"] += 1
						species[group]["group_fitness"] = sum(chromosome.fitness for chromosome in species[group]["chromosomes"]) / species[group]["group_size"]
						chromosome_b.species = group + 1

					if (group == len(population) - 2):

						if not any(chromosome_b in dna["chromosomes"] for dna in species):

							chromosome_b.species = group + 2
							species.append({ "group": len(species) + 1,
											 "chromosomes": [chromosome_b],
											 "group_size": 1,
											 "group_fitness": chromosome_b.fitness,
											 "distributed_fitness": 0 })

	modifyFitness(species)
	return species


def crossover(species, topology):

	generation = []

	for group in species:

		population = []

		while (len(population) < group["group_limit"]):

			offspring = []
			network_a = rouletteWheel(group)
			group["chromosomes"].remove(network_a)
			network_b = rouletteWheel(group)
			group["chromosomes"].append(network_a)
			pairs = alignGenes(network_a.genome, network_b.genome, True)
			detached_a = segmentGenes(network_a.genome, network_b.genome)
			detached_b = segmentGenes(network_b.genome, network_a.genome)
			offset_a = segmentGenes(network_a.genome, network_b.genome, "exterior")
			offset_b = segmentGenes(network_b.genome, network_a.genome, "exterior")
			detached = detached_a + detached_b
			offset = offset_a + offset_b
			offspring.extend(detached)

			for pair in pairs:

				gene = random.choice(pair)
				offspring.append(gene)

			for synapse in offset:

				if (((network_a.fitness > network_b.fitness) and
					  synapse in network_a.genome) or
					((network_b.fitness > network_a.fitness) and
					  synapse in network_b.genome)):

					offspring.append(synapse)

				elif (network_a.fitness == network_b.fitness):

					if (random.random() < 0.5):

						offspring.append(synapse)

			population.append(decodeGenome(offspring, topology))

		generation.extend(population)

	return generation


def decodeGenome(genome, architecture):

	network = Network(architecture, generate = False)

	for gene in genome:

		if not any(dna.node == gene.input_node for dna in network.neurons):

			input_neuron = Node(node = gene.input_node,
							    layer = gene.input_layer,
							    branches = [],
							    function = gene.input_neuron.function,
							    activity = 1 if (gene.input_neuron.node_type == "bias") else 0,
							    output = 1 if (gene.input_neuron.node_type == "bias") else 0,
							    node_type = gene.input_neuron.node_type)

			network.neurons.append(input_neuron)

		else:

			input_neuron = next((dna for dna in network.neurons if (dna.node == gene.input_node)), None)

			if (gene.input_layer < input_neuron.layer):

				input_neuron.layer = gene.input_layer
				input_neuron.function = random.choice((gene.input_neuron.function, input_neuron.function))

		if not any(dna.node == gene.output_node for dna in network.neurons):

			output_neuron = Node(node = gene.output_node,
							     layer = gene.output_layer,
							     branches = [],
							     function = gene.output_neuron.function,
							     activity = 1 if (gene.output_neuron.node_type == "bias") else 0,
							     output = 1 if (gene.output_neuron.node_type == "bias") else 0,
							     node_type = gene.output_neuron.node_type)

			network.neurons.append(output_neuron)

		else:

			output_neuron = next((dna for dna in network.neurons if (dna.node == gene.output_node)), None)

			if (gene.output_layer < output_neuron.layer):

				output_neuron.layer = gene.output_layer
				output_neuron.function = random.choice((gene.output_neuron.function, output_neuron.function))

		synapse = Branch(weight = gene.weight,
						 input_node = gene.input_node,
						 output_node = gene.output_node,
						 input_neuron = input_neuron,
						 output_neuron = output_neuron,
						 input_layer = input_neuron.layer,
						 output_layer = output_neuron.layer,
						 active = gene.active,
						 branch_type = gene.branch_type,
						 recurrent = gene.recurrent,
						 skip = gene.skip,
						 innovation = gene.innovation)

		output_neuron.branches.append(synapse)
		network.genome.append(synapse)

	network.layers = max(dna.layer for dna in network.neurons) + 1
	network.network = [tuple()]*network.layers

	for node in network.neurons:

		network.network[node.layer] += (node, )
		network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: dna.node)

	return network


def modifyFitness(species):

	global_fitness = 0
	size = 0

	for group in species:

		for chromosome in group["chromosomes"]:

			chromosome.modified_fitness = chromosome.fitness / group["group_size"]
			group["distributed_fitness"] += chromosome.modified_fitness
			global_fitness += chromosome.modified_fitness

		group["distributed_fitness"] /= group["group_size"]
		size += group["group_size"]

	global_fitness /= size

	for group in species:

		limit = round(group["group_size"]*group["distributed_fitness"] / global_fitness)
		group["group_limit"] = max(limit, 1)


def alignGenes(genome_a, genome_b, off = False):

	group = []

	for a in genome_a:

		for b in genome_b:

			if ((a.innovation == b.innovation) and
				(off or (a.active and b.active))):

				group.append((a, b))

	return group


def segmentGenes(genome_a, genome_b, region = "interior"):

	unpaired = []
	maximum_b = genome_b[-1].innovation

	for a in genome_a:

		if all(((b.innovation != a.innovation) and
				((a.innovation < maximum_b) if (region == "interior") else
				 (a.innovation > maximum_b))) for b in genome_b):

			unpaired.append(a)

	return unpaired


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


def rouletteWheel(group):

	absolute_fitness = group["distributed_fitness"]*group["group_size"]
	random.shuffle(group["chromosomes"])
	theta = random.uniform(0, 1)
	probability = 0

	for chromosome in group["chromosomes"]:

		probability += chromosome.modified_fitness / absolute_fitness

		if (probability >= theta):

			return chromosome

	maximum = max(dna.fitness for dna in group["chromosomes"])
	candidate = next((gene for gene in group["chromosomes"] if (gene.fitness == maximum)), random.choice(group["chromosomes"]))
	return candidate
