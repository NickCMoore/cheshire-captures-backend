# Generated by Django 4.2 on 2024-11-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0002_alter_photographer_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='cover_image',
            field=models.ImageField(
                default=(
                    'https://res.cloudinary.com/dwgtce0rh/image/upload/'
                    'v1727862662/vestrahorn-mountains-stokksnes-iceland_aoqbtp.jpg'
                ),
                upload_to='cover_images/',
            ),
        ),
        migrations.AlterField(
            model_name='photographer',
            name='profile_image',
            field=models.ImageField(
                default=(
                    'https://res.cloudinary.com/dwgtce0rh/image/upload/'
                    'v1727862662/vestrahorn-mountains-stokksnes-iceland_aoqbtp.jpg'
                ),
                upload_to='images/',
            ),
        ),
    ]