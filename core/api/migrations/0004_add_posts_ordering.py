# Generated by Django 4.1.1 on 2022-10-17 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_add_is_permanent_block_to_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
