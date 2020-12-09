from django.urls import path

from . import views

app_name = 'managers'

urlpatterns = [

    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signup-save/', views.save_signup, name='signup_save'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.login_view, name='user_logout'),
]
