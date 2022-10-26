import io
from PIL import Image as im
import torch
from .models import Diary

from django.shortcuts import redirect, render
from .models import Diary
# Create your views here.
def feed(request):
    if request.method=='POST':
        sel_cat = request.POST.get('shop')
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
        
        labels = results.pandas().xyxy[0]['name']
        
        for label in labels:
            if label == sel_cat:
                return render(request, 'feed.html')

        Diary.objects.filter().last().delete()
        context = {
            'com': comment,
        }
        return render(request, 'write.html', context)
    else:
        return render(request, 'feed.html')

def write(request):
    return render(request, 'write.html')