from django.core.management.base import BaseCommand, CommandError
from people.loader import load_data_from_file


class Command(BaseCommand):
    help = "Read data from a json file and store it in the database"

    def add_arguments(self, parser):
        parser.add_argument("filenames", nargs="+", type=str)

    def handle(self, *args, **options):
        for filename in options["filenames"]:
            load_data_from_file(filename)
