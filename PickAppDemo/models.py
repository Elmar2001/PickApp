from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField('customer_status', default=False)
    is_store = models.BooleanField('store_status', default=False)


class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=128)
    logo = models.URLField()

    def __str__(self):
        return f"{self.user}"


class Listing(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    image = models.URLField()
    content = models.TextField(max_length=512)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    category = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_user")
    store = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_store")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=19, decimal_places=0, default=1)
    date = models.DateTimeField(auto_now_add=False)
    completed = models.BooleanField("completed", default=False)

    def __str__(self):
        return f"{self.user} purchased {self.quantity} {self.listing}"

