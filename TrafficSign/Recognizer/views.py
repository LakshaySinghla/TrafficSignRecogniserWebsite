from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadPictureForm

import cv2
from keras.models import load_model
import numpy as np
import os

def normailze_blur(img):
    img = cv2.normalize(img, img, 50,200 ,cv2.NORM_MINMAX)
    cv2.medianBlur(img, 3)                    ##here 30% noise is added to the original dataset and applied median blur on it
    return img

def upload_file(request):
    if request.method == 'POST' and request.FILES :
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['img'], form.cleaned_data['title'])
            return HttpResponseRedirect('/success/' + form.cleaned_data['title'])
    else:
        form = UploadPictureForm()
    return render(request, 'Recognizer/upload.html', {'form': form})

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def success(request,name):
    # img = open(name+'.png','rb')
    img = cv2.imread('Recognizer/temp/' + name+'.png' , cv2.IMREAD_UNCHANGED)
    os.remove('Recognizer/temp/' + name+'.png')
    img = cv2.resize(img,(32,32))
    img = normailze_blur(img)
    img = np.asarray(img)
    print("Shape",img.shape)
    img = img.reshape((1,32,32,3))
    model = load_model('Recognizer/TrafficSignModel.h5')
    y = np.argmax(model.predict(img))
    return HttpResponse("Successfully uploaded. Output class - " + str(y))

def handle_uploaded_file(f, name):
    with open('Recognizer/temp/' + name + '.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)