from django.urls import path
from . import views

app_name='topics'

urlpatterns = [
    path('main/', views.main, name="main"),
    path('login/', views.login, name="login"),
    path('graph/', views.graph, name="graph"),
    path('feed/', views.feed, name="feed"),
    path('point/', views.point, name="point"),
    path('write/', views.write, name="write"),
    path('check/', views.check, name="check"), 
    path('goal/', views.goal, name="goal"), 
    path('graph_1/', views.graph_1, name="graph_1"), 
    
]
