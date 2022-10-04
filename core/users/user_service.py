from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries

from api.models import Page

# reset_queries()
# print(connection.queries)


def user_list_service():
    return get_user_model().objects.all()


def user_create_service(validated_data):
    user = get_user_model().objects.create(**validated_data)
    return user


def user_update_service(instance, validated_data):
    instance.username = validated_data["username"]
    instance.password = validated_data["password"]
    instance.email = validated_data["email"]
    instance.image_path = validated_data["image_path"]
    instance.title = validated_data["title"]
    instance.save()
    return instance


def user_retrieve_service(id: int):
    return get_object_or_404(get_user_model(), pk=id)


def user_delete_service(instance):
    instance.delete()
