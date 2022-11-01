from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer, RegistrateUserSerializer, UpdateAvatarSerializer, BlockUserSerializer
from users import user_service as services
from users.permissions import IsAdmin, IsModerator, IsSelfUser, IsUser, IsNotAuthenticated
from api.serializers.post_serializer import PostSerializer


class UserAllViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    '''
    Implements Create User and Get all Users
    '''
    serializer_classes = {
        'list': UserSerializer,
        'create': CreateUserSerializer,
        'registrate': RegistrateUserSerializer,
        'find_user': UserSerializer,
    }
    permissions = {
        'list': (AllowAny,),
        'create': (IsAdmin | IsModerator,),
        'registrate': (IsNotAuthenticated,),
        'find_user': (AllowAny,),
    }
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes.get(self.action)
        return UserSerializer

    def get_permissions(self):
        permissions = []
        if self.action in self.permissions:
            permissions = self.permissions[self.action]
        return [permission() for permission in permissions]

    def get_queryset(self):
        return services.user_list_service()

    @action(detail=False, methods=['POST'])
    def registrate(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.registrate(request.data)
        return Response({"message": msg}, _status)

    @action(detail=False, methods=['GET'])
    def find_user(self, request, pk=None):
        """
        Provides finding user by username, title
        """
        username = request.query_params.get('username')
        title = request.query_params.get('title')
        if username == None:
            return Response("Must be specified fields", status.HTTP_400_BAD_REQUEST)
        queryset = services.find_user(username, title)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    '''
    Implements Retrieve, Update, Destroy User
    '''
    serializer_classes = {
        'update': UpdateUserSerializer,
        'retrieve': UserSerializer,
        'destroy': UserSerializer,
        'update_avatar': UpdateAvatarSerializer,
        'block': BlockUserSerializer,
        'mynews': PostSerializer,
    }
    permissions = {
        'update': (IsSelfUser | IsAdmin | IsModerator,),
        'partial_update': (IsSelfUser | IsAdmin | IsModerator,),
        'retrieve': (AllowAny,),
        'destroy': (IsAdmin | IsModerator,),
        'update_avatar': (IsSelfUser,),
        'block': (IsAdmin,),
        'mynews': (IsSelfUser,),
    }
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes.get(self.action)
        return UserSerializer

    def get_permissions(self):
        permissions = []
        if self.action in self.permissions:
            permissions = self.permissions[self.action]
        return [permission() for permission in permissions]

    def retrieve(self, request, *args, **kwargs):
        instance = services.user_retrieve_service(self.kwargs['pk'])
        # self.get_permissions().check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        services.user_delete_service(instance)

    @action(detail=True, methods=['POST'])
    def update_avatar(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.update_avatar(pk, request.FILES.get('image_uploaded'))
        return Response({"message": msg}, _status, request.user)

    @action(detail=True, methods=['POST'])
    def block(self, request, pk=None):
        """
        For admins and moderators
        Provide permanently blocking user
        """
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.block(pk, request.data)
        return Response({"message": msg}, _status, request.user)

    @action(detail=True, methods=['GET'])
    def mynews(self, request, pk=None):
        """
        Show posts of subscribed pages
        """
        queryset = services.mynews_posts(self.get_object())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
