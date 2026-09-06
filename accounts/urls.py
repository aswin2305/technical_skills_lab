from django.urls import path
from . import views

urlpatterns = [
    path('login/student/', views.login_student, name='login_student'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.TSLPasswordChangeView.as_view(), name='change_password'),
]