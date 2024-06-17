from django.contrib import admin
from .models import StockData, StockDataAdmin
# Register your models here.
admin.site.register(StockData, StockDataAdmin)