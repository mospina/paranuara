from django.db import models

from companies.models import Company

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'No response')
)

KNOWN_FRUITS = ['orange', 'banana', 'strawberry', 'apple']

KNOWN_VEGETABLES = ['cucumber', 'carrot', 'celery', 'beetroot']

class Tag(models.Model):
    label = models.CharField(max_length=64)

    def __str__(self):
        return self.label

class Fruit(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Vegetable(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    _id = models.CharField(max_length=128, unique=True)
    index = models.IntegerField(unique=True)
    guid = models.CharField(max_length=128, unique=True) # UUI
    has_died = models.BooleanField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.URLField()
    age = models.IntegerField()
    eyeColor = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    about = models.TextField()
    registered = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    friends = models.ManyToManyField("self")
    greeting = models.CharField(max_length=256)
    favouriteFruits = models.ManyToManyField(Fruit)
    favouriteVegetables = models.ManyToManyField(Vegetable)

    def __str__(self):
        return self.name
