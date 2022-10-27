import io
from PIL import Image as im
import torch

from itertools import accumulate
from logging import exception
import json
from multiprocessing import context
from re import M, X
from django.shortcuts import render, redirect
from . models import User
from . models import UserSummary
from . models import PointHistory
from . models import Diary
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.dateformat import DateFormat

#페이지
#그래프 그리기
def graph(request,pk):
    user = UserSummary.objects.get(userid = pk)
    #적립가능한 물품 불러오기
    diary = Diary.objects.filter(userid = pk).exclude(acc_bool = True)
   
    #물품 개수
    tum = user.tumbler
    bag = user.bag
    con = user.container
    
    t=0
    c=0
    b=0
    for i in diary:       
        if i.cat_selected =="tumbler":
            t+=1
        elif i.cat_selected=="container":
            c+=1
        else:
            b+=1
         
    #한달동안 쓴 내역 불러오기
    d_list = Diary.objects.filter(userid=pk)
    
    #이번달 이용내역
    month = DateFormat(datetime.now()).format('Ym')
    m_c=0
    m_b=0
    m_t =0
    
    for d in d_list:
        mth = str(d.create_at.year)+str(d.create_at.month)
        
        if mth == month:
            if d.cat_selected =="tumbler":
                m_t+=1
            elif d.cat_selected =="container":
                m_c+=1
            else:
                m_b+=1

            
    context={
        'user':user,
        'count':[tum, bag, con],
        'save':[tum*50, bag*32, con*200], #물품 탄소량
        'point':[tum * 20, bag * 10, con * 30],#물품 포인트
        'c_cnt':[t*20,b*10,c*30],#적립가능한 물품 갯수
        'm_cnt':[m_t, m_b, m_c]
        }
    return render(request, "pages/graph.html",context)

def feed(request):
    if request.method=='POST':
        sel_cat = request.POST.get('shop')
        comment = request.POST.get('comment')
        image = request.FILES['image']
        userid = request.POST.get('pk')
        diary = Diary(userid=userid, comment = comment, image = image, cat_selected=sel_cat)
        diary.save()

        
        uploaded_img_qs = Diary.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = im.open(io.BytesIO(img_bytes))

        path_weightfile = "topics/model/best.pt"

        model = torch.hub.load('ultralytics/yolov5', 'custom',
                               path=path_weightfile)

        results = model(img, size=640)
        results.save(save_dir='media', exist_ok=True)
        
        labels = results.pandas().xyxy[0]['name']
        #UserSummary에 저장하기
        user = UserSummary.objects.get(userid=userid)
        
        for label in labels:
            if label == sel_cat:
                if sel_cat == 'tumbler':
                    user.tumbler+=1
                    sel_cat = '텀블러'
                    
                elif sel_cat == 'bag':
                    user.bag +=1
                    sel_cat = '장바구니'
                    
                elif sel_cat == 'container':
                    user.container +=1
                    sel_cat = '다회용기'
                    
                
                context = {
                    'com': comment,
                    'image': uploaded_img_qs.image.url,
                    'sel_cat': sel_cat,
                }
                
                
                user.save()
                return render(request, 'pages/feed.html', context)

        Diary.objects.filter().last().delete()
        
        return render(request, 'pages/write.html', context)
    else:
        return render(request, 'pages/feed.html')


def point(request,pk):
    user = UserSummary.objects.get(userid = pk)
    point = PointHistory.objects.filter(userid=pk)
    
    tumbler = user.tumbler * 20
    container = user.container *30
    bag = user.bag * 10
    acc = tumbler + container + bag
  
    context={
        'user':user,
        'point':point,
        'tumbler': tumbler,
        'container': container,
        'bag':bag,
        'acc':acc,
    }
    return render(request, "pages/point.html", context)


def save(request,pk):
    user = UserSummary.objects.get(userid = pk)
    diary = Diary.objects.filter(userid = pk)
    
    tumbler = user.tumbler * 50
    container = user.container * 200
    bag = user.bag * 32
    acc = tumbler + container + bag
    
    
    today = DateFormat(datetime.now()).format('Ymd')
    today_g = 0
    for dd in diary:
        day = str(dd.create_at.year) + str(dd.create_at.month) + str(dd.create_at.day)
        if day == today:
            if dd.cat_selected == "tumbler":
                today_g += 50
            elif dd.cat_selected == "bag":
                today_g += 32
            else:
                today_g +=200
        
    context={
        'user':user,
        'tumbler': tumbler,
        'container': container,
        'bag':bag,
        'acc':acc,
        'today_g':today_g,
        'diary':diary           
    }
    
    return render(request, "pages/save.html",context)

#다이어리
def write(request, pk):
    context={
        'pk': pk
    }
    return render(request, "pages/write.html", context)

def feed_detail(request, id):
    detail = Diary.objects.get(id=id)
    id = detail.userid
    context = {
        'detail': detail,
        'id':id
    }
    return render(request, 'pages/feed_detail.html', context)


def popup(request):
    return render(request, "pages/popup.html")



# 메인
def main(request, pk):
    one = User.objects.get(pk = pk)
    diary = Diary.objects.filter(userid = pk)
    
    try:
        point = UserSummary.objects.get(userid = pk)
    except UserSummary.DoesNotExist:
        point = UserSummary(userid = pk, accumulated_point =0, used_point=0, 
                            tumbler=0, bag=0, container=0)
        point.save()
        
    savePoint = point.tumbler*50 + point.bag*32 + point.container*200
    acc = point.accumulated_point
    #Diary 처리
    
    contents = Diary.objects.filter(userid=pk).order_by('-id')
    contents_all = Diary.objects.all().order_by('-id')
 
    #하루 달성 이미지
    day_cnt = 0
    today = DateFormat(datetime.now()).format('Ymd')
    for dd in diary:
        day = str(dd.create_at.year) + str(dd.create_at.month) + str(dd.create_at.day)
        if day == today:
            if dd.cat_selected == "tumbler":
                day_cnt+=1
            elif dd.cat_selected == "bag":
                day_cnt+=1
            else:
                day_cnt+=1
                
    context={
        'one':one,
        'point':point,
        'savePoint':savePoint,
        'contents': contents,
        'contents_all': contents_all,
        'acc':acc,
        'day_cnt':day_cnt
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
            a = 20
            b = "텀블러 사용 적립"
            point.tumbler +=1
            msg = "텀블러"
            
        elif kind == "bag":
            a = 10
            b = "장바구니 사용 적립"
            point.bag +=1
            msg = "장바구니"
            
        elif kind == "container":
            a = 30
            b = "다회용기 사용 적립"
            point.container +=1
            msg = "다회용기"
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