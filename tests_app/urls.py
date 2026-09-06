from django.urls import path
from . import views

urlpatterns = [
    # Admin
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tests/assign/', views.assign_test, name='assign_test'),
    path('tests/', views.manage_tests, name='manage_tests'),
    path('tests/<int:pk>/edit/', views.edit_test, name='edit_test'),
    path('tests/<int:pk>/delete/', views.delete_test, name='delete_test'),
    path('tests/<int:test_id>/report/', views.view_report, name='view_report'),
    path('tests/<int:test_id>/report/export/', views.export_report_excel, name='export_report_excel'),

    # Student
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/test/<int:assignment_id>/start/', views.start_test, name='start_test'),
    path('student/test/<int:assignment_id>/', views.take_test, name='take_test'),
    path('student/test/<int:assignment_id>/result/', views.test_result, name='test_result'),
]