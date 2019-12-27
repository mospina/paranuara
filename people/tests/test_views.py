import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from people.tests.factories import PersonFactory, FruitFactory, VegetableFactory


class PeopleViewTest(TestCase):
    def set_data(self):
        self.friends = []
        for _ in range(5):
            person = PersonFactory()
            self.friends.append(person)

        self.blue_eye_person = PersonFactory(eyeColor="blue")
        self.friends.append(self.blue_eye_person)

        self.person1 = PersonFactory(friends=self.friends)
        self.person2 = PersonFactory(friends=self.friends)
        self.person3 = PersonFactory(
            favouriteFruits=[FruitFactory(name="banana"), FruitFactory(name="apple")],
            favouriteVegetables=[
                VegetableFactory(name="beetroot"),
                VegetableFactory(name="lettuce"),
            ],
        )

    def setUp(self):
        self.client = APIClient()
        self.base_url = "/v1/people/"
        self.set_data()

    def test_people_get_one_returns_200(self):
        response = self.client.get(self.base_url + "{}".format(self.person3.index))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")
        self.assertEqual(json.loads(response.content)["fruits"], ["banana", "apple"])
        self.assertEqual(
            json.loads(response.content)["vegetables"], ["beetroot", "lettuce"]
        )

    def test_people_get_two_return_friends(self):
        response = self.client.get(
            self.base_url, {"index": [self.person1.index, self.person2.index]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")
        self.assertEqual(len(json.loads(response.content)["common_friends"]), 5)
        self.assertEqual(len(json.loads(response.content)["people"]), 2)
