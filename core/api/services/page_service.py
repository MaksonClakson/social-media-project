import requests
import json

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import APIException, ParseError
from api import s3_service
import os
from dotenv import load_dotenv
load_dotenv()


from api.models import Tag, Page, Post
from core.producer import CommandTypes, CONTAINER_MESSAGES_IP

# reset_queries()
# print(connection.queries)


def page_list():
    return Page.objects.all()


def page_create(validated_data, current_user):
    tags_data = validated_data.pop('tags')
    validated_data.pop('owner')
    page = Page.objects.create(owner=current_user, **validated_data)
    page.tags.set(tags_data)
    response = requests.post(
        f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.CREATE_PAGE}', data=json.dumps({'page_id': page.pk, 'user_id': current_user.pk, 'page_name': page.title}))
    if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
            return "Error with statistic microservice", response.status_code
    return page


def page_update(instance, validated_data):
    instance.name = validated_data["name"]
    instance.uuid = validated_data["uuid"]
    instance.description = validated_data["description"]
    instance.is_private = validated_data["is_private"]
    instance.save(update_fields=['name', 'uuid', 'description', 'is_private'])
    return instance


def page_retrieve(id: int):
    s3_service.main()
    response = s3_service.list_buckets()
    print("1----------" + str(response))

    file_name = '/Users/abhinav.dumbre/hands-on-cloud/localstack-boto3/s3/files/hands-on-cloud.txt'
    object_name = 'hands-on-cloud.txt'
    bucket = os.getenv("AWS_BUCKET_NAME")
    response2 = s3_service.upload_file(file_name, bucket, object_name)
    print("2----------" + str(response2))
    return get_object_or_404(Page, pk=id)


def page_delete(instance):
    instance.delete()


def posts_of_page(page_pk):
    return Post.objects.filter(page__pk=page_pk)


def mypages_list_service(user):
    return Page.objects.filter(owner=user)


def follow_requests(page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    if not page.is_private:
        return {"message": "Your page is public"}, status.HTTP_400_BAD_REQUEST
    return page.follow_requests.all(), status.HTTP_200_OK


def subscribe(page_pk, user):
    page = get_object_or_404(Page, pk=page_pk)
    if user == page.owner:
        return "You can't subscribe to your page", status.HTTP_400_BAD_REQUEST
    if page.followers.filter(pk=user.pk).exists():
        return "You are already following this page", status.HTTP_400_BAD_REQUEST
    if page.is_private:
        if page.follow_requests.filter(pk=user.pk).exists():
            return "You have already sent follow request to this page", status.HTTP_400_BAD_REQUEST
        page.follow_requests.add(user)
        response, _status = requests.post(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.NEW_PAGE_FOLLOW_REQUEST}/', data=json.dumps({'page_id': page.pk}))
        if _status != status.HTTP_200_OK:
            return response, _status
        return "You have sent follow request to this page", status.HTTP_200_OK
    else:
        response = requests.post(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.NEW_PAGE_FOLLOWER}/', data=json.dumps({'page_id': page.pk}))
        if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
            return "Error with statistic microservice", response.status_code
        return "You have subscribed to this page", status.HTTP_200_OK


def unsubscribe(page_pk, user):
    page = get_object_or_404(Page, pk=page_pk)
    if user == page.owner:
        return "That's owner page!", status.HTTP_400_BAD_REQUEST
    if not page.followers.filter(pk=user.pk).exists():
        return "No such follower", status.HTTP_400_BAD_REQUEST
    if page.is_private:
        if not page.follow_requests.filter(pk=user.pk).exists():
            return "There's no follow request to undo", status.HTTP_400_BAD_REQUEST
        page.follow_requests.remove(user)
        response = requests.post(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.UNDO_FOLLOW_REQUEST}/', data=json.dumps({'page_id': page.pk}))
        if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
            return "Error with statistic microservice", response.status_code
        return "Undo sending follow request", status.HTTP_200_OK
    else:
        page.followers.remove(user)
        response = requests.post(
            f'http://{CONTAINER_MESSAGES_IP}/{CommandTypes.UNDO_PAGE_FOLLOWER}/', data=json.dumps({'page_id': page.pk}))
        if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
            return "Error with statistic microservice", response.status_code
        return "Unsubscribed", status.HTTP_200_OK


def follow_request_aciton(page_pk, data):
    user_pk = data['id']
    is_accept = data['is_accept']
    page = get_object_or_404(Page, pk=page_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if not page.follow_requests.all().exists():
        return "There is nothing to accept", status.HTTP_400_BAD_REQUEST
    if not page.follow_requests.filter(pk=user.pk).exists():
        return "User (pk:" + str(user_pk) + ") is not in follow requests", status.HTTP_400_BAD_REQUEST
    page.follow_requests.remove(user)
    if is_accept:
        page.followers.add(user)
    return "User (pk:" + str(user_pk) + ") was accepted", status.HTTP_200_OK


def all_follow_request_aciton(page_pk, data):
    page = get_object_or_404(Page, pk=page_pk)
    users = page.follow_requests.all()
    is_accept = data['is_accept']
    if not users.exists():
        return "There is nothing to accept", status.HTTP_400_BAD_REQUEST
    page.follow_requests.clear()
    if is_accept:
        page.followers.add(users)
    return "All follow requests was accepted", status.HTTP_200_OK


def add_tag(page_pk, data):
    page = get_object_or_404(Page, pk=page_pk)
    tag = Tag.objects.get(id=data['tag_id'])
    if tag in page.tags.all():
        return "Tag is already in the page", status.HTTP_400_BAD_REQUEST
    page.tags.add(tag)
    return "Tag added", status.HTTP_200_OK


def remove_tag(page_pk, data):
    page = get_object_or_404(Page, pk=page_pk)
    tag = Tag.objects.get(id=data['tag_id'])
    if tag not in page.tags.all():
        return "No such tag in the page", status.HTTP_400_BAD_REQUEST
    page.tags.remove(tag)
    return "Tag removed", status.HTTP_200_OK


def block(page, data):
    if 'unblock_date' in data:
        page.unblock_date = data['unblock_date']
        page.is_permanent_block = False
        page.save(update_fields=['is_permanent_block', 'unblock_date'])
        return "Unblock date setted", status.HTTP_200_OK
    if 'is_permanent' in data:
        page.is_permanent_block = data['is_permanent']
        page.unblock_date = None
        page.save(update_fields=['is_permanent_block', 'unblock_date'])
        return "Page blocked permanentrly", status.HTTP_200_OK


def unblock(page):
    page.unblock_date = None
    page.is_permanent_block = False
    page.save(update_fields=['unblock_date', 'is_permanent_block'])
    return "Page unblocked", status.HTTP_200_OK


def find_pages(_name, _uuid, _tag):
    if Tag.objects.filter(name=_tag).exists():
        tag = Tag.objects.filter(name=_tag)
        pages = Page.objects.filter(
            Q(name__contains=_name) & Q(uuid__contains=_uuid) & Q(tags__in=tag)
        )
    else:
        pages = Page.objects.filter(
            Q(name__contains=_name) & Q(uuid__contains=_uuid)
        )
    return pages


def get_stat(page):
    return
