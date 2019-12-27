import json

from django.db import models


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{} - {}".format(self.index, self.name)

    @classmethod
    def load_data_from_file(cls, file_path):
        """
        Save the data from a json file in the RDB
        """
        with open(file_path, newline="") as fh:
            json_data = json.load(fh)
        fh.close()

        for entry in json_data:
            cls.objects.get_or_create(index=entry["index"], name=entry["company"])
