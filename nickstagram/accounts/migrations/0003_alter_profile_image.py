# Generated by Django 4.0.3 on 2022-04-10 12:57

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]
