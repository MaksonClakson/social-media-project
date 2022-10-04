from django.shortcuts import get_object_or_404

from typing import List
from typing import Generator
from dataclasses import dataclass

from api.models import Tag


def tag_list_service():
    return Tag.objects.all()

def tag_create_service(validated_data):
    return Tag.objects.create(**validated_data)

def tag_retrieve_service(id : int):
    return get_object_or_404(Tag, pk=id)

def tag_update_service(instance, validated_data):
    instance.name = validated_data['name']
    instance.save()
    return instance

def tag_delete_service(instance):
    instance.delete()
