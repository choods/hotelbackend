# Generated by Django 5.2 on 2025-05-12 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0030_remove_profile_email_verification_token_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="otp",
            name="user",
        ),
        migrations.AddField(
            model_name="profile",
            name="email_verification_sent_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="email_verification_token",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="otp_code",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="otp_expiry",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="EmailVerificationToken",
        ),
        migrations.DeleteModel(
            name="OTP",
        ),
    ]
