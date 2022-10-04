from django.db import models


class Tag(models.Model):
    """Tag model"""
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    """Page model"""
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('api.Tag', related_name='pages')

    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', related_name='follows')
    likes = models.ManyToManyField('users.User', related_name='likes')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        'users.User', related_name='requests')

    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Post model"""
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey(
        'api.Post', on_delete=models.SET_NULL, null=True, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
