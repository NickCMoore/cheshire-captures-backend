# Generated by Django 4.2.7 on 2024-12-14 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0019_alter_photographer_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='cover_image',
            field=models.ImageField(
                default='../gettyimages-10157832-612x612_mj1plv.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='photographer',
            name='profile_image',
            field=models.ImageField(
                default='../gettyimages-10157832-612x612_mj1plv.jpg', upload_to='images/'),
        ),
    ]
