from django.core.management.base import BaseCommand, CommandError

from companies.models import Company
from people.loader import load_data_from_file

class Command(BaseCommand):
    help = "Read data from a json file and store it in the database"

    def add_arguments(self, parser):
        parser.add_argument('--companies', nargs='+', dest='companies', type=str)
        parser.add_argument('--people', nargs='+', dest='people', type=str)

    def handle(self, *args, **options): 
        # First load companies
        for elem in options['companies']:
            Company.load_data_from_file(elem)
        # Then load people
        for elem in options['people']:
            load_data_from_file(elem)
