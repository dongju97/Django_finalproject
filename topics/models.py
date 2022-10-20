from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.TextField() #아이디
    user_pwd = models.TextField() #비번
    name = models.CharField(max_length=20) #이름
    email = models.EmailField()
    profile = models.ImageField(blank=True, null=True, upload_to="") #글 입력시 이미지 
   
    
    