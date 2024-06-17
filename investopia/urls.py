"""
URL configuration for invest_adviser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from index import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('index/', views.homepage, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('member_center/', views.member_center, name='member_center'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('investment/', include('investment.urls')),
    path('avg_backtest/', include('avg_backtest.urls')),
    path('ma_backtest/', include('ma_backtest.urls')),
    path('bb_backtest/', include('bb_backtest.urls')),
]
