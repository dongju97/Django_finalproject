from logging import exception
from django.shortcuts import render, redirect
from . models import User

#페이지

def graph(request):
    save = [1,2,3]
    count =  [10,9,8]
    context = {
        'save' : save,
        'count' : count,
    }
    return render(request, "pages/graph.html",context)


def feed(request):
    return render(request, "pages/feed.html")


def point(request):
    return render(request, "pages/point.html")


def save(request):
    return render(request, "pages/save.html")


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