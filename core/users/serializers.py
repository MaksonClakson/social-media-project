from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.user_service import user_create_service, user_update_service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'image_path', 'role', 'title',
                  'is_blocked', 'date_joined', 'pages', 'follows', )


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'image_path', )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',  'email', )

    def create(self, validated_data):
        return user_create_service(validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',  'email', 'title', )

    def update(self, instance, validated_data):
        return user_update_service(instance, validated_data)


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)

    def update(self, instance, validated_data):
        return user_update_service(instance, validated_data)


class RegistrateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2', 'email', )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs


class UpdateAvatarSerializer(serializers.Serializer):
    image_uploaded = serializers.FileField()
    # image_path = serializers.URLField(max_length=200)


class BlockUserSerializer(serializers.Serializer):
    to_block = serializers.BooleanField()
