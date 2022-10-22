from logging import exception
from django.shortcuts import render, redirect
from . models import User

#페이지

def graph(request):
    london = [3.9,4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    tokyo =  [-3.2, 6.9, 9.5, 14.5, 30, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    context = {
        'london' : london,
        'tokyo' : tokyo,
    }
    return render(request, "pages/graph.html")


def feed(request):
    return render(request, "pages/feed.html")


def point(request):
    return render(request, "pages/point.html")


def write(request):
    return render(request, "pages/write.html")

def popup(request):
    return render(request, "pages/popup.html")

# Create your views here.
def main(request, pk):
    one = User.objects.get(pk=pk)
    context={
        'one':one
    }
    return render(request, "topics/main.html", context)

def login(request):
    return render(request, "topics/login.html")

def logindo(request):
    id = request.POST.get('id')
    pwd = request.POST.get('pwd')
    
    user = User.objects.get(userid = id)
    
    return redirect('topics:main', user.pk)

def signin(request):
    return render(request, "topics/signin.html")

#회원가입
def signup(request):
    name = request.POST.get('name')
    userid= request.POST.get('userid')
    userpwd= request.POST.get('userpwd')
    email= request.POST.get('email')
    
    user = User(name=name,userid=userid, userpwd=userpwd,email=email)
    
    user.save()
    
    
    return redirect('topics:main',user.pk)