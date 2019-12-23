from factory.django import DjangoModelFactory
import factory

from companies.tests.factories import CompanyFactory
from people.models import Tag, Fruit, Vegetable, Person

class TagFactory(DjangoModelFactory):

    class Meta:
        model = Tag

    label = 'tag' 

class FruitFactory(DjangoModelFactory):

    class Meta:
        model = Fruit

    name = 'apple' 

class VegetableFactory(DjangoModelFactory):

    class Meta:
        model = Vegetable

    name = 'carrot' 

class PersonFactory(DjangoModelFactory):

    class Meta:
        model = Person

    _id = factory.Sequence(lambda n: 'id%d' % n)
    index = factory.Sequence(lambda n: n)
    guid = factory.Sequence(lambda n: 'guid%d' % n)
    has_died = 'False'
    balance = 1000.00
    picture = 'http://www.example.com/photo.jpg'
    age = 50
    eyeColor = 'brown'
    name = factory.Faker('name')
    gender = 'M'
    company = factory.SubFactory(CompanyFactory)
    email = 'namesur@example.com'
    phone = '900088812345'
    address = '10 Street Avenue'
    about = 'About me'
    registered = '2010-10-10 10:10:10'
    greeting = 'hello'

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def friends(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for friend in extracted:
                self.friends.add(friend)

    @factory.post_generation
    def favouriteFruits(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for food in extracted:
                self.favouriteFruits.add(food)

    @factory.post_generation
    def favouriteVegetables(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for food in extracted:
                self.favouriteVegetables.add(food)
