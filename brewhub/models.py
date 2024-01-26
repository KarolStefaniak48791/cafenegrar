from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    customer_id = models.IntegerField()
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    date = models.DateField(auto_now_add=True)
    hour = models.TimeField(auto_now_add=True)

class Coffee(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255, default='path/to/default/image.jpg')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    table_ids = models.CharField(max_length=255, blank=True, null=True)
    number_of_hours = models.IntegerField()
    selected_date = models.DateField()
    reservation_cost = models.FloatField()