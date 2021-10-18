from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from  . import views
from django.urls import path
from django.views.generic import CreateView

app_name='accounts'

urlpatterns = [
    path('login/', views.Login.as_view(),name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    
    path('demo/', views.Demo.as_view(), name="demo"),
    path('profile_setting/', views.ProfileSetting.as_view(), name='profile_setting'),

    

]
