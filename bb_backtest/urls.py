from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bb_backtest, name='bb_backtest'),
    # path('calculate_return/', views.calculate_return, name='calculate_return'),
]