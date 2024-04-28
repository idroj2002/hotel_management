from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from super_user.views import superuser_home, user_detail, clear_groups

app_name = 'superuser'

urlpatterns = [
    path('', superuser_home, name='superuser_home'),
    path('detail/<int:user_id>/', user_detail, name='user_detail'),
    path('clear/<int:user_id>/', clear_groups, name='clear_groups'),
]