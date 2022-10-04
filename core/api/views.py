from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from api.models import Tag, Page, Post
from api.serializers.tag_serializer import TagSerializer
from api.serializers.page_serializer import PageSerializer, CreatePageSerializer, UpdatePageSerializer
from api.serializers.post_serializer import PostSerializer, CreatePostSerializer, UpdatePostSerializer
from api.services.tag_service import tag_list_service, tag_retrieve_service, tag_delete_service
from api.services.page_service import page_list_service, page_retrieve_service, page_delete_service
from api.services.post_service import post_list_service, post_retrieve_service, post_delete_service


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


class PageAllViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    '''
    Implements Create page and Get all pages
    '''
    serializer_classes = {'list': PageSerializer,
                        'create': CreatePageSerializer}
    queryset = Page.objects.all()

    def get_serializer_class(self):
        return self.get_serializer_classes.get(self.action)

    def get_queryset(self):
        return page_list_service()


class PageViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    '''
    Implements Retrieve, Update, Destroy page
    '''
    serializer_classes = {'update': UpdatePageSerializer,
                        'retrieve': PageSerializer,
                        'destroy': PageSerializer}
    queryset = Page.objects.all()

    def get_serializer_class(self):
        return self.get_serializer_classes.get(self.action)

    def retrieve(self, request, *args, **kwargs):
        instance = page_retrieve_service(self.kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        page_delete_service(instance)


class PostAllViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    '''
    Implements Create post and Get all posts
    '''
    serializer_classes = {'list': PostSerializer,
                        'create': CreatePostSerializer}
    queryset = Post.objects.all()

    def get_serializer_class(self):
        return self.get_serializer_classes.get(self.action)

    def get_queryset(self):
        return post_list_service()


class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    '''
    Implements Retrieve, Update, Destroy post
    '''
    serializer_classes = {'update': UpdatePostSerializer,
                        'retrieve': PostSerializer,
                        'destroy': PostSerializer}
    queryset = Post.objects.all()

    def get_serializer_class(self):
        return self.get_serializer_classes.get(self.action)

    def retrieve(self, request, *args, **kwargs):
        instance = post_retrieve_service(self.kwargs['pk'])
        serializer = self.get_serializer(instance)
        print(repr(UpdatePostSerializer()))
        return Response(serializer.data)

    def perform_destroy(self, instance):
        post_delete_service(instance)
