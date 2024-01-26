from django.contrib import admin
from .models import Coffee
from .models import Order
from .models import OrderItem
from .models import Reservation

admin.site.register(Coffee)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reservation)
