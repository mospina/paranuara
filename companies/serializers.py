from rest_framework import serializers

from companies.models import Company

class CompanySerializer(serializers.ModelSerializer):

    employees = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'index', 'name', 'employees')


