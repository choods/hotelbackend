# Generated by Django 5.2 on 2025-05-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_rename_is_verified_profile_email_verified_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
