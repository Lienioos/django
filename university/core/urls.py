from django.urls import path
from .views import dashboard, add_student

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add_student/', add_student, name='add_student'),
    
]
