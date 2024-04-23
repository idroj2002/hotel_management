"""
URL configuration for base project.

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
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from cleaning.views import cleaning_home, create_cleaning_data, mark_as_completed, cancel_cleaning, mark_as_occupied

urlpatterns = [
    path('', cleaning_home, name='home'),
    path('create-data', create_cleaning_data, name='create-data'),
    path('mark-as-completed', mark_as_completed, name='mark-as-completed'),
    path('cancel-cleaning', cancel_cleaning, name='cancel-cleaning'),
    path('mark-as-occupied', mark_as_occupied, name='mark-as-occupied'),
]
