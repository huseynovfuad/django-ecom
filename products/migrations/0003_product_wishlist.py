# Generated by Django 3.2 on 2023-01-18 14:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
