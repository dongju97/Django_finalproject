from email.policy import default
from django.db import models

# Create your models here.
class User(models.Model):
    userid = models.TextField() #아이디
    userpwd = models.TextField() #비번
    name = models.CharField(max_length=20) #이름
    email = models.EmailField()
    profile = models.ImageField(blank=True, null=True, upload_to="") #글 입력시 이미지 
   
class UserSummary(models.Model):
    userid = models.IntegerField() #user pk
    accumulated_point = models.IntegerField() #누적 포인트
    used_point = models.IntegerField() #사용 포인트
    
    #물품
    tumbler = models.IntegerField(); #50g
    bag = models.IntegerField(); #32g
    container = models.IntegerField(); #200g
    
    
    
class Diary(models.Model):
    userid = models.IntegerField() #user pk
    cat_selected = models.CharField(max_length=15, null=False, default="no")
    create_at = models.DateTimeField(auto_now_add=True) #등록일자
    image = models.ImageField() #등록 이미지
    comment = models.TextField() #글쓰기 내용
    acc_bool = models.BooleanField(default=False)

class PointHistory(models.Model):
    userid = models.IntegerField() #user pk
    point = models.IntegerField() #적립포인트
    detail = models.CharField(max_length=20) #포인트 사용/적립 내역
    create_at = models.DateTimeField(auto_now_add=True) #사용일자