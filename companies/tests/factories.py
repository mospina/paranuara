from factory.django import DjangoModelFactory
from factory import Sequence

from companies.models import Company

class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    index = Sequence(lambda n: n)
    name = 'Company'
