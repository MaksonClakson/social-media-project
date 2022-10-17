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
from users.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly, IsPostOwnerOrAdminOrReadOnly, IsPostOwner, IsAdmin, IsModerator


class TagAllViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    '''
    Implements Create tag and Get all tags
    '''
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        return tag_list_service()


class TagViewSet(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    '''
    Implements Retrieve tag, Update tag, Destroy tag
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = tag_retrieve_service(self.kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        tag_delete_service(instance)
