from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Page
from api.services.page_service import page_create_service, page_update_service


class PageSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, required=False)
    owner = serializers.StringRelatedField()
    followers = serializers.StringRelatedField(many=True, required=False)
    owner = serializers.StringRelatedField()
    likes = serializers.StringRelatedField(many=True, required=False)
    follow_requests = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Page
        fields = ('pk', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'likes', 'image', 'is_private', 'follow_requests', 'unblock_date', 'posts')


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description',
                  'tags', 'image', 'is_private',)

    def create(self, validated_data):
        return page_create_service(validated_data, self.context["request"].user)


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'tags', 'is_private',)

    def update(self, instance, validated_data):
        return page_update_service(instance, validated_data)
