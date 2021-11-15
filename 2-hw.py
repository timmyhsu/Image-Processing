from PIL import Image , ImageTk
import numpy as np 
import tkinter as tk
import cv2 as cv 
from tkinter import filedialog

#create a window
window = tk.Tk()
window.title("HW2 B092040038") 
window.geometry('1000x1000')

#開啟圖案
def open():
    global right , left 
    file_path = filedialog.askopenfilename(title = 'Select file',filetypes =(('tif files','.tif'),('jpg files','.jpg'),('raw files','.raw')))
    left = cv.imread(file_path,1)                 #使用opencv讀取影像(array)
    left = cv.resize(left,(300,300))            #使影像大小變為500x500
    img = Image.fromarray(left)                  #array轉成image
    right = left.copy()                                                     #複製影像
    render = ImageTk.PhotoImage(image = img)     #轉換成tkinter可用的image
    lab = tk.Label(window, image = render)  #設一個label在windows上
    lab.image = render                           #在label位置上放影象
    lab.place(x = 125 ,y = 0)                   #調整image的位置
#儲存影像
def save():
        #儲存影像視窗的名稱影像類型
        window.filename = filedialog.asksaveasfilename(title = 'save file', filetypes = (('jpg files','.jpg'),('tif files','.tif')))
        cv.imwrite(window.filename,x)                      #輸出影像

def average_mask():
    global right , left 
    width , height , color = right.shape ; width -= 2 ; height-=2 # take the width and height
    for y in range(0,height) :
        for x in range (0,width) :
            right[y][x] = np.mean(left [y:y+3 ,x:x+3])  #對每一個值在3x3 的mask 裏面，做平均值
    img = Image.fromarray(right) # from numpy array to img
    photo1 = ImageTk.PhotoImage(image = img) 
    lab1  = tk.Label(window,image = photo1,width = 300,height = 300) # display the image
    lab1.image = photo1
    lab1.place(x = 500 ,y = 0) # place the image to the correct place 

 #median masj
def median_mask():
    global right , left 
    width , height , color = right.shape ; width -= 2 ; height-=2 #提取寬高
    for y in range(0,height) :
        for x in range (0,width) :
            right[y][x] = np.median(left [y:y+3 ,x:x+3]) #對每一個值在3x3 的mask 裏面，做中位值
    #Display the Image
    img = Image.fromarray(right)
    photo1 = ImageTk.PhotoImage(image = img)
    lab1  = tk.Label(window,image = photo1,width = 300,height = 300)
    lab1.image = photo1
    lab1.place(x = 500 ,y = 400)

   #8 bit plane 
def bit_plane(self):
    global left , right 
    width ,height = left.shape[:2]
    bitplane = np.zeros((height,width,8),dtype = np.uint8) #create an 3 dimensinal array with height * width * 8 because wi devided into 8 bits 
    for bit in range(8) :
        temp = 2**bit
        bitplane[:,:,bit] = cv.bitwise_and(left,temp) # in each plane from  1-8 ,we do the operator 'and' to store every pixel's bit in each plane
    img = np.copy(bitplane[:,:,r.get()]) #then we copy the bitplane to img
    img = Image.fromarray(bitplane)
    photo1 = ImageTk.PhotoImage(image = img)
    lab1  = tk.Label(window,image = photo1,width = 300,height = 300)# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 500 ,y = 400)


    ##operating smoothing
def smooth(self):
    global left
    d=1+s.get()
    img = np.hstack([cv.GaussianBlur(left,(d,d),0)]) # 用套件寫出smooth 的感覺
    # Display the Image
    img = Image.fromarray(img)
    photo1 = ImageTk.PhotoImage(image = img)
    lab1  = tk.Label(window,image = photo1,width = 300,height = 300)# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 500 ,y = 400)

    ##operating sharpening
def sharp(self):
    global right
    d=p.get()+8
    filte = np.array([[-1,-1,-1],[-1,d,-1],[-1,-1,-1]])
    img = cv.filter2D(right,-1,filte)
     #Display the image
    img = Image.fromarray(img)
    photo1 = ImageTk.PhotoImage(image = img)
    lab1  = tk.Label(window,image = photo1,width = 300,height = 300)# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 500 ,y = 400)
    
