import unittest
import utility


class TestUtility(unittest.TestCase):

	def test_generatePopulation(self):

		population = utility.generatePopulation(0)
		self.assertEqual(population, [(), (), (), (), ()])

	def test_wordScore(self):

		score = utility.wordScore("", "not empty")
		self.assertEqual(score, 0)
		score = utility.wordScore("word six", "word seven")
		self.assertEqual(score, 0)

		with self.assertRaisesRegex(AssertionError, "Both the input string and the target word must be of type 'str', 'list' or 'tuple', but got 'list' and 'int'."):

			utility.wordScore([], 0)

	def test_randomSelection(self):

		population = utility.generatePopulation(2)
		dna_pool = utility.randomSelection(population)
		self.assertEqual(len(dna_pool), len(population))
		self.assertEqual(type(dna_pool), type(population))
		self.assertEqual(len(dna_pool[0]), 2)

	def test_sequentialMatching(self):

		population = utility.generatePopulation(2)
		dna_pool = utility.randomSelection(population)
		cluster = utility.sequentialMatching(dna_pool)
		self.assertEqual(cluster[0][0], dna_pool[0])
		self.assertEqual(cluster[-1][-1], dna_pool[-1])

	def test_randomMatching(self):

		population = utility.generatePopulation(2)
		dna_pool = utility.randomSelection(population)
		cluster = utility.randomMatching(dna_pool)
		self.assertEqual(len(cluster[0][0]), len(dna_pool[0]))
		self.assertEqual(type(cluster[0][0]), type(dna_pool[0]))
		self.assertEqual(len(cluster[-1][-1]), len(dna_pool[-1]))
		self.assertEqual(type(cluster[-1][-1]), type(dna_pool[-1]))

	def test_pointCrossOver(self):

		population = utility.generatePopulation(2)
		dna_pool = utility.randomSelection(population)
		cluster = utility.randomMatching(dna_pool)
		mutants = utility.pointCrossOver(cluster)
		self.assertEqual(len(mutants), len(population))
		self.assertEqual(type(mutants), type(population))

	def test_swapAllele(self):

		population = utility.generatePopulation(5)
		dna_pool = utility.randomSelection(population)
		cluster = utility.randomMatching(dna_pool)
		mutant = utility.swapAllele(cluster[0], 2)
		self.assertEqual(len(mutant[0]), len(population[0]))
		self.assertEqual(type(mutant[0]), type(population[0]))
		self.assertEqual(mutant[3:], cluster[3:])

	def test_rotateMutation(self):

		population = utility.generatePopulation(5)
		mutant = utility.rotateMutation(population[0])
		self.assertEqual(len(mutant), len(population[0]))
		self.assertEqual(type(mutant), type(population[0]))

	def test_randomMutation(self):

		population = utility.generatePopulation(5, category = "character", genotype = "base")
		mutant = utility.randomMutation(population[0])
		self.assertEqual(type(mutant), type(population[0]))
		self.assertEqual(len(mutant), len(population[0]))




if __name__ == "__main__":

	unittest.main()
