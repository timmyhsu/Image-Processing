import cv2
import math
import tkinter 
import numpy as np 
import matplotlib.pyplot as plt
from tkinter import*
from tkinter import filedialog
from PIL import ImageTk, Image

#create a window
window = tkinter.Tk() 
window.title('HW1')              
window.geometry('1000x1000')              

flag = True 

#open the picture
def ope():
        global load
        #開啟影像視窗的名稱影像類型
        file_path = filedialog.askopenfilename(title = 'Select file', filetypes = (('jpg files','.jpg'),('tif files','.tif')))
        load = cv2.imread(file_path)                 
        load = cv2.resize(load,(300,300))            #300x300
        img = Image.fromarray(load)                  #convert array into image
        cp = load.copy()                                                     #copy the image
        render = ImageTk.PhotoImage(image = img)     
        lab = tkinter.Label(window, image = render)  
        lab.image = render              
        lab.place(x = 300 ,y = 0)                   #place the image




#linearly變換
def linear():
        global cp,cp1,x
        width,height,rgb = load.shape                                            #讀取影像的width,height,rbg值
        cp = load.copy()                                     #複製原影像
        for y in range(height):
                for x in range(width):
                        for z in range(rgb):
                                color = load[x,y][z] * a.get() + b.get() #get滑桿的值，做線性變換
                                if color > 255:
                                    cp[x,y][z] = 255
                                elif color < 0:
                                        cp[x,y][z] = 0
        img1 = Image.fromarray(cp)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp.copy()
        x=np.array(img1)#convert img into array


#exponential conversion
def exponential():
        global cp,cp1,x
        width,height,rgb = load.shape
        cp = load.copy()
        for y in range(height):
                for x in range(width):
                        for z in range(rgb):
                                color = np.exp(load[x,y][z] * a.get() + b.get()) # exponential conversion
                                if color > 255:
                                    cp[x,y][z] = 255
                                elif color < 0:
                                        cp[x,y][z] = 0
        img1 = Image.fromarray(cp)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp.copy()
        x=np.array(img1)


#logarithmical conversion
def logarithmical():
        global cp,cp1,x
        width,height,rgb = load.shape
        cp = load.copy()
        for y in range(height):
                for x in range(width):
                        for z in range(rgb):
                                color = (load[x,y][z] * a.get() + b.get())/255 #log converison
                                color = math.log(color)*255
                                if color > 255:
                                    cp[x,y][z] = 255
                                elif color < 0:
                                        cp[x,y][z] = 0
        img1 = Image.fromarray(cp)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp.copy()
        x=np.array(img1)


#save the image
def save_picture():
        window.filename = filedialog.asksaveasfilename(title = 'save file', filetypes = (('jpg files','.jpg'),('tif files','.tif')))
        cv2.imwrite(window.filename,x)                      #output the image


#定義histogram
def histogram():
        global cp1,x
        gray = cv2.cvtColor(cp1,cv2.COLOR_BGR2GRAY)         
        hist,bins=np.histogram(gray,bins=256,range=[0,255]) 
        pdf = hist/cp1.size                             
        cdf = pdf.cumsum()                  
        newcolor = np.round(cdf*255)                    
        width,height,rgb = cp1.shape            
        for y in range(height): 
                for x in range(width):
                        for z in range(rgb):
                                cp1[x,y][z] = newcolor[cp1[x,y][z]]
        img1 = Image.fromarray(cp1)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp1.copy()
        x=np.array(img1)



#定義滑桿給a的值
def change_a(self):
        global value_a
        value_a = a.get()


#定義滑桿給b的值
def change_b(self):
        global value_b
        value_b = b.get()