def gray_slice_setz(): #gray slice 
    global left 
    height, width = left.shape[:2]
    #  Create an zeros array to store the sliced image
    temp = np.zeros((height,width),dtype = 'uint8') #創造 height * width 的np array
    #  Specify the min and max range from scale
    minimum = sn.get()
    maximum = sm.get()
    #  Loop over the input image and if pixel value lies in desired range set it to 255 otherwise set it to 0.
    for i in range(height):
        for j in range(width):
            if left[i,j][1]>minimum and left[i,j][1]<maximum: #若大於自己設定的直則255，反之0
                temp[i,j] = 255
            else:
                temp[i,j] = 0
    # Display the image
    img = Image.fromarray(temp)
    photo1 = ImageTk.PhotoImage(image = img)
    lab1  = tk.Label(window,image = photo1,width = 300,height = 300)# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 1000 ,y = 0)

def gray_slice_setp():
    global left 
    height, width = left.shape[:2]
    #  Create an zeros array to store the sliced image
    temp = np.zeros((height,width),dtype = 'uint8')
    #  Specify the min and max range
    minimum = sn.get()
    maximum = sm.get()
    #  Loop over the input image and if pixel value lies in desired range set it to 255 otherwise set it to 0.
    for i in range(height):
        for j in range(width):
            if left[i,j][1]>minimum and left[i,j][1]<maximum: 
                temp[i,j] = 255
            else:
                temp[i,j][1] = left[i,j][1]
    # Display the image
    img = Image.fromarray(temp)
    photo1 = ImageTk.PhotoImage(image = img)
    lab1  = tk.Label(window,image = photo1,width = 300,height = 300)# use a lable to display image
    lab1.image = photo1
    lab1.place(x = 1000 ,y = 0)
#====================== GUI Configuration =========================#

#執行open picture的button
btn1 = tk.Button(window,text='open picture',command=open)  #創造一個button
btn1.pack()                                                             #bottun顯示在window上 
btn1.place(x=0,y=0) 
                                                    #bottun的位置
#執行save picture的button
btn2 = tk.Button(window,text='save picture',command=save)  
btn2.pack()                   
btn2.place(x=0,y=80)

#button of average mask
btn1 = tk.Button(window,text='average mask',command=average_mask)  #創造一個button
btn1.pack()                                                             #bottun顯示在window上 
btn1.place(x=0,y=160)
#button of median mask
btn3 = tk.Button(window,text='median  mask',command=median_mask)  #創造一個button
btn3.pack()                                                             #bottun顯示在window上 
btn3.place(x=0,y=240)

#button of slicing set 0
btn4 = tk.Button(window,text='generate\n gray slice set 0',command=gray_slice_setz)  #創造一個button
btn4.pack()                                                             #bottun顯示在window上 
btn4.place(x=825,y=0)

#button of slicing set preserve
btn4 = tk.Button(window,text='generate\n gray slice set preserve',command=gray_slice_setp)  #創造一個button
btn4.pack()                                                             #bottun顯示在window上 
btn4.place(x=825,y=40)

# Scale of Bitplane
r=tk.Scale(length = 150)
r.config(from_= 0,to = 8)
r.config(resolution =1 )
r.config(label = "which bit")
r.config(command = bit_plane)
r.pack()
r.place(x = 0,y = 320)  

# Scale of Smoothing
s=tk.Scale(length = 150)
s.set(0)
s.config(from_= 0,to = 8)
s.config(resolution =1 )
s.config(label = "smooth")
s.config(command = smooth)
s.pack()
s.place(x = 200,y = 320)  

#Scale of Sharpening 
p=tk.Scale(length = 150)
p.set(0)
p.config(from_= 0,to = 40)
p.config(resolution =1 )
p.config(label = "sharp")
p.config(command = sharp)
p.pack()
p.place(x = 400,y = 320)  

#Scale of slicing max
sm=tk.Scale(length = 150)
sm.set(0)
sm.config(from_= 0,to = 100)
sm.config(resolution =1 )
sm.config(label = "max")
sm.pack()
sm.place(x = 0,y = 500)  

#Scale of slicing min
sn=tk.Scale(length = 150)
sn.set(0)
sn.config(from_= 0,to = 50)
sn.config(resolution =1 )
sn.config(label = "min")
sn.pack()
sn.place(x = 200,y = 500)  


window.mainloop()

