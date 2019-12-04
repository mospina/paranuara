import unittest
from companies import fileloader
from companies.models import Company

class TestFileLoader(unittest.TestCase):

    def test_load_data_from_file(self):
        before_count = Company.objects.count()
        result = fileloader.load_data_from_file('../../resources/companies.json')
        after_count = Company.objects.count()

        self.assertGreater(after_count, before_count)
