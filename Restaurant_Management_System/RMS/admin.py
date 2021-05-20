from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Food,Review,Foodtype,orders,Bill
# Register your models here.
admin.site.register(get_user_model())

# Register your models here.
admin.site.register(Food)

# Register your models here.
admin.site.register(Review)

# Register your models here.
admin.site.register(Bill)

# Register your models here.
admin.site.register(orders)