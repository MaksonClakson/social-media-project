# Generated by Django 4.1.1 on 2022-10-17 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_move_likes_to_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_permanent_block',
            field=models.BooleanField(default=False),
        ),
    ]