#定義滑桿給z的變數值並使用biliner interpolation放大縮小影像
def zoom(var):
        global value_z,cp1,cp,flag,x
        if flag ==False:
                flag = True
                value_z = z.get()
                width1 = int(z.get()/50*300)
                height1 = int(z.get()/50*300)
                res = cv2.resize(cp1,(height1,width1),interpolation = cv2.INTER_LINEAR)
                img1 = Image.fromarray(res)
                photo1 = ImageTk.PhotoImage(image = img1)
                lab1  = tkinter.Label(window,image = photo1,width = 300,height = 300)
                lab1.image = photo1
                lab1.place(x = 600 ,y = 0)
                cp1 = cp1.copy()
                x =np.array(img1)
        else: flag = False


#定義滑桿給r的變數值並旋轉影像
def rotate(self):
        global cp1,x
        value_r = r.get()
        img1 = Image.fromarray(cp1)
        img1 = img1.rotate(r.get())
        photo1 = ImageTk.PhotoImage(image = img1)
        lab1  = tkinter.Label(window,image = photo1)
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0)
        cp1 = cp1.copy()
        x = np.array(img1)


#設置a變數滑桿
a=Scale(orient = HORIZONTAL,length = 300)   #滑桿調整成水平，長度300
a.config(from_= 0,to = 6)                                       #滑桿數字0到6
a.config(tickinterval = 1,resolution = 0.1) #滑桿顯示刻度為1,動一次0.1格
a.config(label = "變數a")                                       #滑桿的標籤
a.config(command = change_a)                            #滑桿的指令
a.pack()                                    #滑桿顯示
a.place(x = 200,y = 300)                                        #滑桿位置

#設置b變數滑桿
b=Scale(orient = HORIZONTAL,length = 300)
b.config(from_= 10,to = 100)
b.config(tickinterval = 10,resolution = 1)
b.config(label = "變數b")
b.config(command = change_b)
b.pack()
b.place(x = 400,y = 300)

#設置zoom變數滑桿
z=Scale(orient = HORIZONTAL,length = 200)
z.config(from_= 0,to = 100)
z.config(resolution =1 )
z.config(label = "zoom")
z.config(command = zoom)
z.set(50)                                    #滑桿起始位置
z.pack()
z.place(x = 200,y = 400) 

#設置rotate變數滑桿                
r=Scale(orient = HORIZONTAL,length = 200)
r.config(from_= 0,to = 360)
r.config(resolution =1 )
r.config(label = "rotate")
r.config(command = rotate)
r.pack()
r.place(x = 200,y = 500)  

#執行open picture的button
btn1 = tkinter.Button(window,text='open picture',command=ope)  #創造一個button
btn1.pack()                                                             #bottun顯示在window上 
btn1.place(x=0,y=0) 
                                                    #bottun的位置
#執行save picture的button
btn2 = tkinter.Button(window,text='save picture',command=save_picture)  
btn2.pack()                   
btn2.place(x=0,y=100) 

#執行線性變換的button
linearbtn = tkinter.Button(window,text = 'linear',command = linear,width = 11) 
linearbtn.place(y=430)

#執行exp變換的button
exponentialbtn = tkinter.Button(window,text = 'exponential',command = exponential,width = 11)
exponentialbtn.place(y=460)

#執行log變換的button
logarithmicalbtn = tkinter.Button(window,text = 'logarithmical',command = logarithmical,width = 11)
logarithmicalbtn.place(y=490)

#執行histogram的button
histogrambtn = tkinter.Button(window,text = 'histogram',command = histogram,width = 11)
histogrambtn.place(y=550)


#不斷執行視窗程式
window.mainloop()

                                                                                                                                                                                
┌──(timmy㉿timmyMBP)-[~/Image-Processing/1-hw]
└─$ vim hw1.py
                                                                                                                                                                                
┌──(timmy㉿timmyMBP)-[~/Image-Processing/1-hw]
└─$ python3 hw1.py     
  File "/home/timmy/Image-Processing/1-hw/hw1.py", line 1
    mport cv2
          ^
SyntaxError: invalid syntax
                                                                                                                                                                                
