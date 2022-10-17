from django.forms import BooleanField, IntegerField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Page, Tag
from api.services.page_service import page_create, page_update


class PageSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, required=False)
    owner = serializers.StringRelatedField()
    followers = serializers.StringRelatedField(many=True, required=False)
    follow_requests = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Page
        fields = ('pk', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'image', 'is_private', 'follow_requests', 'unblock_date', 'is_permanent_block', 'posts')


class PageAnonymousSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, required=False)
    owner = serializers.StringRelatedField()

    class Meta:
        model = Page
        fields = ('name', 'description', 'tags', 'owner',
                  'image', 'is_private', 'posts')


class CreatePageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description',
                  'tags', 'image', 'is_private', 'owner', )

    def create(self, validated_data):
        return page_create(validated_data, self.context["request"].user)


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'image', 'is_private', )

    def update(self, instance, validated_data):
        return page_update(instance, validated_data)


class FollowRequestActionSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all())
    is_accept = serializers.BooleanField()


class AllFollowRequestActionSerializer(serializers.Serializer):
    is_accept = serializers.BooleanField()


class TagNameSerializer(serializers.Serializer):
    tag_id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())


class BlockSerializer(serializers.Serializer):
    unblock_date = serializers.DateTimeField(required=False)
    is_permanent = serializers.BooleanField(required=False)

    def validate(self, data):
        if 'unblock_date' not in data and ('is_permanent' not in data or data['is_permanent'] is False):
            raise serializers.ValidationError(
                {"unblock_date": "You must specify either of the fields", "is_permanent": "You must specify either of the fields"})
        if 'unblock_date' in data and 'is_permanent' in data and data['is_permanent'] is True:
            raise serializers.ValidationError(
                {"unblock_date": "You must specify either of the fields", "is_permanent": "You must specify either of the fields"})
        return data
