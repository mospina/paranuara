from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Company
from .serializers import CompanySerializer

# Create your views here.
class CompanyDetail(APIView):
    """
    Retrieve a company
    """

    def get_object(self, index):
        try:
            return Company.objects.get(index=index)
        except Company.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, index, format=None):
        company = self.get_object(index)
        serializer = CompanySerializer(company)
        return Response(serializer.data)
