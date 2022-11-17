import json
import requests

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound

from api.models import Post
from api import tasks
from core.producer import CommandTypes, CONTAINER_MESSAGES_IP


def post_list_service():
    return Post.objects.all()


def post_create_service(validated_data, user):
    page = validated_data.pop('page')
    reply_to = validated_data.pop('reply_to')
    if page not in user.pages.all():
        return None, "That is not your own page"
    post = Post.objects.create(
        page=page, reply_to=reply_to, **validated_data
    )
    for follower in page.followers.all():
        tasks.notify_follower_about_new_post.delay(
            page.name, post.content, follower.email)

    return post, None


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
