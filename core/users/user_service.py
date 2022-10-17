from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries
from django.db.models import Q
from rest_framework import status

from itertools import chain

from api.models import Page, Post


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
    instance.save(update_fields=['username', 'password', 'email', 'image_path', 'title'])
    return instance


def user_retrieve_service(id: int):
    return get_object_or_404(get_user_model(), pk=id)


def user_delete_service(instance):
    instance.delete()


def registrate(data):
    user = get_user_model().objects.create(
        username=data['username'],
        email=data['email'],
    )
    user.set_password(data['password'])
    user.save(update_fields=['password'])
    return "You have successfully registrated", status.HTTP_201_CREATED


def update_avatar(user_pk, data):
    user = get_object_or_404(get_user_model().objects, )
    user.image_path = data['image_path']
    return "Image path has been updated", status.HTTP_200_OK


def block(user_pk, data):
    to_block = data['to_block']
    user = get_user_model().objects.get(pk=user_pk)
    for page in user.pages:
        page.is_permanent_block = True
        page.unblock_date = None
    if to_block:
        user.is_blocked = True
        user.save(update_fields=['is_blocked', 'unblock_date'])
        return "User blocked", status.HTTP_200_OK
    else:
        user.is_blocked = False
        user.save(update_fields=['is_blocked', 'unblock_date'])
        return "User unblocked", status.HTTP_200_OK


def mynews_posts(user):
    my_pages = user.pages.all()
    followed_pages = user.follows.all()
    reset_queries()
    posts = Post.objects.filter(
        Q(page__in=my_pages) | Q(page__in=followed_pages))[:20]
    return posts
