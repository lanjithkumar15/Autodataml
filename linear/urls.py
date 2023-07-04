from django.urls import path
from .views import variselect

app_name = 'linear' 

urlpatterns = [
    path('variselect/',variselect, name='variselect')
]