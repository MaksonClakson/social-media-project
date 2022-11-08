from rest_framework import status
from rest_framework import serializers

from api.models import Post
from api.services.post_service import post_create_service, post_update_service


class PostSerializer(serializers.ModelSerializer):
    page = serializers.StringRelatedField()
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    likes = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Post
        fields = ('pk', 'page', 'content', 'reply_to',
                  'likes', 'created_at', 'updated_at',)


class CreatePostSerializer(serializers.ModelSerializer):
    # reply_to = serializers.StringRelatedField(required=False)
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to')

    def create(self, validated_data):
        response, _status = post_create_service(
            validated_data, self['context'].user)
        if _status is not status.HTTP_201_CREATED:
            raise serializers.ValidationError(response)
        return response


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content',)

    def update(self, instance, validated_data):
        return post_update_service(instance, validated_data)
