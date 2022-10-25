import io
from PIL import Image as im
import torch
from .models import Diary

from django.shortcuts import redirect, render
from .models import Diary
# Create your views here.
def feed(request):
    if request.method=='POST':
        comment = request.POST.get('comment')

        image = request.FILES['image']

        diary = Diary(userid=1, comment = comment, image = image)
        diary.save()

        uploaded_img_qs = Diary.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = im.open(io.BytesIO(img_bytes))

        path_weightfile = "detection/model/best.pt"

        model = torch.hub.load('ultralytics/yolov5', 'custom',
                               path=path_weightfile)

        results = model(img, size=640)
        results.save(save_dir='media', exist_ok=True)
        
        return render(request, 'feed.html')
    else:
        return render(request, 'feed.html')

def write(request):
    if request.method=='POST':
        comment = request.POST.get('comment')
        # #image = request.FILES['image']
        context = {
            'com': comment,
            #'image': image,
        }
        return render(request, 'write.html')
    else:
        return render(request, 'write.html')