# Generated by Django 5.2 on 2025-04-13 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_rename_availability_room_available_remove_room_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='available',
            new_name='availability',
        ),
    ]
