from rest_framework import serializers
from .models import *

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['pk', 'name', 'email', 'created']