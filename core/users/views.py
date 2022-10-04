from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer
from users.user_service import user_delete_service, user_list_service, user_retrieve_service


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    '''
    Implements Retrieve, Update, Destroy User
    '''
    serializer_classes = {'update': UpdateUserSerializer,
                        'retrieve': UserSerializer,
                        'destroy': UserSerializer}
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        return self.get_serializer_classes.get(self.action)

    def retrieve(self, request, *args, **kwargs):
        instance = user_retrieve_service(self.kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        user_delete_service(instance)


class UserAllViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    '''
    Implements Create User and Get all Users
    '''
    serializer_classes = {'list': UpdateUserSerializer,
                        'create': CreateUserSerializer,}
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        return self.get_serializer_classes.get(self.action)

    def get_queryset(self):
        return user_list_service()
