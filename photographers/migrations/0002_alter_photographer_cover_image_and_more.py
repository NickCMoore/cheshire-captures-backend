# Generated by Django 4.2.7 on 2024-10-14 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='cover_image',
            field=models.ImageField(
                default='cover_images/mountains',
                upload_to='cover_images/',
            ),
        ),
        migrations.AlterField(
            model_name='photographer',
            name='profile_image',
            field=models.ImageField(
                default='images/icecoast',
                upload_to='images/',
            ),
        ),
    ]
