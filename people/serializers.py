from rest_framework import serializers

from companies.serializers import CompanySerializer
from people.models import Tag, Fruit, Vegetable, Person

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')

class FruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruit
        fields = ('id', 'name')
        
class VegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetable
        fields = ('id', 'name')

class PersonSerializer(serializers.ModelSerializer):

    tag = TagSerializer(read_only=True, many=True)
    favouriteFruits = FruitSerializer(read_only=True, many=True)
    favouriteVegetables = VegetableSerializer(read_only=True, many=True)
    # friends = PersonSerializer(read_only=True, many=True)
    company = CompanySerializer(read_only=True, many=False)

    class Meta:
        model = Person
        fields = (
            'created_at',
            'modified_at',
            '_id',
            'index',
            'guid',
            'has_died',
            'balance',
            'picture',
            'age',
            'eyeColor',
            'name',
            'gender',
            'company',
            'email',
            'phone',
            'address',
            'about',
            'registered',
            'tags',
            'friends',
            'greeting',
            'favouriteFruits',
            'favouriteVegetables'
        )


