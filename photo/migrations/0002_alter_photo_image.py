# Generated by Django 4.2.7 on 2024-10-14 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(
                default='images/mountains', upload_to='images/'),
        ),
    ]
