from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import action
from rest_framework import status

from api.models import Tag, Page, Post
from api.serializers.tag_serializer import TagSerializer
from api.serializers.page_serializer import PageSerializer, CreatePageSerializer, UpdatePageSerializer, PageAnonymousSerializer
from api.serializers.post_serializer import PostSerializer, CreatePostSerializer, UpdatePostSerializer
from api.services.tag_service import tag_list_service, tag_retrieve_service, tag_delete_service
from api.services.page_service import page_list, page_retrieve, page_delete
from api.services.post_service import post_list_service, post_retrieve_service, post_delete_service, like_post_service
from users.permissions import IsPageOwner, IsPostOwnerOrAdminOrReadOnly, IsPostOwner, IsAdmin, IsModerator, IsUser


class PostAllViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    '''
    Implements Create post and Get all posts
    '''
    serializer_classes = {
        'list': PostSerializer,
        'create': CreatePostSerializer}
    permissions = {
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'destroy': (AllowAny,),
        'myposts': (IsPageOwner,),
        'follow_requests': (IsUser,),
        'send_follow_request': (IsUser,),
    }
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes.get(self.action)
        return PostSerializer

    def get_permissions(self):
        permissions = []
        if self.action in self.permissions:
            permissions = self.permissions[self.action]
        return [permission() for permission in permissions]

    def get_queryset(self):
        return post_list_service()


class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    '''
    Implements Retrieve, Update, Destroy post
    '''
    # permission_classes = (IsPostOwnerOrAdminOrReadOnly, )
    # permission_classes = (IsAuthenticated, )
    serializer_classes = {
        'update': UpdatePostSerializer,
        'partial_update': UpdatePostSerializer,
        'retrieve': PostSerializer,
        'destroy': PostSerializer}
    permissions = {
        'retrieve': (AllowAny,),
        'update': (IsPostOwner | IsAdmin | IsModerator,),
        'partial_update': (IsPostOwner | IsAdmin | IsModerator,),
        'destroy': (IsPostOwner | IsAdmin | IsModerator,),
        'like_post': (IsAuthenticated,),
    }
    queryset = Post.objects.all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permissions = []
        if self.action in self.permissions:
            permissions = self.permissions[self.action]
        return [permission() for permission in permissions]

    def retrieve(self, request, *args, **kwargs):
        instance = post_retrieve_service(self.kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        post_delete_service(instance)

    @action(detail=True, methods=['POST'], url_path='like')
    def like_post(self, request, pk=None):
        """
        Provides hitting likes on a particular post
        """
        msg, status = like_post_service(request, self.get_object())
        return Response({'message': msg}, status=status)
