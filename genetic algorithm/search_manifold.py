import math
import utility


if __name__ == "__main__":

	function = lambda X: math.exp(-(X[0]**2 + X[1]**2))
	population_size = 10
	chromosome_length = 2
	generations = 5
	category = "number"
	genotype = "encoded"
	mutation_rate = 0.5 / 100
	loop = True
	display = False
	objective = "maximize"
	task = "search"

	domain = { "minimum": -1e3,
    		   "maximum": 1e3 }

	natural_selection = { "function": utility.tournamentSelection,
						  "arguments": { "size": population_size // 2,
						  				 "objective": objective,
						  				 "chromosome_length": chromosome_length } }

	pairing = { "function": utility.symbolMatching,
				"arguments": { "group_size": 2,
				 			   "strategy": "random",
				 			   "chaos": True } }

	combination = { "function": utility.linearAverage,
					"arguments": { "chromosome_length": chromosome_length } }

	mutation = { "function": utility.randomMutation,
				 "arguments": { "mutation_number": 1,
				 				"chromosome_length": 1 } }

	parameters = { "population_size": population_size,
				   "function": function,
				   "category": category,
				   "genotype": genotype,
				   "chromosome_length": chromosome_length,
				   "mutation_rate": mutation_rate,
				   "funnel": natural_selection,
				   "pairing": pairing,
				   "combination": combination,
				   "mutator": mutation,
				   "task": task,
				   "objective": objective,
				   "loop": loop,
				   "domain": domain,
				   "generations": generations,
				   "display": display }

	alpha, iterations, initial = utility.evolve(parameters)
	if (not(loop) and (iterations < generations)): print(f"\nSUMMARY OF RESULTS:\nsolution: {alpha['chromosome']}\nnumber of iterations: {iterations}\noptimum fitness: {alpha['fitness']}\n")
	elif (iterations < generations): print(f"\nSUMMARY OF RESULTS:\nsolution: {alpha['chromosome']}\nnumber of iterations: {iterations}\noptimum fitness: {alpha['fitness']}\n")
	else: print(f"ALGORITHM TERMINATED EARLY WITH THE FOLLOWING SOLUTION:\nsolution: {alpha['chromosome']}\noptimum fitness: {alpha['fitness']}\n")
