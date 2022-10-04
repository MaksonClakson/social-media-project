from rest_framework import serializers

from api.models import Tag
from api.services.tag_service import tag_create_service, tag_update_service


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'pages',)

    def create(self, validated_data):
        return tag_create_service(validated_data)

    def update(self, instance, validated_data):
        return tag_update_service(instance, validated_data)
