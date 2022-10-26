from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='topics'

urlpatterns = [
    #페이지
    path('graph/<int:pk>', views.graph, name="graph"),
    
    path('feed/', views.feed, name="feed"),
    path('point/<int:pk>', views.point, name="point"),
    path('save/<int:pk>', views.save, name="save"),
    path('write/', views.write, name="write"),
    path('popup/', views.popup, name="popup"),
    
    #로그인/회원가입
    path('main/<int:pk>', views.main, name="main"),
    path('', auth_views.LoginView.as_view(template_name='topics/login.html'), name='login'),
    path('logindo/', views.logindo, name="logindo"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    
    #포인트 적립
    path('getPoint/', views.getPoint, name="getPoint"),
]
