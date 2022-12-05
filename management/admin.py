from django.contrib import admin
from .models import Batch, Deaths, Expenses, Revenue, Customers,UserProfile
# Register your models here.



admin.site.register(Batch)
admin.site.register(Deaths)
admin.site.register(Expenses)
admin.site.register(Revenue)
admin.site.register(Customers)
admin.site.register(UserProfile)
