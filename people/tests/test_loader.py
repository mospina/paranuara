from unittest import skip
import json
from decimal import Decimal

from django.test import TestCase

from companies.models import Company
from people import loader
from people.models import Person
from people.models import Fruit, Vegetable, Tag

PEOPLE = """
[
  {
    "_id": "595eeb9b96d80a5bc7afb106",
    "index": 0,
    "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
    "has_died": true,
    "balance": "$2,418.59",
    "picture": "http://placehold.it/32x32",
    "age": 61,
    "eyeColor": "blue",
    "name": "Carmella Lambert",
    "gender": "female",
    "company_id": 1,
    "email": "carmellalambert@earthmark.com",
    "phone": "+1 (910) 567-3630",
    "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
    "about": "Non duis dolore ad enim. Est id reprehenderit cupidatat tempor excepteur.",
    "registered": "2016-07-13T12:29:07 -10:00",
    "tags": [
      "id",
      "quis",
      "ullamco",
      "consequat",
      "laborum",
      "sint",
      "velit"
    ],
    "friends": [
      {
        "index": 0
      },
      {
        "index": 1
      },
      {
        "index": 2
      }
    ],
    "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
    "favouriteFood": [
      "orange",
      "apple",
      "banana",
      "strawberry"
    ]
  },
  {
    "_id": "595eeb9b1e0d8942524c98ad",
    "index": 1,
    "guid": "b057bb65-e335-450e-b6d2-d4cc859ff6cc",
    "has_died": false,
    "balance": "$1,562.58",
    "picture": "http://placehold.it/32x32",
    "age": 60,
    "eyeColor": "brown",
    "name": "Decker Mckenzie",
    "gender": "male",
    "company_id": 2,
    "email": "deckermckenzie@earthmark.com",
    "phone": "+1 (893) 587-3311",
    "address": "492 Stockton Street, Lawrence, Guam, 4854",
    "about": "Consectetur aute consectetur dolor aliquip dolor sit id.",
    "registered": "2017-06-25T10:03:49 -10:00",
    "tags": [
      "veniam",
      "irure",
      "mollit",
      "sunt",
      "amet",
      "fugiat",
      "ex"
    ],
    "friends": [
      {
        "index": 0
      },
      {
        "index": 1
      },
      {
        "index": 2
      },
      {
        "index": 5
      }
    ],
    "greeting": "Hello, Decker Mckenzie! You have 2 unread messages.",
    "favouriteFood": [
      "cucumber",
      "beetroot",
      "carrot",
      "celery"
    ]
  },
  {
    "_id": "595eeb9bb3821d9982ea44f9",
    "index": 2,
    "guid": "49c04b8d-0a96-4319-b310-d6aa8269adca",
    "has_died": false,
    "balance": "$2,119.44",
    "picture": "http://placehold.it/32x32",
    "age": 54,
    "eyeColor": "blue",
    "name": "Bonnie Bass",
    "gender": "female",
    "company_id": 1,
    "email": "bonniebass@earthmark.com",
    "phone": "+1 (823) 428-3710",
    "address": "455 Dictum Court, Nadine, Mississippi, 6499",
    "about": "Non voluptate reprehenderit ad elit veniam nulla ut ea ex.",
    "registered": "2017-06-08T04:23:18 -10:00",
    "tags": [
      "quis",
      "sunt",
      "sit",
      "aliquip",
      "pariatur",
      "quis",
      "nulla"
    ],
    "friends": [
      {
        "index": 0
      },
      {
        "index": 1
      },
      {
        "index": 2
      }
    ],
    "greeting": "Hello, Bonnie Bass! You have 10 unread messages.",
    "favouriteFood": [
      "orange",
      "beetroot",
      "banana",
      "strawberry"
    ]
  },
  {
    "_id": "595zzza9bb3821d9982ea44f9",
    "index":3,
    "guid": "49z04b8z-0z96-4319-b310-d6aa8269adca",
    "has_died": false,
    "balance": "$2,119.44",
    "picture": "http://placehold.it/32x32",
    "age": 54,
    "eyeColor": "blue",
    "name": "Bronnie Brass",
    "gender": "female",
    "company_id": 0,
    "email": "bronniebrass@earthmark.com",
    "phone": "+1 (823) 428-3710",
    "address": "455 Dictum Court, Nadine, Mississippi, 6499",
    "about": "Non voluptate reprehenderit ad elit veniam nulla ut ea ex.",
    "registered": "2017-06-08T04:23:18 -10:00",
    "tags": [
      "quis",
      "sunt",
      "sit",
      "aliquip",
      "pariatur",
      "quis",
      "nulla"
    ],
    "friends": [],
    "greeting": "Hello, Bronnie Brass! You have 10 unread messages.",
    "favouriteFood": [
      "orange",
      "beetroot",
      "banana",
      "strawberry"
    ]
  }
]
"""


