"""
URL configuration for hotel_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from hotel_management.views import home, set_language
from members.urls import *
from restaurant.views import *
from cleaning import urls

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('members.urls'), name='members'),
    path('administration/', include('administration.urls'), name='administration'),
    path('restaurant/', include('restaurant.urls'), name='restaurant'),
    path('cleaning/', include('cleaning.urls'), name='cleaning'),
    path('superuser/', include('super_user.urls'), name='superuser'),
    path('clients/', include('clients.urls'), name='clients'),
    path('accounting/', include('accounting.urls'), name='accounting'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

extra_urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
]

urlpatterns += extra_urlpatterns

