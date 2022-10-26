from itertools import accumulate
from logging import exception
import json
from multiprocessing import context
from re import X
from django.shortcuts import render, redirect
from . models import User
from . models import UserSummary
from . models import PointHistory
from . models import Diary
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#페이지

def graph(request,pk):
    user = UserSummary.objects.get(userid = pk)
    
    tum = user.tumbler
    bag = user.bag
    con = user.container
    
    context={
        'user':user,
        'count':[tum, bag, con],
        'save':[tum*50, bag*32, con*200]
    }
    return render(request, "pages/graph.html",context)

def feed(request):
    return render(request, "pages/feed.html")


def point(request,pk):
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

# 포인트 적립
@csrf_exempt
def getPoint(request):
    kind = request.POST.get('kind')
    pk = request.POST.get('pk')
    
    
    diary = Diary.objects.filter(userid = pk, cat_selected = kind).exclude(acc_bool = True)
    point = UserSummary.objects.get(userid= pk)
   
    
    #diary에서 false인 게시물 조회하기
    cnt = 0
    a = 0
    b =""
    msg="사용내역 없음"
    
    for i in diary:
        #Diary table
        cnt+=1   
        # print('------',list(i.values()))
        print('-------',i.acc_bool)
        #PointHistory
        if kind =="tumbler":
            a = 50
            b = "텀블러 사용 적립"
            point.tumbler +=1
            msg = "텀블러 등록 완료"
            
        elif kind == "bag":
            a = 32
            b = "장바구니 사용 적립"
            point.bag +=1
            msg = "장바구니 등록 완료"
            
        elif kind == "container":
            a = 200
            b = "다회용기 사용 적립"
            point.container +=1
            msg = "다회용기 등록 완료"
        else: 
            msg="등록실패"  
            
        #UserSummary:
        history = PointHistory(userid=pk, point=a, detail=b)
        history.save()
        point.accumulated_point += a
        point.used_point += a
        point.save()
        # print(i['acc_bool'])
        i.acc_bool = True
        i.save()

    
    context ={
        'msg':msg
    }
    return JsonResponse(context)