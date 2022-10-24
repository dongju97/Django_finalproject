from django.urls import path
from . import views

app_name='topics'

urlpatterns = [
    path('main/', views.main, name="main"),
    path('login/', views.login, name="login"),
    path('feed/', views.feed, name="feed"),
    path('point/', views.point, name="point"),
    path('write/', views.write, name="write"),
    path('check/', views.check, name="check"), 
    path('goal/', views.goal, name="goal"), 
    path('graph/', views.graph, name="graph"),
    path('save/', views.save, name="save"),

    
]
