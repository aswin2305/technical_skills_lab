from django.urls import path
from . import views

urlpatterns = [
    path('candidates/create/', views.create_candidate, name='create_candidate'),
    path('candidates/', views.manage_candidates, name='manage_candidates'),
    path('candidates/<int:pk>/edit/', views.edit_candidate, name='edit_candidate'),
    path('candidates/<int:pk>/delete/', views.delete_candidate, name='delete_candidate'),
    path('candidates/<int:pk>/reset-password/', views.reset_password, name='reset_password'),

    path('candidate-groups/create/', views.create_group, name='create_group'),
    path('candidate-groups/', views.manage_groups, name='manage_groups'),
    path('candidate-groups/<int:pk>/edit/', views.edit_group, name='edit_group'),
    path('candidate-groups/<int:pk>/delete/', views.delete_group, name='delete_group'),
]