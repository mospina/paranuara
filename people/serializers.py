from rest_framework import serializers

from companies.serializers import CompanySerializer
from people.models import Tag, Fruit, Vegetable, Person


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "label")


class FruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruit
        fields = ("id", "name")


class VegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetable
        fields = ("id", "name")


class PersonSerializer(serializers.ModelSerializer):

    tags = TagSerializer(read_only=True, many=True)
    # friends = PersonSerializer(read_only=True, many=True)
    company = CompanySerializer(read_only=True, many=False)
    fruits = serializers.SerializerMethodField("favouriteFruits")
    vegetables = serializers.SerializerMethodField("favouriteVegetables")

    class Meta:
        model = Person
        fields = (
            "created_at",
            "modified_at",
            "_id",
            "index",
            "guid",
            "has_died",
            "balance",
            "picture",
            "age",
            "eyeColor",
            "name",
            "gender",
            "company",
            "email",
            "phone",
            "address",
            "about",
            "registered",
            "tags",
            "friends",
            "greeting",
            "fruits",
            "vegetables",
        )

    def favouriteFruits(self, obj):
        return [o.name for o in obj.favouriteFruits.all()]

    def favouriteVegetables(self, obj):
        return [o.name for o in obj.favouriteVegetables.all()]


class PeopleSerializer(serializers.Serializer):

    common_friends = serializers.SerializerMethodField("get_friends")
    people = serializers.SerializerMethodField("get_people")

    def get_friends(self, obj):
        return [{"name": o.name, "index": o.index} for o in obj.friends]

    def get_people(self, obj):
        return [
            {"name": o.name, "age": o.age, "address": o.address, "phone": o.phone}
            for o in obj.people
        ]
