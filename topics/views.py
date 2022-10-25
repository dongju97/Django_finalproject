from itertools import accumulate
from logging import exception
import json
from multiprocessing import context
from django.shortcuts import render, redirect
from . models import User
from . models import UserSummary
from . models import PointHistory
from . models import Diary
from django.http import JsonResponse
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
    one = User.objects.get(pk = pk)
    try:
        point = UserSummary.objects.get(userid = pk)
    except UserSummary.DoesNotExist:
        point = UserSummary(userid = pk, accumulated_point =0, used_point=0, 
                            tumbler=0, bag=0, container=0)
        point.save()
    savePoint = point.tumbler*50 + point.bag*32 + point.container*200
    context={
        'one':one,
        'point':point,
        'savePoint':savePoint
    }
    return render(request, "topics/main.html", context)

#로그인
def login(request):
    return render(request, "topics/login.html")

def logindo(request):
    id = request.POST.get('id')
    pwd = request.POST.get('pwd')
    
    try :
        user = User.objects.get(userid = id)
        return redirect('topics:main',user.pk)
    except:
        print('회원정보 없음')
        redirect('topics:login')
    

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

#포인트 적립
def getPoint(request):
    msg = "적립이 완료되었습니다!"
    context ={
        'msg':msg
    }
    return JsonResponse(context)