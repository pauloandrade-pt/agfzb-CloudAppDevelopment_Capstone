from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return "Name: " + self.name + ", " + \
                "Description: " + self.description



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('COUPE', 'Coupe'),
        ('VAN', 'Van'),
        ('FASTBACK', 'Fastback'),
        ('WAGON', 'WAGON')
    ]
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=CAR_TYPES)
    year = models.DateField(default=now)
    def __str__(self):
        return "Car Make: " + self.carMake.name + ", " + \
                "Dealer Id: " +  str(self.dealerId) + ", " + \
                "Name: " + self.name + ", " + \
                "Type: " + self.type + ", " + \
                "Year: " + self.year.strftime("%Y")

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
