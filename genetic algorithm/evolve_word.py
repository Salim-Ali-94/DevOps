import utility


if __name__ == "__main__":

	target = "cat"
	population_size = 10*len(target)
	fitness_function = utility.wordScore
	category = "character"
	genotype = "base"
	mutation_rate = 1 / 100
	loop = True
	generations = 5
	display = False

	natural_selection = { "function": utility.tournamentSelection,
						  "arguments": { "size": len(target) } }

	pairing = { "function": utility.symbolMatching,
				"arguments": { "group_size": 2,
				 			   "strategy": "random",
				 			   "chaos": False } }

	combination = { "function": utility.pointCrossOver,
					"arguments": None }

	mutation = { "function": utility.randomMutation,
				 "arguments": { "mutation_number": 1 } }

	parameters = { "population_size": population_size,
				   "function": fitness_function,
				   "category": category,
				   "genotype": genotype,
				   "mutation_rate": mutation_rate,
				   "funnel": natural_selection,
				   "pairing": pairing,
				   "combination": combination,
				   "mutator": mutation,
				   "loop": loop,
				   "generations": generations,
				   "display": display }

	alpha, iterations, initial = utility.evolve(target, parameters)
	if (alpha["chromosome"] == target): print(f"\nEvolved '{ initial['chromosome'] }' to '{ alpha['chromosome'] }' in { iterations } generation(s) with a fitness score of { alpha['fitness'] }\n")
	else: print("ALGORITHM FAILED TO CONVERGE TO A SOLUTION")
