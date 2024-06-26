from django.db import models
from users.models import CustomUser, CarDetails

class TripDetails(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tripposted')
    car = models.ForeignKey(CarDetails, on_delete=models.CASCADE, related_name='tripcar')
    startingpoint = models.CharField(max_length=50, null=False)
    endpoint = models.CharField(max_length=50, null=False)
    departuredate = models.DateField()
    departuretime = models.CharField(max_length=20)
    luggagesize = models.CharField(max_length=20, null=False)
    pets = models.CharField(max_length=5)
    emptyseats = models.IntegerField(default=1)
    kilometers = models.IntegerField(null=False)
    seatprice = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return f"Trip from {self.startingpoint} to {self.endpoint} by {self.driver.email}"
