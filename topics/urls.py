from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='topics'

urlpatterns = [
    path('main/<int:pk>', views.main, name="main"),
    path('login/', auth_views.LoginView.as_view(template_name='topics/login.html'), name='login'),
    path('logindo/', views.logindo, name="logindo"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
]
