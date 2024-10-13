# Generated by Django 5.1.1 on 2024-10-07 17:58

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('rating_count', models.PositiveIntegerField(default=0)),
                ('photographer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='photographers.photographer')),
                ('tags', models.ManyToManyField(blank=True, related_name='photos', to='photo.tag')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photographer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='photographers.photographer')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='photo.photo')),
            ],
            options={
                'unique_together': {('photographer', 'photo')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photographer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='photographers.photographer')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='photo.photo')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('photographer', 'photo', 'content')},
            },
        ),
    ]
