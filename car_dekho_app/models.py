from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class ShowroomList(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website = models.URLField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
# Create your models here.
class CarList(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=False)
    chassisnumber = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    showroom = models.ForeignKey(ShowroomList, on_delete=models.CASCADE, name="showrooms", null= True)
    
    
    def __str__(self) -> str:
        return self.name
    
    
class Review(models.Model):
    api_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator, MinValueValidator])
    comments = models.CharField(max_length=255, null=True, blank=True)
    car = models.ForeignKey(CarList, on_delete=models.CASCADE, related_name="Reviews", null = True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return "the rating of the car " + self.car.name  + " is " + str(self.rating)
        