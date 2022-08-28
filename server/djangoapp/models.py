from unicodedata import name
from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
            return f'CarMake: {self.name}'


class CarModel(models.Model):
    Sedan = "Sedan"
    SUV = "SUV"
    WAGON = "WAGON"

    TYPE_CHOICES = (
        (Sedan, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "WAGON")
    )
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    dealer_id = models.IntegerField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    year = models.DateField(auto_now=False, auto_now_add=False)
    def __str__(self):
            return f'CarModel name : {self.name}, {str(self.car_make)}, dealer_id: {self.dealer_id}, type: {self.type}, year: {str(self.year)}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer:

#     def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
#         self.address = address
#         self.city = city
#         self.full_name = full_name
#         self.id = id
#         self.lat = lat
#         self.long = long
#         self.short_name = short_name
#         self.st = st
#         self.zip = zip

#     def __str__(self):
#         return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
