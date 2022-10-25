from django.urls import path
from . import views

app_name='detection'

urlpatterns = [
  path('feed/', views.feed, name="feed"),
  path('write/', views.write, name="write"),
]
