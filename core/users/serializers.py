from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.user_service import user_create_service, user_update_service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'image_path', 'role', 'title',
                  'is_blocked', 'date_joined', 'likes', 'pages', 'follows', 'requests', )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',  'email', 'title',)

    def create(self, validated_data):
        return user_create_service(validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',  'email', 'image_path', 'title', )

    def update(self, instance, validated_data):
        return user_update_service(instance, validated_data)
