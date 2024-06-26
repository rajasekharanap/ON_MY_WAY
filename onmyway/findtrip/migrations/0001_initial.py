# Generated by Django 4.2.11 on 2024-05-07 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_alter_cardetails_usercar_alter_userfiles_userfile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookoing_date', models.DateField()),
                ('booking_time', models.TimeField()),
                ('no_seats', models.IntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_trips', to='users.cardetails')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_trips_as_driver', to=settings.AUTH_USER_MODEL)),
                ('passengers', models.ManyToManyField(related_name='booked_trips_as_passenger', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
