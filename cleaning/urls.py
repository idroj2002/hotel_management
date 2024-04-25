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
