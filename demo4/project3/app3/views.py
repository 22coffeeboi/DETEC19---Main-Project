import io
import sqlite3
import imageio as imageio
import keras
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from keras.saving.experimental.saving_lib import load_model
from numpy import save

from .models import Users,Predict
import matplotlib.pyplot as plt
from keras.layers import RandomFlip, RandomRotation
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.utils import img_to_array, np_utils, load_img
from keras.layers.convolutional import *
import numpy as np
from PIL import Image
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
#from .forms import PredictForm

import jinja2
import pdfkit
from datetime import datetime

import shutil




#change when code changes hands
label_dict = {0: 'Covid19 Negative', 1: 'Covid19 Positive'}
m, n = 120, 120

u = Users()

#change when code changes hands
model1 = keras.models.load_model('C:\\Users\\USR\\OneDrive\\Desktop')


# for table insertion
# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         blobData = file.read()
#     return blobData
#
# # for table insertion
# def insertBLOB(res, img, acc):
#     try:
#         sqliteConnection = sqlite3.connect('SQLite_Python.db')
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")
#         sqlite_insert_blob_query = """ INSERT INTO Predicts
#                                   (result, img, accuracy) VALUES (?, ?, ?, ?)"""
#
#         CTScan = convertToBinaryData(img)
#         #resume = convertToBinaryData(resumeFile)
#         # Convert data into tuple format
#         data_tuple = (res, CTScan, acc)
#         cursor.execute(sqlite_insert_blob_query, data_tuple)
#         sqliteConnection.commit()
#         print("Image and file inserted successfully as a BLOB into a table")
#         cursor.close()
#
#     except sqlite3.Error as error:
#         print("Failed to insert blob data into sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("the sqlite connection is closed")




# image uploading and prediction display
def uploadfun(request):
    nimrs = []
    label = 'Undefined'
    acc = 0
    current_user = request.user
    print(current_user)
    if request.method == 'POST':
        if 'pre' in request.POST:
            f = request.FILES['filename']
            response =  {}
            file_name = "h.png"
            file_name_2 = default_storage.save(file_name,f)

            # change when code changes hands
            file_url = 'C:\\Users\\USR\\PycharmProjects\\Ronv6\\demo4\\project3' + '\\' + default_storage.url(file_name_2)
            im = load_img(file_url, target_size=(m, n))
            im = im.convert(mode='RGB')
            imrs = im.resize((m, n))
            imrs = img_to_array(imrs) / 255
            imrs = imrs.transpose(2, 0, 1)
            imrs = imrs.reshape(m, n, 3)
            nimrs.append(imrs)
            nimrs = np.array(nimrs)

            predictions = model1.predict(nimrs)

            result = np.argmax(predictions, axis=1)[0]
            accuracy = float(np.max(predictions, axis=1)[0])

            label = label_dict[result]
            acc = round(accuracy*100)

            # print(predictions, result, accuracy)

            response['name'] = label
            response['name1'] = acc

            #insertBLOB(label, im, acc)
            #im = Image.open(file_url)
            #f = imageio.v2.imread(im)
            #b = io.BytesIO()
            # b = tobyte(nimrs)
            predict = Predict(result = label, img = file_url, accuracy = acc) #,img = im, accuracy = accuracy)
            #predict.img.save('hhh.png', ContentFile(Image.open(file_url)))
            # predict.img.save(b, "PNG")
            predict.save()

            today_date = datetime.today().strftime("%d %b, %Y")
            context = {'date': today_date, 'diag': label, 'prob': acc}

            template_loader = jinja2.FileSystemLoader(
                'C:\\Users\\USR\\PycharmProjects\\Ronv6\\demo4\\project3\\app3\\templates')
            template_env = jinja2.Environment(loader=template_loader)

            template = template_env.get_template('pdfreport.html')
            output_text = template.render(context)

            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration=config)


            # path = "C:\\Users\\USR\\PycharmProjects\\Ronv6\\demo4\\project3\\pdf_generated.pdf"
            # assert os.path.isfile(path)
            # with open(path, "r") as f:
            #     pass
            # original = 'C:\\Users\\USR\\PycharmProjects\\Ronv6\\demo4\\project3\\pdf_generated.pdf'
            # target = 'C:\\Users\\USR\\Downloads'
            # shutil.copyfile(original,target)

            return render(request, 'upload.html', response)

        # elif 'pdf' in request.POST:
        #
        #     # predict = Predict.objects.get(id=request.POST[''])
        #
        #     today_date = datetime.today().strftime("%d %b, %Y")
        #     context = {'date': today_date, 'diag': label, 'prob': acc}
        #
        #     template_loader = jinja2.FileSystemLoader('C:\\Users\\USR\\PycharmProjects\\Ronv6\\demo4\\project3\\app3\\templates')
        #     template_env = jinja2.Environment(loader=template_loader)
        #
        #     template = template_env.get_template('pdfreport.html')
        #     output_text = template.render(context)
        #
        #     config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        #     pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration=config)
        #
        #
        #     return render(request, 'upload.html')

    else:
        return render(request, 'upload.html')


def signupfun(request):
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('pass1') and request.POST.get(
                'pass2'):
            users = Users()
            users.username = request.POST.get('username')
            users.pass1 = request.POST.get('pass1')
            users.pass2 = request.POST.get('pass2')

        if Users.objects.filter(username= users.username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')

        if len(users.username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')

        if users.pass1 != users.pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')

        if not (users.username).isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')

        if users.username and users.pass1 and users.pass2 :
            users.save()
            messages.success(request,
                             "Your Account has been created succesfully!! ")
        return render(request, 'signin.html')
    else:
        return render(request, 'signup.html')


def signinfun(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        u = Users(username=username, pass1=pass1)

        users = Users.objects.get(username=username, pass1=pass1)
        if users:

            username = users.username
            pass1 = users.pass1
            request.session['username'] = username
            request.session['pass1'] = pass1
            return redirect('upload')

        else:
            messages.error(request, "Invalid Credentials!!")
            return redirect('signin')

    return render(request, 'signin.html')







def statusfun(request):

    title = "Predict"
    queryset = Predict.objects.all()

    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request,"pastpred.html",context)


# def predictfun(request):
#     form = None
#     if request.method == "POST":
#         form = PredictForm(request.POST,request.FILES)
#         print(form)
#         if form.is_valid():
#             form.save()
#
#             print('Form is not valid')
#             return HttpResponseRedirect('pastpred.html')
#     else:
#         form = PredictForm()
#     return render(request, 'history.html', {'form': form})


        



