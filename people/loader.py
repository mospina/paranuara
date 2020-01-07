import json
from decimal import Decimal
import re
from datetime import datetime, timedelta
import logging

from companies.models import Company
from people.models import Tag, Fruit, Vegetable, Person
from people.models import KNOWN_FRUITS, KNOWN_VEGETABLES

logger = logging.getLogger(__name__)


def load_data_from_file(file_path):
    with open(file_path, newline="") as fh:
        json_data = json.load(fh)
    fh.close()

    for entry in json_data:
        get_person(entry, json_data)


def get_person(person, data):
    if not person:
        return None

    fruits, vegetables, _unknown = split_favourite_food(person["favouriteFood"])

    obj, _ = Person.objects.get_or_create(
        index=person["index"],
        defaults={
            "_id": person["_id"],
            "guid": person["guid"],
            "has_died": person["has_died"],
            "balance": currency_to_decimal(person["balance"]),
            "picture": person["picture"],
            "age": person["age"],
            "eyeColor": person["eyeColor"],
            "name": person["name"],
            "gender": get_gender(person["gender"]),
            "email": person["email"],
            "phone": person["phone"],
            "address": person["address"],
            "about": person["about"],
            "registered": format_date(person["registered"]),
            "greeting": person["greeting"],
        },
    )
    obj.tags.add(*get_tags(person["tags"]))
    # favouriteFood
    obj.favouriteFruits.add(*get_fruits(fruits))
    obj.favouriteVegetables.add(*get_vegetables(vegetables))
    # friends
    friends = get_friends(
        [p for p in person["friends"] if p["index"] != person["index"]], data
    )
    for friend in friends:
        if friend:
            obj.friends.add(friend)
    # company
    company = get_company(person["company_id"])
    if company:
        obj.company = company

    obj.save()
    return obj


def get_friends(friends, data):
    """
    Given a list of friends' ids return a list of Person Objects

    [{index: int}], data -> [Person]
    - index: is the unique identifier for a person given in the data
    - data: is the list of people in json format
    """
    if not friends:
        return []

    head, tail = friends[0], friends[1:]
    try:
        obj = Person.objects.get(index=head["index"])
    except Person.DoesNotExist:
        friend = find_friend(head["index"], data)
        return [get_person(friend, data)] + get_friends(tail, data)
    else:
        return [obj] + get_friends(tail, data)


def find_friend(index, data):
    """
    Return person entry with id index from the data.

    number, data -> person

    index: a integer representing the unique identifier of the person
    data: a json representation of the a list of people
    person: a json representation of a person
    """
    person = [p for p in data if p["index"] == index]
    return person[0] if person else {}


def get_company(company_index):
    """
    Try to search for a matching company in the RDB.
    Return object on success or raise an error.
    """
    try:
        obj = Company.objects.get(index=company_index)
    except Company.DoesNotExist:
        logger.warning("Company {} doesn't exist".format(company_index))
        return None
        # raise Company.DoesNotExist("{} doesn't exist. Load companies first.".format(company_index))
    else:
        return obj


def get_fruits(fruits):
    """
    Given a list of fruit names return a list of Fruit Objects
    [str] -> [Fruit]
    """
    objs = [Fruit.objects.get_or_create(name=f) for f in fruits]
    return [f for f, _ in objs]


def get_vegetables(vegetables):
    """
    Given a list of vegetable names return a list of Vegetable Objects
    [str] -> [Fruit]
    """
    objs = [Vegetable.objects.get_or_create(name=v) for v in vegetables]
    return [v for v, _ in objs]


def get_tags(tags):
    """
    Given a list of tags return a list of Tag Objects
    [str] -> [Tag]
    """
    objs = [Tag.objects.get_or_create(label=t) for t in tags]
    return [t for t, _ in objs]


def currency_to_decimal(currency):
    """
    Given a string representing a currency, return a decimal.
    [Currency] -> decimal
    where Currency is a string of the format '$ number
    """
    if not currency:
        return Decimal(0)

    regex = re.compile(r"\$(?P<quantity>[\d,.]+)")
    match = regex.match(currency)
    if not match:
        return Decimal(0)

    value = match.group("quantity").replace(",", "")

    return Decimal(float(value))


def format_date(date):
    """
    Given a date in an unsupported format, return a django supported string
    string -> string
    """
    regex = re.compile(
        r"(?P<Y>\d+)-(?P<m>\d+)-(?P<d>\d+)T(?P<H>\d+):(?P<M>\d+):(?P<S>\d+)\s*-(?P<OH>\d+):(?P<OM>\d+)"
    )
    match = regex.match(date)
    if not match:
        dt = datetime.now()
    else:
        dt = datetime(
            int(match.group("Y")),
            int(match.group("m")),
            int(match.group("d")),
            int(match.group("H")),
            int(match.group("M")),
            int(match.group("S")),
        ) - timedelta(hours=int(match.group("OH")), minutes=int(match.group("OM")))

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def split_favourite_food(
    list_of_food, known_fruits=KNOWN_FRUITS, known_vegetables=KNOWN_VEGETABLES
):
    """
    Given a list of food, it split it into fruits, vegetables and unknown.

    ([list_of_food],
     [known_fruits],
     [known_vegetables]) -> ([fruits], [vegetables], [unknown])

    where:

    list_of_food = List of strings representing food to be split
    known_fruits = list of strings representing fruits that are known
    known_vegetables = list of strings representing vegetables that are known

    Return a tuple that include a list of fruits, a list of vegetables and
    a list of unknown food.
    """

    fruits = []
    vegetables = []
    unknown = []

    for i in list_of_food:
        if i in known_fruits:
            fruits.append(i)
        elif i in known_vegetables:
            vegetables.append(i)
        else:
            unknown.append(i)

    return (fruits, vegetables, unknown)


def get_gender(gender):
    gender = gender.capitalize()

    if gender in ("M", "Male"):
        return "M"

    if gender in ("F", "Female"):
        return "F"

    return "N"
