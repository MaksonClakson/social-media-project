from django.shortcuts import render
from api.models import Customer
from rest_framework import viewsets
from rest_framework import mixins
from api.serializers import CustomSerializer

class CustomerAllViewSet(mixins.ListModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):
    # API endpoint that allows creation of a new customer
    serializer_class = CustomSerializer
    queryset = Customer.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CustomerViewSet(mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    # API endpoint that allows customer to be viewed
    queryset = Customer.objects.all()
    serializer_class = CustomSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)