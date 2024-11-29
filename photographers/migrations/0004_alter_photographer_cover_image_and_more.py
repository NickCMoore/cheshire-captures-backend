# Generated by Django 4.2 on 2024-11-29 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0003_alter_photographer_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='cover_image',
            field=models.ImageField(default='cover_images/mountains', upload_to='cover_images/'),
        ),
        migrations.AlterField(
            model_name='photographer',
            name='profile_image',
            field=models.ImageField(default='images/icecoast', upload_to='images/'),
        ),
    ]
