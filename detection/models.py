from django.db import models

# Create your models here.
class userSummary:
    userid = models.IntegerField() #user pk
    accumulated_point = models.IntegerField() #누적 포인트
    used_point = models.IntegerField() #사용 포인트
    
class Diary(models.Model):
    userid = models.IntegerField() #user pk
    create_at = models.DateTimeField(auto_now_add=True) #등록일자
    image = models.ImageField() #등록 이미지
    comment = models.TextField() #글쓰기 내용

class pointHistory:
    userid = models.IntegerField() #user pk
    point = models.IntegerField() #적립포인트
    detail = models.CharField(max_length=20) #포인트 사용/적립 내역
    create_at = models.DateTimeField(auto_now_add=True) #사용일자
    