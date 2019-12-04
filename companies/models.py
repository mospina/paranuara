from django.db import models

class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    index = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.first_name, self.last_name)
