# Generated by Django 5.1.2 on 2024-10-14 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='images/race.jpg', upload_to='images/'),
        ),
    ]