┌──(timmy㉿timmyMBP)-[~/Image-Processing/1-hw]
└─$ python3 hw1.py                                                                                                                                                          1 ⨯
Exception in Tkinter callback
Traceback (most recent call last):
  File "/usr/lib/python3.9/tkinter/__init__.py", line 1892, in __call__
    return self.func(*args)
  File "/home/timmy/Image-Processing/1-hw/hw1.py", line 150, in zoom
    res = cv2.resize(cp1,(height1,width1),interpolation = cv2.INTER_LINEAR)
NameError: name 'cp1' is not defined
                                                                                                                                                                                
┌──(timmy㉿timmyMBP)-[~/Image-Processing/1-hw]
└─$ cat hw1.py
import cv2
import math
import tkinter 
import numpy as np 
import matplotlib.pyplot as plt
from tkinter import*
from tkinter import filedialog
from PIL import ImageTk, Image

#create a window
window = tkinter.Tk() 
window.title('HW1')              
window.geometry('1000x1000')              

tag = True 

#open the picture
def ope():
        global load
        #開啟影像視窗的名稱影像類型
        file = filedialog.askopenfilename(title = 'Select file', filetypes = (('jpg files','.jpg'),('tif files','.tif')))
        load = cv2.imread(file)                 
        load = cv2.resize(load,(300,300))            #300x300
        img = Image.fromarray(load)                  #convert array into image
        cp = load.copy()                                                     #copy the image
        render = ImageTk.PhotoImage(image = img)     
        lab = tkinter.Label(window, image = render)  
        lab.image = render              
        lab.place(x = 300 ,y = 0)                   #place the image




#linearly變換
def linear():
        global cp,cp1,x
        width,height,rgb = load.shape                                            #讀取影像的width,height,rbg值
        cp = load.copy()                                     #複製原影像
        for y in range(height):
                for x in range(width):
                        for z in range(rgb):
                                color = load[x,y][z] * a.get() + b.get() #get滑桿的值，做線性變換
                                if color > 255:
                                    cp[x,y][z] = 255
                                elif color < 0:
                                        cp[x,y][z] = 0
        img1 = Image.fromarray(cp)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp.copy()
        x=np.array(img1)#convert img into array


#exponential conversion
def exponential():
        global cp,cp1,x
        width,height,rgb = load.shape
        cp = load.copy()
        for y in range(height):
                for x in range(width):
                        for z in range(rgb):
                                color = np.exp(load[x,y][z] * a.get() + b.get()) # exponential conversion
                                if color > 255:
                                    cp[x,y][z] = 255
                                elif color < 0:
                                        cp[x,y][z] = 0
        img1 = Image.fromarray(cp)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp.copy()
        x=np.array(img1)


#logarithmical conversion
def logarithmical():
        global cp,cp1,x
        width,height,rgb = load.shape
        cp = load.copy()
        for y in range(height):
                for x in range(width):
                        for z in range(rgb):
                                color = (load[x,y][z] * a.get() + b.get())/255 #log converison
                                color = math.log(color)*255
                                if color > 255:
                                    cp[x,y][z] = 255
                                elif color < 0:
                                        cp[x,y][z] = 0
        img1 = Image.fromarray(cp)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp.copy()
        x=np.array(img1)


#save the image
def save_picture():
        window.filename = filedialog.asksaveasfilename(title = 'save file', filetypes = (('jpg files','.jpg'),('tif files','.tif')))
        cv2.imwrite(window.filename,x)                      #output the image


#定義histogram
def histogram():
        global cp1,x
        gray = cv2.cvtColor(cp1,cv2.COLOR_BGR2GRAY)         
        hist,bins=np.histogram(gray,bins=256,range=[0,255]) 
        pdf = hist/cp1.size                             
        cdf = pdf.cumsum()                  
        newcolor = np.round(cdf*255)                    
        width,height,rgb = cp1.shape            
        for y in range(height): 
                for x in range(width):
                        for z in range(rgb):
                                cp1[x,y][z] = newcolor[cp1[x,y][z]]
        img1 = Image.fromarray(cp1)
        photo1 = ImageTk.PhotoImage(image=img1)
        lab1 = tkinter.Label(window, image = photo1) 
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0) 
        cp1=cp1.copy()
        x=np.array(img1)



