from django.urls import path
from reg_auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('register/', auth_views.register, name='register')
]
