# Generated by Django 5.2 on 2025-04-29 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_reservation_room_id_reservation_room_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='room_id',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='room_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
