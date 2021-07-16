"""Vjezba7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from django.contrib.auth.views import LoginView
from vj7 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy_projection/<int:projection_id>/', views.buy_ticket, name='buy'),
    path('home/', views.home_view, name='home'), 
    
    
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('insert_projection/', views.inster_projection, name='insert_projection'),
    path('set_superuser/<str:person_id>', views.set_superuser, name='set_superuser'), 
    path('all_users/', views.all_users, name='users'),

    path('my_tickets/', views.user_tickets, name='user_tickets'), 
    path('projections_users/', views.projection_users, name='projection_users'),
    path('search_projection/', views.count_user_projection, name='search_projection'),    

    path('count_projections/<str:p_id>', views.counter_projection, name='count_projections'),
    path('projection_view/', views.projection_view, name='projection_view'), 

    path('obrana/<str:proj_id>', views.obrana_zadnje_vjezbe, name='obrana') ######
]
