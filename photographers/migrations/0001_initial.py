# Generated by Django 5.1.2 on 2024-10-14 05:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photographer',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('display_name', models.CharField(blank=True, max_length=255)),
                ('bio', models.TextField(blank=True)),
                ('follower_count', models.PositiveIntegerField(default=0)),
                ('total_likes', models.PositiveIntegerField(default=0)),
                (
                    'profile_image',
                    models.ImageField(
                        default='images/raceday.jpg',
                        upload_to='images/',
                    ),
                ),
                (
                    'cover_image',
                    models.ImageField(
                        default='cover_images/northumberlandcastle.jpg',
                        upload_to='cover_images/',
                    ),
                ),
                ('location', models.CharField(blank=True, max_length=255)),
                ('website', models.URLField(blank=True, max_length=255)),
                ('instagram', models.URLField(blank=True, max_length=255)),
                ('twitter', models.URLField(blank=True, max_length=255)),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'follower',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='following',
                        to='photographers.photographer',
                    ),
                ),
                (
                    'following',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='followers',
                        to='photographers.photographer',
                    ),
                ),
            ],
            options={
                'unique_together': {('follower', 'following')},
            },
        ),
    ]
