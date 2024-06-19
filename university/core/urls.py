from django.urls import path
from .views import dashboard, add_student, delete_student, add_grade

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add_student/', add_student, name='add_student'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('add_grade/', add_grade, name='add_grade'),
]
