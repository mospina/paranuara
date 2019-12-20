from io import StringIO
from unittest import skip
from django.test import TestCase
from django.core.management import call_command

from people.models import Person

class LoadDataTest(TestCase):

    def setUp(self):
        self.command = 'load_data'
        self.companies = 'resources/companies.json'
        self.people = 'resources/people.json'

    @skip('Test take too long to run')
    def test_load_data(self):
        out = StringIO()
        before_count = Person.objects.count()
        call_command(self.command, companies=[self.companies], people=[self.people], stdout=out)
        after_count = Person.objects.count()

        self.assertGreater(after_count, before_count)