#定義滑桿給a的值
def chtoa(self):
        global value_a
        value_a = a.get()


#定義滑桿給b的值
def chtob(self):
        global value_b
        value_b = b.get()


#定義滑桿給z的變數值並使用biliner interpolation放大縮小影像
def zoom(var):
        global value_z,cp1,cp,tag,x
        if tag ==False:
                tag = True
                value_z = z.get()
                width1 = int(z.get()/50*300)
                height1 = int(z.get()/50*300)
                res = cv2.resize(cp1,(height1,width1),interpolation = cv2.INTER_LINEAR)
                img1 = Image.fromarray(res)
                photo1 = ImageTk.PhotoImage(image = img1)
                lab1  = tkinter.Label(window,image = photo1,width = 300,height = 300)
                lab1.image = photo1
                lab1.place(x = 600 ,y = 0)
                cp1 = cp1.copy()
                x =np.array(img1)
        else: tag = False


#定義滑桿給r的變數值並旋轉影像
def rotate(self):
        global cp1,x
        value_r = r.get()
        img1 = Image.fromarray(cp1)
        img1 = img1.rotate(r.get())
        photo1 = ImageTk.PhotoImage(image = img1)
        lab1  = tkinter.Label(window,image = photo1)
        lab1.image = photo1
        lab1.place(x = 600 ,y = 0)
        cp1 = cp1.copy()
        x = np.array(img1)


#設置a變數滑桿
a=Scale(orient = HORIZONTAL,length = 300)   #滑桿調整成水平，長度300
a.config(from_= 0,to = 6)                                       #滑桿數字0到6
a.config(tickinterval = 1,resolution = 0.1) #滑桿顯示刻度為1,動一次0.1格
a.config(label = "變數a")                                       #滑桿的標籤
a.config(command = chtoa)                            #滑桿的指令
a.pack()                                    #滑桿顯示
a.place(x = 200,y = 300)                                        #滑桿位置

#設置b變數滑桿
b=Scale(orient = HORIZONTAL,length = 300)
b.config(from_= 10,to = 100)
b.config(tickinterval = 10,resolution = 1)
b.config(label = "變數b")
b.config(command = chtob)
b.pack()
b.place(x = 400,y = 300)

#設置zoom變數滑桿
z=Scale(orient = HORIZONTAL,length = 200)
z.config(from_= 0,to = 100)
z.config(resolution =1 )
z.config(label = "zoom")
z.config(command = zoom)
z.set(50)                                    #滑桿起始位置
z.pack()
z.place(x = 200,y = 400) 

#操作rotate的滑桿                
r=Scale(orient = HORIZONTAL,length = 200)
r.config(from_= 0,to = 360)
r.config(resolution =1 )
r.config(label = "rotate")
r.config(command = rotate)
r.pack()
r.place(x = 200,y = 500)  

#開檔案的按鈕
but1 = tkinter.Button(window,text='open picture',command=ope)  #創造一個按鈕
but1.pack() #bottun顯示在window上 
but1.place(x=0,y=0) #設定bottun的位置

#儲存檔案的按鈕
but2 = tkinter.Button(window,text='save picture',command=save_picture)  
but2.pack()                   
but2.place(x=0,y=100) 

#linear 的按鈕
linearbut = tkinter.Button(window,text = 'linear',command = linear,width = 11) 
linearbut.place(y=430)

#exp的按鈕
exponentialbut = tkinter.Button(window,text = 'exponential',command = exponential,width = 11)
exponentialbut.place(y=460)

#log變換的按鈕
logarithmicalbut = tkinter.Button(window,text = 'logarithmical',command = logarithmical,width = 11)
logarithmicalbut.place(y=490)

#histogram的按鈕
histogrambut = tkinter.Button(window,text = 'histogram',command = histogram,width = 11)
histogrambut.place(y=550)


#顯示在視窗上
window.mainloop()

