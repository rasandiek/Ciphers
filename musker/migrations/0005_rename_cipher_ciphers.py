# Generated by Django 4.2.6 on 2023-11-05 06:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musker', '0004_rename_create_at_cipher_created_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cipher',
            new_name='Ciphers',
        ),
    ]
