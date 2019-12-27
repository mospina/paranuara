import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from people.tests.factories import PersonFactory
from .factories import CompanyFactory


class CompanyViewTest(TestCase):
    def set_data(self):
        self.company1 = CompanyFactory(index=1, name="Company")
        self.company2 = CompanyFactory(index=2, name="Corporation")
        self.company3 = CompanyFactory(index=3, name="Enterprise")

        self.person1 = PersonFactory(index=1, company=self.company1)
        self.person2 = PersonFactory(index=2, company=self.company1)
        self.person3 = PersonFactory(index=3, company=self.company1)
        self.person4 = PersonFactory(index=4, company=self.company3)

    def setUp(self):
        self.client = APIClient()
        self.base_url = "/v1/companies/{company_index}"
        self.set_data()

    def test_company_get_returns_200(self):
        response = self.client.get(
            self.base_url.format(company_index=self.company1.index)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")

    def test_company_get_returns_list_of_employees(self):
        response = self.client.get(
            self.base_url.format(company_index=self.company1.index)
        )
        self.assertEqual(json.loads(response.content)["employees"], [1, 2, 3])

    def test_company_get_returns_empty_list(self):
        response = self.client.get(
            self.base_url.format(company_index=self.company2.index)
        )
        self.assertEqual(json.loads(response.content)["employees"], [])
