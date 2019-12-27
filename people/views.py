from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Person, People
from .serializers import PersonSerializer, PeopleSerializer


class PersonDetail(APIView):
    """
    Retrieve a single person
    """

    def get_object(self, index):
        try:
            return Person.objects.get(index=index)
        except Person.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, index, format=None):
        people = self.get_object(index)
        serializer = PersonSerializer(people)
        return Response(serializer.data)


class PeopleList(APIView):
    """
    Retrieve two or more people
    """

    def get(self, request, format=None):
        indexes = request.query_params.getlist("index")
        if len(indexes) == 1:
            return redirect(PersonDetail.as_view(indexes[0]))
        if indexes:
            people = Person.objects.filter(index__in=indexes)
        else:
            people = Person.objects.all()
        friends = [
            f
            for f in self.get_common_friends(people)
            if f.eyeColor == "brown" and not f.has_died
        ]
        data = People(friends=friends, people=people)
        serializer = PeopleSerializer(data)
        return Response(serializer.data)

    @classmethod
    def get_common_friends(cls, people):
        """
        Given two list of friends, return a list of common friends. That's it
        friends that are in both lists

        [person] -> [person] -> [person]

        Cross product
        -------------

        """
        friends = people[0].friends.all()

        for person in people:
            common_friends = filter(lambda x: x in person.friends.all(), friends)
            friends = list(common_friends)

        return friends
