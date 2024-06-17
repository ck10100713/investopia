from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ma_backtest, name='ma_backtest'),
    # path('calculate_return/', views.calculate_return, name='calculate_return'),
]