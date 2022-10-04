from django.contrib import admin

from api.models import Tag, Page, Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'description', 'owner',
                    'image', 'is_private', 'unblock_date',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('page', 'content', 'reply_to', 'created_at', 'updated_at')
