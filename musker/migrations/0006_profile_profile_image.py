# Generated by Django 4.2.7 on 2023-11-17 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musker', '0005_rename_cipher_ciphers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
