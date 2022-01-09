from PIL import Image , ImageTk
import numpy as np 
import tkinter as tk
import cv2 as cv 
import random as rm 
from tkinter import filedialog
from matplotlib import pyplot as plt
from queue import Queue as qu 
import math
window = tk.Tk()
window.title("Final B092040038") 
window.geometry('1000x1000')

def open():
    global right , left 
    file_path = filedialog.askopenfilename(title = 'Select file',filetypes =(('all files','.*'),('jpg files','.jpg'),('raw files','.raw'),('tiff files','.tiff')))
    left = cv.imread(file_path,cv.IMREAD_COLOR) #使用opencv讀取影像(array)
    #left = cv.resize(left,(300,300))            #使影像大小變為500x500
    left = left[:,:,::-1] 
    right = left.copy()                                                     #複製影像
    img = Image.fromarray(left)                  #array轉成image
    render = ImageTk.PhotoImage(image = img)     #轉換成tkinter可用的image
    lab = tk.Label(window, image = render)  #設一個label在windows上
    lab.image = render                           #在label位置上放影象
    lab.place(x = 175 ,y = 0)                   #調整image的位置
#儲存影像
def save():
    #儲存影像視窗的名稱影像類型
        window.filename = filedialog.asksaveasfilename(title = 'save file', filetypes = (('jpg files','.jpg'),('tif files','.tif')))
        cv.imwrite(window.filename,x)                      #輸出影像
def detect():
    global left,right 

    face_cascade = cv.CascadeClassifier('/home/timmy/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('/home/timmy/haarcascades/haarcascade_eye.xml')
    img = left
    img = np.ascontiguousarray( img , dtype=np.uint8)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=5,
        minSize=(32, 32))

    eyes= eye_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=3,
        minSize=(32, 32))
    for (x, y, w, h) in faces:
        cv.ellipse(img, (int(x + w/2) ,int( y + h/2 )), (int(w/2), int(h/2+10)), 0,0 ,360 ,(255, 255, 255),2)
        for (ex, ey, ew, eh) in eyes:
            cv.circle(img, (int(ex + ew/2) ,int( ey + eh/2 )), (int(ew/2)),(255, 255, 255),2)
            print(eyes)

    img1 = Image.fromarray(img)
    photo1 = ImageTk.PhotoImage(img1)
    lab1  = tk.Label(window,image = photo1,width = left.shape[0] ,height = left.shape[1])# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 800 ,y = 0)
    return (faces,eyes)

def snow():
    global right
    t = detect () 
    face = t[0] ; eye = t[1]
    for (x, y ,w ,h ) in face:
        getrm(2000, int((w+h)/4) , int(x+w/2) ,int(y+h/2))
        for (ex, ey, ew, eh) in eye:
            getrme(ew*eh**2,int((ew+eh)/4) , int(ey+ew/2) ,int(ex+eh/2))
    img = Image.fromarray(right)
    photo1 = ImageTk.PhotoImage(img)
    lab1  = tk.Label(window,image = photo1,width = right.shape[0],height = right.shape[1])# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 800 ,y = 0)

def getrm (num ,radius ,centerx,centery):
    global left 
    samplePoint = []
    for i in range(num):
        theta = rm.random() * 2 * np.pi
        r = rm.uniform(0,radius **2 )
        x = math.cos(theta) * (r ** 0.5) + centerx 
        y = math.sin(theta) * (r ** 0.5) + centery 
        samplePoint.append((int(x) , int(y)))
        right[int(x)][int(y)] = (255,255,255)
        #plt.plot(x,y,'*',color = 'blue')

    return samplePoint
    
def getrme (num ,radius ,centerx,centery):
    global left 
    samplePoint = []
    for i in range(num):
        theta = rm.random() * 2 * np.pi
        r = rm.uniform(0,radius **2 )
        x = math.cos(theta) * (r ** 0.5) + centerx 
        y = math.sin(theta) * (r ** 0.5) + centery 
        samplePoint.append((int(x) , int(y)))
        right[int(x)][int(y)] = left[int(x)][int(y)]
        #plt.plot(x,y,'*',color = 'blue')

    return samplePoint
    
def check():
    global right 
    for x in range(right.shape[0]):
        for y in range(right.shape[1]):
            if right[x][y][0] == 255 and right[x][y][1] == 255 and right[x][y][2]==255 :
                print(x,y,True )
    img = Image.fromarray(right)
    photo1 = ImageTk.PhotoImage(img)
    lab1  = tk.Label(window,image = photo1,width = left.shape[0] ,height = left.shape[1])# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 800 ,y = 0)

#執行open picture的button
btn1 = tk.Button(window,text='open picture',command=open)  #創造一個button
btn1.pack()                                                             #bottun顯示在window上
btn1.place(x=0,y=0)
                                                    #bottun的位置
#執行save picture的button
btn2 = tk.Button(window,text='save picture',command=save)
btn2.pack()
btn2.place(x=0,y=80)

#執行save picture的button
btn2 = tk.Button(window,text='face detection',command=detect)
btn2.pack()
btn2.place(x=0,y=160)


#執行save picture的button
btn2 = tk.Button(window,text='snow face',command=snow)
btn2.pack()
btn2.place(x=0,y=240)
window.mainloop() 
