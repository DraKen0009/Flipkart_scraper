from django.urls import path

from .views import create_data

urlpatterns = [
    path('', create_data, name='create_data'),

]
