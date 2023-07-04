from django.urls import path
from .views import upload_excel, visualize_data, select_variables

app_name = 'visual'

urlpatterns = [
    path('upload/', upload_excel, name='upload_excel'),
    path('select/', select_variables, name='select_variables'),
    path('visualize/', visualize_data, name='visualize_data'),
]
