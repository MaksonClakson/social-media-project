from django.shortcuts import render
from .models import *
from rest_framework import generics
from .serializers import *

class CustomerCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new customer
    queryset = Customer.objects.all(),
    serializer_class = CustomSerializer

class CustomerList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed
    queryset = Customer.objects.all()
    serializer_class = CustomSerializer

class CustomerDetail(generics.RetrieveAPIView):
    # API endpoint that returns a single customer by pk
    queryset = Customer.objects.all()
    serializer_class = CustomSerializer

class CustomerUpdate(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a customer record to be updated
    queryset = Customer.objects.all()
    serializer_class = CustomSerializer

class CustomerDelete(generics.RetrieveDestroyAPIView):
    # API endpoint that allows a customer record to be updated
    queryset = Customer.objects.all()
    serializer_class = CustomSerializer