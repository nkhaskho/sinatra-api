from ..utils import sparql_query
import unittest

class SparQLQueryTest(unittest.TestCase):

    def testSparQL(self):
        new_column = "birth"
        results_bindings = sparql_query(new_column)["results"]["bindings"]
        self.assertEqual(len(results_bindings), 2)

    if __name__ == '__main__':
        unittest.main()