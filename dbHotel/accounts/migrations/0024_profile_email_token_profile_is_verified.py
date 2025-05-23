# Generated by Django 5.2 on 2025-05-12 05:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0023_remove_profile_email_verification_token_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="email_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="profile",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
