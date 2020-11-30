from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class Store(AbstractUser):
    location = models.CharField(max_length=128)
    logo = models.URLField()
    pass


class Listing(models.Model):
    store = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    image = models.URLField()
    content = models.TextField(max_length=512)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.DecimalField(max_digits=10, default=0)
    category = models.CharField(max_length=128)
    active = models.BooleanField(default=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

