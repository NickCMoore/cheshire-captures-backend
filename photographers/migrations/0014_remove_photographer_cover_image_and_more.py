# Generated by Django 4.2.7 on 2024-12-13 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0013_alter_photographer_cover_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photographer',
            name='cover_image',
        ),
        migrations.AlterField(
            model_name='photographer',
            name='profile_image',
            field=models.ImageField(default='../coast', upload_to='images/'),
        ),
    ]
