from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries

from api.models import Post

# reset_queries()
# print(connection.queries)


def post_list_service():
    return Post.objects.all()


def post_create_service(validated_data):
    page_data = validated_data.pop('page')
    reply_to_data = validated_data.pop('reply_to')
    post = Post.objects.create(
        page=page_data, reply_to=reply_to_data, **validated_data)
    return post


def post_update_service(instance, validated_data):
    instance.content = validated_data["content"]
    instance.save()
    return instance


def post_retrieve_service(id: int):
    return get_object_or_404(Post, pk=id)


def post_delete_service(instance):
    instance.delete()
