import json
import requests

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries
from rest_framework import status
from rest_framework.exceptions import NotFound

from api.models import Post
from api.tasks import notify_follower_about_new_post
from core.producer import CommandTypes, CONTAINER_MESSAGES_IP


def post_list_service():
    return Post.objects.all()


def post_create_service(validated_data, user):
    page_data = validated_data.pop('page')
    reply_to_data = validated_data.pop('reply_to')
    if page_data in user.pages:
        return None
    post = Post.objects.create(
        page=page_data, reply_to=reply_to_data, **validated_data
    )

    for follower in page_data.followers.all():
        response = notify_follower_about_new_post(
            page_data.name, post.content, follower.email)
        print(f"{response.__dict__= }")

    return post


def post_update_service(instance, validated_data):
    instance.content = validated_data["content"]

    if instance.page.is_permanent_block or instance.page.unblock_date != None:
        raise NotFound(detail="Page is blocked", code=None)
    instance.save()
    return instance


def post_retrieve_service(id: int):
    return get_object_or_404(Post, pk=id)


def post_delete_service(instance):
    for likes in list(instance.likes.all()):
        response = requests.post(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.UNDO_PAGE_LIKE}/', data=json.dumps({'page_id': instance.page.pk}))
    instance.delete()


def like_post_service(request, post):
    if post.likes.filter(pk=request.user.id).exists():
        post.likes.remove(request.user)
        msg = "Unliked"
        response = requests.post(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.UNDO_PAGE_LIKE}/', data=json.dumps({'page_id': post.page.pk}))
    else:
        post.likes.add(request.user)
        msg = "Liked"
        response = requests.post(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.NEW_PAGE_LIKE}/', data=json.dumps({'page_id': post.page.pk}))
    if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
        return "Error with statistic microservice", response.status_code
    return msg, status.HTTP_200_OK
