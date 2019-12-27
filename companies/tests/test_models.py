from django.test import TestCase
from companies.models import Company


class TestCompanyFileLoader(TestCase):
    def test_load_data_from_file(self):
        before_count = Company.objects.count()
        Company.load_data_from_file("../../resources/companies.json")
        after_count = Company.objects.count()

        self.assertGreater(after_count, before_count)

    def test_index_must_be_unique(self):
        Company.load_data_from_file("../../resources/companies.json")
        before_count = Company.objects.count()
        Company.load_data_from_file("../../resources/companies.json")
        after_count = Company.objects.count()

        self.assertEqual(after_count, before_count)
