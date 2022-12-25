# Generated by Django 3.2 on 2022-12-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20221223_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(choices=[('Extra Large', 'Extra Large'), ('Large', 'Large'), ('Medium', 'Medium'), ('Small', 'Small')], max_length=200)),
            ],
            options={
                'verbose_name': 'Size',
                'verbose_name_plural': 'Sizes',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='products.Size'),
        ),
    ]
