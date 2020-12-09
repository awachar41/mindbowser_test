from django.urls import path

from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('save-employee/', views.save_employee, name='save_emp'),
    path('delete-employee/<emp_id>/', views.delete_emp, name='delete_emp'),
    path('update-employee/<emp_id>/', views.update_emp, name='update_emp'),
    path('update-employee-save/<emp_id>/', views.save_update_emp, name='update_emp_save'),

]
