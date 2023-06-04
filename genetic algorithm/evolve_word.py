import utility


if __name__ == "__main__":

	target = "Let none ignorant of calculus enter here."
	population_size = 100
	fitness_function = utility.wordScore
	category = "character"
	genotype = "base"
	episodes = 1000
	mutation_rate = 0.5 / 100
	natural_selection = utility.randomSelection
	pairing = utility.sequentialMatching
	combination = utility.pointCrossOver
	mutation = utility.randomMutation
	group_size = 2
	member = utility.evolve(target,
				   			population_size,
						    fitness_function,
						    category,
						    genotype,
						    episodes,
						    mutation_rate,
						    natural_selection,
						    pairing,
						    combination,
						    mutation,
						    group_size)
