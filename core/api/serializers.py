from rest_framework import serializers
from api.models import Customer

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('pk', 'name', 'email', 'created')