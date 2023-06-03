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
		self.assertEqual(score, 36)
		with self.assertRaises(Exception) as context: utility.wordScore([], 0)
		self.assertTrue("Both the input string and the target word must be of type 'str', 'list' or 'tuple', but got 'list' and 'int'." in context.exception)



if __name__ == "__main__":

	unittest.main()
