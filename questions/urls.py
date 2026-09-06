from django.urls import path
from . import views

urlpatterns = [
    path('questions/create/', views.create_question, name='create_question'),
    path('questions/', views.manage_questions, name='manage_questions'),
    path('questions/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:pk>/delete/', views.delete_question, name='delete_question'),
]