from django.db import models
from django.utils import timezone

# Create your models here


class Apartment(models.Model):
    address = models.CharField(max_length=200)
    unit_number = models.IntegerField('Unit Number')
    rent = models.IntegerField(default=0)
    date_built = models.DateTimeField(
        "date built")

class Lease(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lease_expires = models.DateTimeField(
        "lease expires")
