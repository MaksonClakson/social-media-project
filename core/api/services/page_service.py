from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries

from rest_framework.exceptions import APIException, ParseError

from dataclasses import dataclass
from pydoc import describe
from typing import List

from api.models import Tag, Page

# reset_queries()
# print(connection.queries)


def page_list_service():
    return Page.objects.all()


def page_create_service(validated_data, current_user):
    tags_data = validated_data.pop('tags')
    page = Page.objects.create(owner=current_user, **validated_data)
    page.tags.set(tags_data)
    return page


def page_update_service(instance, validated_data):
    instance.name = validated_data["name"]
    instance.uuid = validated_data["uuid"]
    instance.description = validated_data["description"]
    instance.tags.set(validated_data["tags"])
    instance.is_private = validated_data["is_private"]
    instance.save()
    return instance


def page_retrieve_service(id: int):
    return get_object_or_404(Page, pk=id)


def page_delete_service(instance):
    instance.delete()
