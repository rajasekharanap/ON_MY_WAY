# Generated by Django 4.2.11 on 2024-05-07 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findtrip', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingtrip',
            old_name='bookoing_date',
            new_name='booking_date',
        ),
    ]