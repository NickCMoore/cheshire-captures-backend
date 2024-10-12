# Generated by Django 5.1.2 on 2024-10-12 17:48

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0004_comment_is_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(
                default=45,  # Ensure a valid user ID exists
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to=settings.AUTH_USER_MODEL,  # Use AUTH_USER_MODEL to reference the user model dynamically
            ),
        ),
    ]