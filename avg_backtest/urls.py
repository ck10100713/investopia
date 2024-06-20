from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.avg_backtest, name='avg_backtest'),
    path('avg_backtest_result/', views.avg_backtest_result, name='avg_backtest_result'),
    # path('calculate_return/', views.calculate_return, name='calculate_return'),
]