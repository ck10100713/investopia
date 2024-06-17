from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.investment, name='investment'),
    path('calculate/', views.calculate_and_show_results, name='calculate_view'),
    path('import-data/', views.import_data_view, name='import_data_view'),
    path('dollar-cost-averaging/', views.calculate_dollar_cost_averaging, name='dollar_cost_averaging_view'),
    path('stock-list/', views.stock_list, name='stock_list'),
    path('stock-detail/<str:ticker>/', views.stock_detail, name='stock_detail'),
    path('backtest/', views.backtest, name='backtest'),
    # path('backtest-result/', views.backtest_results, name='backtest_results'),
]