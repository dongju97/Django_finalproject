from django.urls import path
from . import views

app_name='topics'

urlpatterns = [
    path('main/', views.main, name="main"),
    path('login/', views.login, name="login"),
    path('graph/', views.graph, name="graph"),
    path('feed/', views.feed, name="feed"),
    
]
