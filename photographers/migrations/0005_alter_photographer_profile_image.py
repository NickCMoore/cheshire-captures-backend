# Generated by Django 5.1.1 on 2024-10-05 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0004_photographer_follower_count_photographer_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='profile_image',
            field=models.ImageField(default='path_to_default_image_here', upload_to='images/'),
        ),
    ]
