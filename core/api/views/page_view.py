from datetime import datetime
import json
import requests
import asyncio
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework import status

from api.models import Page
from api.serializers.page_serializer import FollowRequestActionSerializer, PageSerializer, CreatePageSerializer, UpdatePageSerializer, PageAnonymousSerializer, AllFollowRequestActionSerializer, TagNameSerializer, BlockSerializer
from api.serializers.post_serializer import PostSerializer
from api.services import page_service as services
from users.serializers import UserNameSerializer
from users.permissions import IsPageOwner, IsAdmin, IsModerator, IsUser
from core.producer import CommandTypes, CONTAINER_MESSAGES_IP


class PageAllViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    '''
    Implements Create page and Get all pages
    '''
    # permission_classes = (IsAuthenticated,)
    serializer_classes = {
        'list': PageSerializer,
        'create': CreatePageSerializer,
        'mypages': PageSerializer,
        'find_pages': PageSerializer,
    }
    permissions = {
        'list': (AllowAny,),
        'create': (IsUser,),
        'mypages': (IsUser,),
        'find_pages': (AllowAny,),
    }
    queryset = Page.objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes.get(self.action)
        return PageSerializer

    def get_permissions(self):
        permissions = []
        if self.action in self.permissions:
            permissions = self.permissions[self.action]
        return [permission() for permission in permissions]

    def get_queryset(self):
        return services.page_list()

    @action(detail=False, methods=['GET'])
    def mypages(self, request, pk=None):
        """
        Show all pages whose owner is a current user
        """
        queryset = services.mypages_list_service(request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def find_pages(self, request, pk=None):
        """
        Provides finding pages by name, uuid, tag
        """
        name = request.query_params.get('name')
        uuid = request.query_params.get('uuid')
        tag = request.query_params.get('tag')
        if (name == None) | (uuid == None) | (tag == None):
            return Response("Must be specified 3 fields", status.HTTP_400_BAD_REQUEST)
        queryset = services.find_pages(name, uuid, tag)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PageViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    '''
    Implements Retrieve, Update, Destroy page
    '''
    serializer_classes = {
        'update': UpdatePageSerializer,
        'partial_update': UpdatePageSerializer,
        'retrieve': PageSerializer,
        'destroy': PageSerializer,
        'myposts': PostSerializer,
        'follow_requests': UserNameSerializer,
        'follow_request_action': FollowRequestActionSerializer,
        'all_follow_request_action': AllFollowRequestActionSerializer,
        'add_tag': TagNameSerializer,
        'remove_tag': TagNameSerializer,
        'block': BlockSerializer,
    }
    permissions = {
        'update': (IsPageOwner | IsAdmin | IsModerator,),
        'partial_update': (IsPageOwner | IsAdmin | IsModerator,),
        'retrieve': (AllowAny,),
        'destroy': (IsPageOwner,),
        'myposts': (IsPageOwner,),
        'subscribe': (IsUser,),
        'follow_requests': (IsPageOwner,),
        'follow_request_action': (IsPageOwner,),
        'add_tag': (IsPageOwner,),
        'remove_tag': (IsPageOwner,),
        'block': (IsAdmin | IsModerator,),
        'unblock': (IsAdmin | IsModerator,),
    }
    queryset = Page.objects.all()

    def get_serializer_class(self):
        if type(self.request.user) is AnonymousUser:
            return PageAnonymousSerializer
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permissions = []
        if self.action in self.permissions:
            permissions = self.permissions[self.action]
        return [permission() for permission in permissions]

    def retrieve(self, request, *args, **kwargs):
        instance = services.page_retrieve(self.kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        services.page_delete(instance)

    def perform_update(self, serializer):
        serializer.save()
        response = requests.delete(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.DELETE_PAGE}', data=json.dumps({'page_id': self.get_object().pk, 'user_id': self.request.user.pk, 'page_name': self.get_object().name}))
        if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
            return "Error with statistic microservice", response.status_code

    @action(detail=True, methods=['GET'])
    def myposts(self, request, pk=None):
        """
        Show posts of one particular owner page 
        """
        queryset = services.posts_of_page(pk)
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def subscribe(self, request, pk=None):
        """
        Provide subscribing on public page or sending follow request to private page
        """
        msg, _status = services.subscribe(pk, request.user)
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['POST'])
    def unsubscribe(self, request, pk=None):
        """
        Provide unsubscribing on public page or undo sending follow request to private page
        """
        msg, _status = services.unsubscribe(pk, request.user)
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['GET'])
    def follow_requests(self, request, pk=None):
        """
        Show follow requests of the page
        """
        data, status = services.follow_requests(pk)
        if isinstance(data, QuerySet):
            serializer = self.get_serializer(data, many=True)
            data = serializer.data
        return Response(data, status)

    @action(detail=True, methods=['POST'])
    def follow_request_action(self, request, pk=None):
        """
        Provide accept or reject one follow request
        """
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.follow_request_aciton(pk, request.data)
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['POST'])
    def all_follow_request_action(self, request, pk=None):
        """
        Provide accept or reject all follow requests
        """
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.all_follow_request_aciton(pk, request.data)
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['POST'])
    def add_tag(self, request, pk=None):
        """
        Provide adding tag to the page
        """
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.add_tag(pk, request.data)
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['POST'])
    def remove_tag(self, request, pk=None):
        """
        Provide removing tag from the page
        """
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.remove_tag(pk, request.data)
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['POST'])
    def block(self, request, pk=None):
        """
        For admin and moderator
        Provide blocking page permanently or for particular time
        """
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        msg, _status = services.block(self.get_object(), request.data)
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['POST'])
    def unblock(self, request, pk=None):
        """
        For admin and moderator
        Provide unblocking page
        """
        msg, _status = services.unblock(self.get_object())
        return Response({"message": msg}, _status)

    @action(detail=True, methods=['POST'])
    def get_stat(self, request, pk=None):
        """
        Return statistic from microservice regarding certain page
        """
        msg = services.get_stat(self.get_object())
        return Response({"message": msg})
