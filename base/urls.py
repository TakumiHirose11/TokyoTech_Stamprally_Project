from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from  . import views
from django.urls import path
from django.views.generic import CreateView

app_name='base'

urlpatterns = [
    path('',views.IndexView.as_view(), name="index"),
    path('home/', views.Home.as_view(), name='home'),
]