class TestLoader(TestCase):
    def test_split_favourite_food(self):
        favourite_food = ["cucumber", "beetroot", "strawberry", "cookie"]
        (fruits, vegetables, unknown) = loader.split_favourite_food(favourite_food)

        self.assertIn("cucumber", vegetables)
        self.assertIn("beetroot", vegetables)
        self.assertIn("strawberry", fruits)
        self.assertIn("cookie", unknown)

    def test_get_fruits(self):
        fruits = ["apple", "strawberry"]
        objs = loader.get_fruits(fruits)
        self.assertTrue(len(objs) > 0)
        for f in objs:
            self.assertIsInstance(f, Fruit)

    def test_get_vegetables(self):
        vegetables = ["cucumber", "beetroot"]
        objs = loader.get_vegetables(vegetables)
        self.assertTrue(len(objs) > 0)
        for f in objs:
            self.assertIsInstance(f, Vegetable)

    def test_get_tags(self):
        tags = ["cupidatat", "id", "anim", "tempor"]
        objs = loader.get_tags(tags)
        self.assertTrue(len(objs) > 0)
        for o in objs:
            self.assertIsInstance(o, Tag)

    def test_get_company(self):
        company = "5"
        # Return None when company doesn't exist
        self.assertIsNone(loader.get_company(company))

        Company.objects.create(index=5)
        obj = loader.get_company(company)
        self.assertIsInstance(obj, Company)

    def test_currency_to_decimal(self):
        currency = "$2,418.59"
        # Empty string returns 0
        self.assertEqual(0, loader.currency_to_decimal(""))
        # Wrong representation of currency returns 0
        self.assertEqual(0, loader.currency_to_decimal("AUD2345"))
        # String representing currency return decimal values
        result = loader.currency_to_decimal(currency)
        self.assertIsInstance(result, Decimal)
        self.assertEqual(Decimal(2418.59), result)

    def test_format_date(self):
        input_date = "2016-07-13T12:29:07 -10:00"
        output_date = "2016-07-13 02:29:07"
        self.assertEqual(output_date, loader.format_date(input_date))

    def test_get_person(self):
        Company.objects.create(index=0, name="NETBOOK")
        Company.objects.create(index=1, name="NETBOOK")
        Company.objects.create(index=2, name="NETBOOK")

        data = json.loads(PEOPLE)
        # Return None when person is empty
        self.assertIsNone(loader.get_person({}, data))
        # Return a Person object on success
        self.assertIsInstance(loader.get_person(data[0], data), Person)

    @skip
    def test_get_friends(self):
        """
        Person is { 
            index: int,
            friends: [Person]
            }

        def fn_for_person(person):
            ... person['index'], 
                fn_for_lop(person['friends'])

        def fn_for_lop(people):
            if not people:
                ... 
            else:
                ... fn_for_person(people[0]), fn_for_lop(people[1:])

        ----
        json_data = data

        def fn_for_person(person):
            # Prerequisite: person must contain all raw data
            obj = cls.objects.get_or_create(
                person['index']
            )
            obj.add(*fn_for_lop(person['friends']))
            return obj

        def fn_for_lop(people):
            if not people:
                return []
            else:
                if obj = cls.objects.get('index'=people[0]['index']):
                    return [obj] + fn_for_lop(people[1:])
                else:
                    return [fn_for_person(find_person(people[0], json_data))] + fn_for_lop(people[1:])
        """
        person0 = {"index": 0, "friends": [{"index": 1}]}
        person1 = {"index": 1, "friends": [{"index": 2}, {"index": 0}]}
        person2 = {"index": 2, "friends": [{"index": 1}]}
        people = [person0, person1, person2]
        objs = Person.get_friends(person0["friends"], people)
        self.assertTrue(len(objs) > 0)
        for o in objs:
            self.assertIsInstance(o, Person)
