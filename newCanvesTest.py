from win32api import GetSystemMetrics
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import numpy as np
import subprocess
# import windnd
import os
import time
import http.client
import json

import re
import socket
import threading

# from onlinevideo import *

st = subprocess.STARTUPINFO
st.dwFlags = subprocess.STARTF_USESHOWWINDOW
st.wShowWindow = subprocess.SW_HIDE

import cv2
import tkinter as tk  # imports

import pythoncom

import pyHook
import win32clipboard
import win32con

from pymouse import PyMouse, PyMouseEvent

import tensorflow as tf



class Contour(object):

    def __init__(self):
        print('Contour init')
    #得到点击区域
    def getClickRect(self,x,y,img):
        print('getClickRect')
        self.width=img.shape[1]
        self.height=img.shape[0]
        self.x=x
        self.y=y
        self.img=img
        ox1 = x - 100;
        oy1 = y - 100;
        ox2 = x + 100;
        oy2 = y + 100;
        if ox1 < 0 :
            ox1 = 0
        if oy1 < 0:
            oy1 = 0
        if ox2 > self.width:
            ox2 =self.width
        if oy2 > self.height:
            oy2 = self.height
        self.rect=[ox1,oy1,ox2-ox1,oy2-oy1]
        print(self.rect)
        # 665, 477, 710, 505
        img=img[self.rect[1]:self.rect[3]+self.rect[1],self.rect[0]:self.rect[2]+self.rect[0]]

        lightness=self.Lightness_mean_value(img)
        kernel = cv2.getStructuringElement( cv2.MORPH_RECT, (3,3))
        if lightness>127:
            img = cv2.erode(img, kernel)
            # img = cv2.erode(img, kernel)
            # img = cv2.dilate(img, kernel)
        else:
            img = cv2.dilate(img, kernel)
            # img = cv2.dilate(img, kernel)
            # img = cv2.erode(img, kernel)
        # img=cv2.cvtColor(img,cv2.COLOR_RGB2HLS)
        # self.rect = self.findOptimalRect(img,ox1,ox2)
        img=cv2.split(img)
        # cv2.imshow("0",img[0])
        # cv2.imshow("1", img[1])
        # cv2.imshow("2", img[2])
        img=cv2.adaptiveThreshold(img[0],255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,101,0)
        print('cv2.findContours')
        tuple_allValue = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # countours, hierarchy
        print('===========len:',len(tuple_allValue))
        if len(tuple_allValue)==2:
            countours, hierarchy=tuple_allValue
        else:
            binary,countours, hierarchy = tuple_allValue

        mindis=9999
        index=0
        for i in range(0, len(countours)):
            x, y, w, h = cv2.boundingRect(countours[i])
            x=x+ox1
            y=y+oy1
            dis=self.XYtoXYDistance(self.x,self.y,int(x+w/2),int(y+h/2))
            if dis<mindis and w*h>100:
                mindis=dis
                index=i
            # cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 1)

        x, y, w, h = cv2.boundingRect(countours[index])
        x=x+ox1
        y=y+oy1
        self.rect=[x,y,w,h]
        return self.rect

        # cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        #
        # cv2.imshow("1",self.img)
        # cv2.waitKey(0)

    def findOptimalRect(self,img,ox1,oy1):
        sourceImg=img
        img = cv2.split(img)

        mindis = 9999
        rect=[0,0,0,0]
        for j in range(2):
            img = cv2.adaptiveThreshold(img[j], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 0)
            img2, countours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for i in range(0, len(countours)):
                x, y, w, h = cv2.boundingRect(countours[i])
                x = x + ox1
                y = y + oy1
                dis = self.XYtoXYDistance(self.x, self.y, int(x + w / 2), int(y + h / 2))
                if dis < mindis and w * h > 100:
                    mindis = dis
                    rect = [x,y, w, h]
        print('findOptimalRect rect=',rect)
        return rect


    def getImage(self):

        img=self.img[self.rect[1]:self.rect[3]+self.rect[1],self.rect[0]:self.rect[2]+self.rect[0]]

        return img



    def XYtoXYDistance(self,x_1,y_1,x_2,y_2):
        # print("XYtoXYDistance")
        distance = int(np.sqrt(((x_1 - x_2) * (x_1 - x_2)) + ((y_1 - y_2) * (y_1 - y_2))))
        return distance

    def Lightness_mean_value(self,img):
        #求 图像的平均亮度
        print("Lightness_mean_value,",img.shape)
        w=img.shape[1]
        h=img.shape[0]

        img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        img =cv2.split(img)
        # num=np.sum(img[0])
        print("num=",np.sum(img[0])/(w*h))
        num=np.sum(img[1])
        print("num=",num/(w*h))
        # num=np.sum(img[2])
        print("num=",np.sum(img[2])/(w*h))
        return num/(w*h)



class canves(object):

    def __init__(self, mTk, mTtk):
        print("open")
        self.tk = mTk
        self.ttk = mTtk
        self.mWindow1 = self.tk.Toplevel()
        self.mWindow1.title("canvas")
        self.mWindow1.geometry(str(GetSystemMetrics(0)) + 'x' + str(GetSystemMetrics(1)) + '+0+0')
        self.frame = None
        self.mImgPath = None
        self.mImg = None
        self.mImg1 = None
        self.mImgContour=None
        self.mImgContourSave=None
        self.currentImage = None
        self.click = None
        self.hbar = None
        self.frameMouse = None
        self.saveArray = []
        self.cutPic_x1 = None
        self.cutPic_y1 = None
        self.cutPic_x2 = None
        self.cutPic_y2 = None
        self.selectRegion_start = True
        self.videoOn_Off = False
        self.Obj = None
        self.cut_img = None
        self.cut_canvas = None
        self.current_cut_range = [None, None, None, None]  # 当前已选中的裁剪范围
        self.adjustmentCutRegion_start = True
        self.currentBGR=None
        '''
        self.mWindowMouse=self.tk.Toplevel()
        
        self.mWindowMouse.geometry(str(250) + 'x' + str(250) + '+' + str(10) + '+' + str(10))
        # self.mWindowMouse.protocol('WM_DELETE_WINDOW',self.prohibit)
        self.mWindowMouse.attributes('-toolwindow', True)
        # self.mWindowMouse.attributes("-alpha", 0.9)#窗口透明度60 %
        self.mWindowMouse.resizable(0, 0)
        '''
        self.mRGB = None
        self.FM = True
        self.canvas_FM = None
        self.draw_canvas = None
        self.ImgList = []
        self.ImgList_index = -1
        '''
        self.canvas_FM = self.tk.Canvas(self.mWindowMouse, bg='grey', height=200, width=200)
        self.canvas_FM.config(width=200, height=200)
        # self.canvas_FM.pack(side=self.tk.LEFT, expand=True, fill=self.tk.BOTH)
        self.canvas_FM.place(x=0,y=0)

        
        self.X=self.tk.StringVar()
        self.Y=self.tk.StringVar()
        self.label1=self.tk.Label(self.mWindowMouse, text="X:", width=1, height=1).place(x=5,y=210)
        self.label2 = self.tk.Label(self.mWindowMouse, text="Y:", width=1, height=1).place(x=80, y=210)
        self.label3 = self.tk.Label(self.mWindowMouse, textvariable=self.X, width=4, height=1).place(x=25, y=210)
        self.label4 = self.tk.Label(self.mWindowMouse, textvariable=self.Y, width=4, height=1).place(x=100, y=210)
        '''
        self.selectRegion_Press_x1 = None
        self.selectRegion_Press_y1 = None
        self.draw_Window = None
        self.TextDetection=None
        # = ttk.Notebook(mWindow)

        # side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.

    def toValue(self):
        print("toValue")
        min = self.entry_to_Value_min.get()
        max = self.entry_to_Value_max.get()
        print('min=', min, ',max=', max)
        min1 = int(min.split(',')[0])
        min2 = int(min.split(',')[1])
        min3 = int(min.split(',')[2])
        max1 = int(max.split(',')[0])
        max2 = int(max.split(',')[1])
        max3 = int(max.split(',')[2])
        lower_red = np.array([min1, min2, min3])
        upper_red = np.array([max1, max2, max3])
        # lower_red = np.array([200, 200, 200])
        # upper_red = np.array([255, 255, 255])
        mat = self.currentImage.convert("RGB")
        mat = np.array(mat)
        print(mat.shape)
        mat = cv2.inRange(mat, lower_red, upper_red)
        img = Image.fromarray(mat).convert('RGB')
        self.currentImage = img
        self.mImg = ImageTk.PhotoImage(self.currentImage)
        self.canvas.create_image(0, 0, anchor="nw", image=self.mImg)
        # self.currentImage=img

    def toValue_vague(self):
        print("toValue_vague")
        print(self.toValue_threshold_entry.get(), ',', self.toValue_set_entry.get(), ',',
              self.combobox_to_Value_mode.get())
        # self.combobox_to_Value_mode['values'] = ['THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO','THRESH_TOZERO_INV']
        image = self.currentImage.convert('RGB')
        image = np.array(image)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        mode = None
        if self.combobox_to_Value_mode.get() == 'THRESH_BINARY':
            mode = cv2.THRESH_BINARY
        elif self.combobox_to_Value_mode.get() == 'THRESH_BINARY_INV':
            mode = cv2.THRESH_BINARY_INV
        elif self.combobox_to_Value_mode.get() == 'THRESH_TRUNC':
            mode = cv2.THRESH_TRUNC
        elif self.combobox_to_Value_mode.get() == 'THRESH_TOZERO':
            mode = cv2.THRESH_TOZERO
        elif self.combobox_to_Value_mode.get() == 'THRESH_TOZERO_INV':
            mode = cv2.THRESH_TOZERO_INV
        ret, thresh = cv2.threshold(gray, int(self.toValue_threshold_entry.get()), int(self.toValue_set_entry.get()),mode)

        img = Image.fromarray(thresh)
        self.currentImage = img
        self.ImgList.append(img)
        self.ImgList_index=self.ImgList_index+1
        print('self.ImgList_index=', self.ImgList_index)
        self.update_mImg()


    def followMouse(self, mouse_x, mouse_y):
        print("followMouse")
        self.FM = False
        # self.mWindowMouse.title(str(self.mRGB))
        # self.mWindowMouse.geometry(str(250) + 'x' + str(250) + '+' + str(mouse_x) + '+' + str(mouse_y))
        # self.mWindowMouse.deiconify()
        print("self.mImg1=", self.mImg1)

        self.mImg1 = ImageTk.PhotoImage(self.mImg1)
        print("self.mImg1=", self.mImg1)
        self.canvas_FM.create_image(0, 0, anchor="nw", image=self.mImg1)
        self.canvasEnlarge.create_image(0, 0, anchor="nw", image=self.mImg1)
        self.FM = True

    def EnlargeImg(self, event):
        print('EnlargeImg')

        self.mImg1 = ImageGrab.grab((event.x_root - 10, event.y_root - 10, event.x_root + 10, event.y_root + 10))
        multiple = 10
        size = (self.mImg1.size[0] * multiple, self.mImg1.size[1] * multiple)
        self.mImg1 = self.mImg1.resize(size).convert('RGB')
        # self.mImg1.show("1111")
        if event.y_root > 500:
            display_x = event.x_root
            display_y = event.y_root - 300
        elif event.y_root <= 500:
            display_x = event.x_root
            display_y = event.y_root + 100
        draw = ImageDraw.Draw(self.mImg1)
        draw.rectangle((100, 100, 110, 110), fill=None, outline='red')
        self.mImg1 = ImageTk.PhotoImage(self.mImg1)
        self.canvasEnlarge.create_image(0, 0, anchor="nw", image=self.mImg1)
        # print(event.x,',',event.y)
        x = event.x - 2
        # y=event.y-2
        y = int(event.y - 2 + (1280 * self.vbar.get()[0]))
        print(x, ',', y)
        self.label_X.config(text='X:' + str(x))
        self.label_Y.config(text='Y:' + str(y))
        mat1 = np.array(self.currentImage)
        mRGB = mat1[y][x]
        print(mRGB)
        print(mRGB[0])
        # self.lable_RGB_entry_text.set(str(mRGB))
        rgbstr=str(mRGB[0]) + ',' + str(mRGB[1]) + ',' + str(mRGB[2])
        self.currentBGR=rgbstr
        self.label_RGB_.config(text='RGB:' + rgbstr)

    def cut_canvas_event(self, event, w, h):
        print(event, ',', w, ',', h)
        print('cut_canvas_event', event.x, event.y, )
        x = event.x
        y = event.y
        # print(w/2)
        # left_w=int(w/3)

        # print(self.judgeRange(x,y,(0,h/3,w/3,2*h/3)))
        if self.judgeRange(x, y, (0, h / 3, w / 3, 2 * h / 3)):
            print('left')
            self.cut_canvas.config(cursor='sb_left_arrow')
        elif self.judgeRange(x, y, (w / 3 * 2, h / 3, w, 2 * h / 3)):
            print('right')
            self.cut_canvas.config(cursor='sb_right_arrow')
        elif self.judgeRange(x, y, (w / 3, 0, w / 3 * 2, h / 3)):
            print('up')
            self.cut_canvas.config(cursor='sb_up_arrow')
        elif self.judgeRange(x, y, (w / 3, h / 3 * 2, w / 3 * 2, h)):
            print('down')
            self.cut_canvas.config(cursor='sb_down_arrow')
        else:
            self.cut_canvas.config(cursor='arrow')

    # 判断 x,y 是否在 range范围内
    def judgeRange(self, x, y, range):

        # print('judgeRange--- range=', range, ',x=', x, ',y=', y)

        if x >= int(range[0]) and x <= int(range[2]) and y >= int(range[1]) and y <= int(range[3]):
            # print('return true')
            return True
        else:
            return False

    def handler_adaptor(self, fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def prohibit(self):
        print("prohibit")

    def onMouseMove(self, event):
        print("move", self.mWindow1.winfo_x(), self.mWindow1.winfo_y())

        if self.selectRegion_Press_x1 != None and self.selectRegion_Press_y1 != None:
            self.mWindowMouse.iconify()
            return

        self.mWindow1.update()
        print("fram=", self.frame.winfo_y())
        print("现在的位置是", event.x_root, event.y_root)
        print(self.click)
        if self.click == 37:
            PyMouse.move(None, event.x_root + 1, event.y_root)
        elif self.click == 38:
            PyMouse.move(None, event.x_root + 1, event.y_root)
        elif self.click == 38:
            PyMouse.move(None, event.x_root + 1, event.y_root)
        elif self.click == 38:
            PyMouse.move(None, event.x_root + 1, event.y_root)
        print("现在的位置是", event.x_root, event.y_root)
        xo = self.mWindow1.winfo_x() + 8 + 2
        yo = self.mWindow1.winfo_y() + 8 + 24
        print(xo, ",", yo)
        print(event.x_root - xo, ",", event.y_root - yo)
        print(" bar=", self.vbar.winfo_rooty(), ",", self.hbar.winfo_rooty(), ",", self.vbar.winfo_rootx(), ",",
              self.hbar.winfo_rootx())

        row = event.x_root - xo
        col = event.y_root - yo
        print("row=", row, ",col=", col)
        print("x=", event.x, ",y=", event.y)

        row = event.x - 2
        col = event.y - 2

        if self.currentImage == None:
            return
        # mat1=cv2.imread(self.mImgPath)
        print("self.currentImage=", type(self.currentImage))
        mat1 = np.array(self.currentImage)
        col_ox = int(col + (1280 * self.vbar.get()[0]))
        # print(mat1[col_ox][row][::-1])
        # print(mat1[col_ox][row])
        # a=mat1[col_ox][row]
        # print(a[::-1])
        # a = a[::-1]
        # self.mRGB=sorted(mat1[col_ox][row],reverse=True)
        self.mRGB = mat1[col_ox][row]

        # self.mWindowMouse.iconify()
        '''
        self.mRGB=str(self.mRGB).replace("[","")
        self.mRGB=str(self.mRGB).replace("]","")
        self.X.set(str(row))
        self.Y.set(str(col_ox))
        '''
        if self.mWindowMouse != None and self.FM == True:
            self.mImg1 = ImageGrab.grab((event.x_root - 10, event.y_root - 10, event.x_root + 10, event.y_root + 10))
            multiple = 10
            size = (self.mImg1.size[0] * multiple, self.mImg1.size[1] * multiple)
            self.mImg1 = self.mImg1.resize(size).convert('RGB')
            if event.y_root > 500:
                display_x = event.x_root
                display_y = event.y_root - 300
            elif event.y_root <= 500:
                display_x = event.x_root
                display_y = event.y_root + 100
            draw = ImageDraw.Draw(self.mImg1)
            draw.rectangle((100, 100, 110, 110), fill=None, outline='red')
            self.followMouse(display_x, display_y)
        self.hbar.update()
        print(self.hbar.winfo_y(), self.hbar.winfo_x(), self.hbar.get(), self.hbar.winfo_pointerxy(),
              self.hbar.winfo_vrootx())
        return True

    # 选择裁剪范围

    def selectRegion_Press(self, event):
        print('selectRegion_Press', event)
        print(event.x, ",", event.y, ",", event.char)
        print('button_cut', self.button_cut.config()['text'])
        if str(self.button_cut.config()['text']).find('裁剪') > 0:
            return

        if self.selectRegion_start == False:
            return
        self.selectRegion_start = False
        self.vbar.update()
        print(self.vbar.winfo_y(), self.vbar.winfo_x(), self.vbar.get(), self.vbar.winfo_pointerxy(),
              self.vbar.winfo_vrootx())
        # print()
        if self.selectRegion_Press_x1 == None and self.selectRegion_Press_y1 == None:
            self.selectRegion_Press_x1 = event.x
            self.selectRegion_Press_y1 = event.y + int(1280 * self.vbar.get()[0])
            # self.current_cut_range[0]=event.x
            # self.current_cut_range[1]=event.y +int(1280*self.vbar.get()[0])

        print('x1=', self.selectRegion_Press_x1, ',y1=', self.selectRegion_Press_y1, ',x2=', event.x, 'y2=',
              event.y + int(1280 * self.vbar.get()[0]))

        img = self.currentImage.convert("RGB")
        img = np.array(img)
        # r,g,b=cv2.split(img)
        # img=cv2.merge([b,g,r])
        # 当前坐标减去起点坐标大于
        if event.y + int(1280 * self.vbar.get()[
            0]) - self.selectRegion_Press_y1 > 0 and event.x - self.selectRegion_Press_x1 > 0:
            cup = img[self.selectRegion_Press_y1:event.y + int(1280 * self.vbar.get()[0]),
                  self.selectRegion_Press_x1:event.x]
            h = event.y + int(1280 * self.vbar.get()[0]) - self.selectRegion_Press_y1
            w = event.x - self.selectRegion_Press_x1
            # self.canvas_FM.create_image(0, 0, anchor="nw", image=self.mImg1)
            img = Image.fromarray(cup)
            self.cut_img = ImageTk.PhotoImage(img)
            # self.cut_canvas
            if self.cut_canvas != None:
                self.cut_canvas.destroy()
            self.cut_canvas = self.tk.Canvas(self.canvas, bg='grey', height=h - 2, width=w - 2)

            # self.cut_canvas.setvar('cursor','fleur')

            self.cut_canvas.bind('<Motion>', self.handler_adaptor(self.cut_canvas_event, w=w, h=h))
            self.cut_canvas.bind('<B1-Motion>', self.adjustmentCutRegion)  # 鼠标按下
            self.cut_canvas.bind('<ButtonRelease-1>', self.cutCanvasEvent_MouseUp)  # 鼠标弹起
            self.cut_canvas.bind('<ButtonRelease-3>', self.cancelCut)
            self.cut_canvas.create_image(0, 0, anchor="nw", image=self.cut_img)
            # self.cut_canvas.cursor
            self.cut_canvas.place(x=self.selectRegion_Press_x1 + 2,
                                  y=self.selectRegion_Press_y1 + 2 - int(1280 * self.vbar.get()[0]))
        self.selectRegion_start = True

    def clickDown(self,event):
        print('clickDown--',event.x,',',(event.y+ int(1280 * self.vbar.get()[0])))
        self.clickDownX=event.x
        self.clickDownY=event.y+ int(1280 * self.vbar.get()[0])


    # 取消 cut_canvas 截图
    def cancelCut(self, event):
        print('cancelCut')
        if self.cut_canvas:
            self.button_cut.config(text='裁剪')
            self.cut_canvas.destroy()

    def cutCanvasEvent_MouseUp(self, event):
        self.current_cut_range[0] = None
        self.current_cut_range[1] = None
        try:
            self.entry_xy_text.set(
                str(self.cutPic_x1) + "," + str(self.cutPic_y1) + "," + str(self.cutPic_x2) + "," + str(self.cutPic_y2))
            self.entry_wh_text.set(str(self.cutPic_x1) + "," + str(self.cutPic_y1) + "," + str(
                self.cutPic_x2 - self.cutPic_x1) + "," + str(self.cutPic_y2 - self.cutPic_y1))
        except:
            pass

    # 调整裁剪范围
    def adjustmentCutRegion(self, event):
        print('adjustmentCutRegion==', event)
        print('x1=', self.cutPic_x1, ',y1=', self.cutPic_y1, ',x2=', self.cutPic_x2, ',y2=', self.cutPic_y2)
        print(self.current_cut_range[0])
        try:
            if self.current_cut_range[0] == None and self.current_cut_range[1] == None:
                self.current_cut_range[0] = int(event.x)
                self.current_cut_range[1] = int(event.y)
                return
            if self.adjustmentCutRegion_start == False:
                return
            self.adjustmentCutRegion_start = False
            # print(self.cut_canvas.config()['cursor'])

            # print(str(self.cut_canvas.config()['cursor']).find('left'))
            # print(str(self.cut_canvas.config()['cursor']).find('right'))
            # print(str(self.cut_canvas.config()['cursor']).find('up'))
            # print(str(self.cut_canvas.config()['cursor']).find('down'))

            if str(self.cut_canvas.config()['cursor']).find('left') > 0:
                print('left==', self.current_cut_range[0], ',', event.x)
                if self.current_cut_range[0] > int(event.x):
                    self.cutPic_x1 = self.cutPic_x1 - 1
                else:
                    self.cutPic_x1 = self.cutPic_x1 + 1
                # self.current_cut_range[0]=int(event.x)
            elif str(self.cut_canvas.config()['cursor']).find('right') > 0:
                print('right==', self.current_cut_range[0], ',', event.x)
                if self.current_cut_range[0] < int(event.x):
                    self.cutPic_x2 = self.cutPic_x2 + 1
                else:
                    self.cutPic_x2 = self.cutPic_x2 - 1
            elif str(self.cut_canvas.config()['cursor']).find('up') > 0:
                print('up==', self.current_cut_range[1], ',', event.y)
                if self.current_cut_range[1] > int(event.y):
                    self.cutPic_y1 = self.cutPic_y1 - 1
                else:
                    self.cutPic_y1 = self.cutPic_y1 + 1
            elif str(self.cut_canvas.config()['cursor']).find('down') > 0:
                print('down==', self.current_cut_range[1], ',', event.y)

                if self.current_cut_range[1] < int(event.y):
                    self.cutPic_y2 = self.cutPic_y2 + 1
                else:
                    self.cutPic_y2 = self.cutPic_y2 - 1
            # self.cut_canvas_event(event,self.cutPic_x2-self.cutPic_x1,self.cutPic_y2-self.cutPic_y1)
            self.cut_canvas.bind('<Motion>',
                                 self.handler_adaptor(self.cut_canvas_event, w=self.cutPic_x2 - self.cutPic_x1,
                                                      h=self.cutPic_y2 - self.cutPic_y1))

            img = self.currentImage.convert("RGB")
            img = np.array(img)
            cup = img[self.cutPic_y1:self.cutPic_y2, self.cutPic_x1:self.cutPic_x2]
            # cv2.imshow('2222',cup)
            # cv2.waitKey(100)
            print(self.cutPic_x1)
            img = Image.fromarray(cup)
            self.cut_img = ImageTk.PhotoImage(img)
            self.cut_canvas.config(width=self.cutPic_x2 - self.cutPic_x1 - 2,
                                   height=self.cutPic_y2 - self.cutPic_y1 - 2)
            self.cut_canvas.create_image(0, 0, anchor="nw", image=self.cut_img)
            self.cut_canvas.place(x=self.cutPic_x1 + 2,
                                  y=self.cutPic_y1 + 2 - int(1280 * self.vbar.get()[0]))
        except:
            self.adjustmentCutRegion_start = True

        self.adjustmentCutRegion_start = True
        # if self.judgeRange(x,y,(0,h/3,w/3,2*h/3)):
        #     print('left')
        #     self.cut_canvas.config(cursor='sb_left_arrow')
        # elif self.judgeRange(x,y,(w/3*2,h/3,w,2*h/3)):
        #     print('right')
        #     self.cut_canvas.config(cursor='sb_right_arrow')
        # elif self.judgeRange(x,y,(w/3,0,w/3*2,h/3)):
        #     print('up')
        #     self.cut_canvas.config(cursor='sb_up_arrow')
        # elif self.judgeRange(x,y,(w/3,h/3*2,w/3*2,h)):
        #     print('down')
        #     self.cut_canvas.config(cursor='sb_down_arrow')

    def selectRegion_up(self, event):
        print('selectRegion_up', event)
        print(event.x, ",", (event.y + int(1280 * self.vbar.get()[0])))
        rect=None
        if self.clickDownX==event.x and self.clickDownY==event.y + int(1280 * self.vbar.get()[0]):
            Obj = Contour()
            img = self.currentImage.convert("RGB")
            img = np.array(img)
            print(self.clickDownX,self.clickDownY)
            rect=Obj.getClickRect(self.clickDownX, self.clickDownY, img)
            img=Obj.getImage()

            img=Image.fromarray(img)
            self.mImgContourSave=img
            self.mImgContour = ImageTk.PhotoImage(img)
            self.canvasContour.create_image(0, 0, anchor="nw", image=self.mImgContour)
            self.cancelCut(None)
            print(rect)
        self.lable_RGB_entry_text.set(self.currentBGR)
        self.lable_XY_entry_text.set(str(str(event.x - 2) + "," + str(event.y - 2 + int(1280 * self.vbar.get()[0]))))
        if rect==None:
            self.cutPic_x1 = self.selectRegion_Press_x1
            self.cutPic_y1 = self.selectRegion_Press_y1
            self.cutPic_x2 = event.x
            self.cutPic_y2 = event.y + int(1280 * self.vbar.get()[0])
        else:
            self.cutPic_x1 = int(rect[0])
            self.cutPic_y1 = int(rect[1])
            self.cutPic_x2 = rect[2]+rect[0]
            self.cutPic_y2 = rect[3]+rect[1]

        print(self.currentImage)
        if self.cutPic_x1 < 0:
            self.cutPic_x1 = 0
        if self.cutPic_x2 > self.currentImage.width:
            self.cutPic_x2 = self.currentImage.width

        if self.cutPic_y1 < 0:
            self.cutPic_y1 = 0
        if self.cutPic_y2 > self.currentImage.height:
            self.cutPic_y2 = self.currentImage.height
        try:
            self.entry_xy_text.set(
                str(self.cutPic_x1) + "," + str(self.cutPic_y1) + "," + str(self.cutPic_x2) + "," + str(self.cutPic_y2))
            self.entry_wh_text.set(str(self.cutPic_x1) + "," + str(self.cutPic_y1) + "," + str(
                self.cutPic_x2 - self.cutPic_x1) + "," + str(self.cutPic_y2 - self.cutPic_y1))
        except:
            pass
        self.selectRegion_Press_x1 = None
        self.selectRegion_Press_y1 = None

    # 查找范围
    def find_Range(self, model):
        # model =0 范围
        # model=1 宽高
        print('find_Range=', model)
        print('Range=', self.find_Range_entry.get())
        # find_range=self.find_Range_entry.get()
        find_range = re.sub(r"\s+", "", self.find_Range_entry.get(), flags=re.UNICODE)
        print('re,,',find_range)
        reMatch = re.match('\d+,\d+,\d+,\d+', find_range)
        if reMatch == None:
            return
        selectRange = str(find_range).split(',')
        x1 = int(selectRange[0])
        y1 = int(selectRange[1])
        if model == 0:
            x2 = int(selectRange[2])
            y2 = int(selectRange[3])
        else:
            x2 = x1 + int(selectRange[2])
            y2 = y1 + int(selectRange[3])

        img = self.currentImage.convert("RGB")
        img = np.array(img)
        cup = img[y1:y2 + int(1280 * self.vbar.get()[0]),
              x1:x2]
        h = y2 + int(1280 * self.vbar.get()[0]) - y1
        w = x2 - x1

        img = Image.fromarray(cup)
        self.cut_img = ImageTk.PhotoImage(img)
        # self.cut_canvas
        if self.cut_canvas != None:
            self.cut_canvas.destroy()
        self.cut_canvas = self.tk.Canvas(self.canvas, bg='grey', height=h - 2, width=w - 2)

        # self.cut_canvas.setvar('cursor','fleur')

        # self.cut_canvas.bind('<Motion>', self.handler_adaptor(self.cut_canvas_event, w=w, h=h))
        # self.cut_canvas.bind('<B1-Motion>', self.adjustmentCutRegion)  # 鼠标按下
        # self.cut_canvas.bind('<ButtonRelease-1>', self.cutCanvasEvent_MouseUp)  # 鼠标弹起
        self.cut_canvas.bind('<ButtonRelease-3>', self.cancelCut)
        self.cut_canvas.create_image(0, 0, anchor="nw", image=self.cut_img)
        # self.cut_canvas.cursor
        self.cut_canvas.place(x=x1 + 2,
                              y=y1 + 2 - int(1280 * self.vbar.get()[0]))

    def cutPic(self, event):
        print('cutPic', ',', event)
        print('x1=', self.cutPic_x1, ',y1=', self.cutPic_y1, ',x2=', self.cutPic_x2, ',y2=', self.cutPic_y2)
        img = self.currentImage
        region = (self.cutPic_x1, self.cutPic_y1, self.cutPic_x2, self.cutPic_y2)
        img = img.crop(region)
        self.currentImage = img
        self.ImgList.append(self.currentImage)
        self.ImgList_index = self.ImgList_index + 1
        self.mImg = img
        self.update_mImg()

    def update_mImg(self):
        print("update_mImg")

        self.mImg = self.currentImage

        self.mImg = ImageTk.PhotoImage(self.mImg)
        self.canvas.create_image(0, 0, anchor="nw", image=self.mImg)

    def recovery(self):
        print('recovery')
        self.cancelCut(None)
        # self.mImg = Image.open(self.mImgPath)
        print(self.ImgList_index)
        if self.ImgList_index > 0:
            self.ImgList_index = self.ImgList_index - 1
            self.currentImage = self.ImgList[self.ImgList_index]
            # self.mImg=self.currentImage
            self.update_mImg()
        # self.mImg = ImageTk.PhotoImage(self.mImg)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.mImg)

    def advance(self):
        print('advance')
        print(self.ImgList_index)
        print(len(self.ImgList))
        self.cancelCut(None)

        if self.ImgList_index + 1 <= len(self.ImgList):
            self.ImgList_index = self.ImgList_index + 1
            self.currentImage = self.ImgList[self.ImgList_index]
            self.update_mImg()

    def movetLeft(self, event):
        print("left")
        PyMouse.move(None, PyMouse.position(None)[0] - 1, PyMouse.position(None)[1])

    def movetRight(self, event):
        print("left")
        PyMouse.move(None, PyMouse.position(None)[0] + 1, PyMouse.position(None)[1])

    def movetUp(self, event):
        print("left")
        PyMouse.move(None, PyMouse.position(None)[0], PyMouse.position(None)[1] - 1)

    def movetDown(self, event):
        print("left")
        PyMouse.move(None, PyMouse.position(None)[0], PyMouse.position(None)[1] + 1)

    def mSelect(self):
        print("mSelect")
        filename = self.tk.filedialog.askopenfilename()
        if filename != '':
            self.label5.config(text=filename)
            # self.label5.config(text="1111")
            self.mImgPath = filename
            self.mImg = Image.open(self.mImgPath)
            self.mImg = self.mImg.convert("RGB")

            self.currentImage = self.mImg
            self.ImgList.append(self.currentImage)
            print(len(self.ImgList))
            self.ImgList_index = self.ImgList_index + 1
            print('self.ImgList_index=',self.ImgList_index)
            self.mImg = ImageTk.PhotoImage(self.mImg)
            self.canvas.create_image(0, 0, anchor="nw", image=self.mImg)
        else:
            self.label5.config(text=" ");

    def screenCapture(self):
        print("screenCapture")
        print(self.setSize.get())
        ip = self.entry_ip.get()
        self.cancelCut(None)

        print("ip=", ip)
        while (True):
            if os.path.exists('./pic') == False:
                os.makedirs('./pic')
            else:
                break
        name = str(int(time.time()))
        self.CMD("adb -s " + ip + ":5555 shell screencap -p /sdcard/screencap.png")
        # self.CMD("adb -s " + ip + ":5555 pull /sdcard/screencap.png " + "./" + name + ".png")
        self.CMD("adb -s " + ip + ":5555 pull /sdcard/screencap.png " + "./pic\\" + name + ".png")
        self.currentImage = Image.open('./pic\\' + name + '.png')
        self.currentImage = self.currentImage.convert("RGB")

        self.mImg = self.currentImage
        if self.setSize.get() == 1:
            self.rotate()
        self.ImgList.append(self.currentImage)
        self.ImgList_index = self.ImgList_index + 1
        self.update_mImg()

    def getIpList(self):
        print("getIpList")
        ipList = self.CMD('adb devices')
        print("ipList=", ipList)

    # 旋转
    def rotate(self):
        print('rotate')
        self.cancelCut(None)
        img = self.currentImage
        img = img.transpose(Image.ROTATE_90)
        self.currentImage = img
        self.ImgList.append(self.currentImage)
        self.ImgList_index = self.ImgList_index + 1
        self.mImg = img
        self.update_mImg()

    # 提取轮廓
    def myFindContours(self):
        print('myFindContours')
        self.currentImage = np.array(self.currentImage)
        img = self.currentImage
        img = np.array(img)
        print("self=", self.combobox_find_Contour.get())
        if self.combobox_find_Contour.get() == 'cv2.RETR_LIST':
            findMode = cv2.RETR_LIST
        elif self.combobox_find_Contour.get() == 'cv2.RETR_TREE':
            findMode = cv2.RETR_TREE
        elif self.combobox_find_Contour.get() == 'cv2.RETR_CCOMP':
            findMode = cv2.RETR_CCOMP
        elif self.combobox_find_Contour.get() == 'cv2.RETR_EXTERNAL':
            findMode = cv2.RETR_EXTERNAL

        lower_red = np.array([127, 127, 127])
        upper_red = np.array([255, 255, 255])
        img = cv2.inRange(img, lower_red, upper_red)
        img2, countours, hierarchy = cv2.findContours(img, findMode, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0, len(countours)):
            x, y, w, h = cv2.boundingRect(countours[i])
            cv2.rectangle(self.currentImage, (x, y), (x + w, y + h), (255, 0, 0), 1)
        self.currentImage = Image.fromarray(self.currentImage)
        self.update_mImg()

    def mCNlist(self):
        # f=open("./CNIP.txt","r+")
        list = []

        conn = http.client.HTTPConnection("api.padyun.com")

        conn.request("GET", "/ws/serverTools.php?act=getCnList")

        res = conn.getresponse()
        data = res.read()

        # print(data.decode("utf-8"))
        # json_str = json.dumps(data.decode("utf-8"))
        data2 = json.loads(data.decode("utf-8"))
        # print(data2)
        # if str(str(data2).strip()).find('padyun') > -1:
        if str(str(data2).strip()).find('padyun') > -1:
            print(' ok http')
            for ss in data2['data']:
                print(ss['ip'])
                list.append(str(ss['ip']).strip())

            list = sorted(list)
            # print(list)



        else:
            list.append("cnbj20.padyun.cn")
            list.append("cnbj21.padyun.cn")
            list.append("cnbj22.padyun.cn")
            list.append("cnbj23.padyun.cn")
            list.append("cnbj24.padyun.cn")
            list.append("cnbj26.padyun.cn")
            list.append("cnbj28.padyun.cn")
            list.append("cnbj29.padyun.cn")
            list.append("cngz01.padyun.cn")
            list.append("cncz26.padyun.cn")
            list.append("cncz27.padyun.cn")
            list.append("cncz50.padyun.cn")
            list.append("cncz51.padyun.cn")
            list.append("cncz52.padyun.cn")
            list.append("cncz62.padyun.cn")

        return list

    def PortToIp(self, mPort):
        print('PortToIp')
        x = int(mPort) - 12400
        ip2 = int(x / 255)
        ip3 = x % 255
        print('ip2=', ip2, ',ip3=', ip3)

        return "192.168." + str(ip2) + '.' + str(ip3)

    def onlineCapture(self):
        print('onlineCapture')
        print(self.combobox1.get())
        self.cancelCut(None)
        print("IP=", self.entry_online_ip.get())
        if len(str(self.entry_online_ip.get())) <= 5:
            ip = str(self.PortToIp(self.entry_online_ip.get()))
        else:
            ip = str(self.entry_online_ip.get())

        # http: // cncz27.padyun.cn: 3000 / screensingle / 192_168_3_150?_ = 1536841042164
        conn = http.client.HTTPConnection(str(self.combobox1.get()) + ":3000")
        conn.request("GET", "/screensingle/" + ip + "?_" + str(time.time()))
        conn.getresponse()

        conn = http.client.HTTPConnection(str(self.combobox1.get()) + ":3000")
        conn.request("GET", "/images/screencap/" + ip + ".png")
        res = conn.getresponse()
        data = res.read()
        name_time=str(time.time())
        fp = open("./pic\\" + ip + "_" +name_time + ".png", "wb")
        fp.write(data)
        fp.close()
        self.currentImage = Image.open("./pic\\" + ip + "_" + name_time + ".png").convert("RGB")
        if self.setSize.get() == 1:
            self.rotate()
        self.ImgList.append(self.currentImage)
        self.ImgList_index = self.ImgList_index + 1
        self.update_mImg()

    def erodeAndDilate_(self, mMode):
        print('erodeAndDilate')
        # erodeAndDilate=self.ttk.Frame(self.tabControl,width=500,height=250)#腐蚀和膨胀
        # self.tabControl.add(erodeAndDilate,text='膨胀腐蚀')
        # self.tk.Label(erodeAndDilate,text='卷积核',width=10).place(x=0,y=40)
        # self.entry_erodeAndDilate_kernel=self.tk.Entry(erodeAndDilate,width=15)
        # self.entry_erodeAndDilate_kernel.place(x=80,y=40)
        # self.combobox_erodeAndDilate_mode = self.ttk.Combobox(erodeAndDilate, width=25)
        # self.combobox_erodeAndDilate_mode['values'] = ['cv2.MORPH_ELLIPSE','cv2.MORPH_CROSS','cv2.MORPH_RECT','自定义']
        # self.combobox_erodeAndDilate_mode.current(0)
        # self.combobox_erodeAndDilate_mode.place(x=0, y=5)
        # self.erode_button=self.tk.Button(erodeAndDilate, text="腐蚀", width=10, height=1, command=lambda :self.erodeAndDilate_("erode"))
        # self.erode_button.place(x=0,y=80)
        # self.dilate_button=self.tk.Button(erodeAndDilate, text="腐蚀", width=10, height=1, command=lambda :self.erodeAndDilate_("dilate"))
        # self.dilate_button.place(x=0,y=80)
        if self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_BLACKHAT':
            mode = cv2.MORPH_BLACKHAT
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_CLOSE':
            mode = cv2.MORPH_CLOSE
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_CROSS':
            mode = cv2.MORPH_CROSS
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_DILATE':
            mode = cv2.MORPH_DILATE
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_ELLIPSE':
            mode = cv2.MORPH_ELLIPSE
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_ERODE':
            mode = cv2.MORPH_ERODE
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_GRADIENT':
            mode = cv2.MORPH_GRADIENT
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_HITMISS':
            mode = cv2.MORPH_HITMISS
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_OPEN':
            mode = cv2.MORPH_OPEN
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_RECT':
            mode = cv2.MORPH_RECT
        elif self.combobox_erodeAndDilate_mode.get() == 'cv2.MORPH_TOPHAT':
            mode = cv2.MORPH_TOPHAT

        kernel = self.entry_erodeAndDilate_kernel.get().split(',')
        print('kernel=', kernel)
        # closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        kernel = cv2.getStructuringElement(mode, (int(kernel[0]), int(kernel[1])))
        print('kernel=', kernel)
        img = self.currentImage
        img = np.array(img)
        print('mMode=', mMode)
        if mMode == 'erode':
            img = cv2.erode(img, kernel)
        elif mMode == 'dilate':
            img = cv2.dilate(img, kernel)

        img = Image.fromarray(img)
        self.currentImage = img
        self.ImgList.append(self.currentImage)
        self.ImgList_index = self.ImgList_index + 1
        self.update_mImg()

    # def getByte(self,msoket,mFile):
    #
    #     print('getbyte')
    #     # ss=bytes([])
    #     # for i in range(1000):
    #     while True:
    #         data = msoket.recv(100000)
    #         self.wri = False
    #         mFile.write(data)
    #         self.wri = True

    # def playStream(self,s,cap):
    #     time1 = int(time.time())
    #
    #     while True:
    #         ret = False
    #         if self.wri == True:
    #             ret, frame = cap.read()
    #         # print(ret)
    #         if ret:
    #             cv2.imshow('frame', frame)
    #             cv2.waitKey(35)
    #         else:
    #             # time.sleep(1)
    #             cv2.waitKey(50)
    #         if int(time.time()) - time1 >= 25:
    #             time1 = int(time.time())
    #             s.send(bytes([0, 0, 0, 2, 0, 5]))

    def lookStream(self):
        print('lookStream')
        if self.Obj != None:
            return
        print(self.combobox1.get())
        self.videoOn_Off = False
        cn = self.combobox1.get()
        print("IP=", self.entry_online_ip.get())
        if len(str(self.entry_online_ip.get())) <= 5:
            ip = str(self.PortToIp(self.entry_online_ip.get()))
        else:
            ip = str(self.entry_online_ip.get())
        print(cn)
        print(ip)
        self.Obj = onlinevideo(cn, ip)

        t1 = threading.Thread(target=self.Obj.getVideoData)
        t1.start()
        t2 = threading.Thread(target=self.showImgVideo)
        t2.start()
        # Obj.startVideo()

    def showImgVideo(self):
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        while True:
            # print("im show ", self.Obj.mat)
            # print("im show ", type(self.Obj.mat))
            # print(isinstance(self.Obj.mat,np.ndarray))
            if isinstance(self.Obj.mat, np.ndarray):
                # print("im show ", self.Obj.mat)

                # print(self.Obj.mat)
                cv2.imshow("Video", self.Obj.mat)
                if self.videoOn_Off:
                    cv2.destroyAllWindows()
                    break

                cv2.waitKey(10)

    def stopStream(self):

        print("stopStream")
        # Obj = onlinevideo("0", "0")
        self.videoOn_Off = True
        self.Obj.stopStream()
        self.Obj = None

    def copy_wh(self):
        print('copy_wh')
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, self.entry_wh.get().encode(encoding='gbk'))
        win32clipboard.CloseClipboard()

    def copy_xy(self):
        print('copy_xy')
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, self.entry_xy.get().encode(encoding='gbk'))
        win32clipboard.CloseClipboard()

    def copy_code(self):
        print('copy_code')
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, self.code_entry.get().encode(encoding='gbk'))
        win32clipboard.CloseClipboard()

    def copy_color_code(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, self.entry_color_code.get().encode(encoding='utf-8'))
        win32clipboard.CloseClipboard()

    def minWindow(self, event):
        print("minWindow event  ", event)
        # self.mWindowMouse.iconify()

    def mCutPic(self):
        print('mCutPic')
        print('x1=', self.cutPic_x1, ',y1=', self.cutPic_y1, ',x2=', self.cutPic_x2, ',y2=', self.cutPic_y2)
        print(self.button_cut.config()['text'])
        if str(self.button_cut.config()['text']).find('裁剪') > 0:
            self.button_cut.config(text='确认')
            return
        self.button_cut.config(text='裁剪')

        img = self.currentImage.convert("RGB")
        img = np.array(img)

        cup = img[self.cutPic_y1:self.cutPic_y2, self.cutPic_x1:self.cutPic_x2]
        img = Image.fromarray(cup)
        self.currentImage = img
        self.ImgList.append(self.currentImage)
        self.ImgList_index = self.ImgList_index + 1

        # img = ImageTk.PhotoImage(img)
        self.update_mImg()
        if self.cut_canvas:
            self.cut_canvas.destroy()


    def add_color(self,event):
        print(event)
        print(int(event.keysym))
        print(self.label_X['text'])
        print(self.label_Y['text'])
        print(self.label_RGB_['text'])
        key=int(event.keysym)
        rgbValue=self.label_RGB_['text'].split(':')[1]
        strs='#'
        for i in rgbValue.split(','):
            num = int(i)
            strs += str(hex(num))[-2:].replace('x', '0').upper()
        print(strs)
        self.frame_color_List[key]['bg']=strs
        self.entry_color_StringVar_List[key].set(rgbValue)
        self.entry_xy_StringVar_List[key].set(self.label_X['text'].split(':')[1] + ',' + self.label_Y['text'].split(':')[1])




    def openCanves(self):
        # global img
        # img=Image.open("D:\\jingl\\newScript\\py\\pyNumber\\pic\\13.png")
        self.wri = False
        button1 = self.tk.Button(self.mWindow1, text="选择", width=8, command=self.mSelect)
        button1.grid(row=1, column=51, columnspan=1, rowspan=1)
        self.label_ip = self.tk.Label(self.mWindow1, text='IP').grid(row=2, column=51)

        f_IP = open('./Connect_IP.txt', 'r+')
        entry_IP = tk.StringVar()
        entry_IP.set(f_IP.read())
        f_IP.close()
        self.entry_ip = self.tk.Entry(self.mWindow1, width=20, textvariable=entry_IP)
        self.entry_ip.grid(row=2, column=52)

        self.combobox1 = self.ttk.Combobox(self.mWindow1, width=15)
        self.combobox1['values'] = self.mCNlist()
        self.combobox1.current(0)
        self.combobox1.grid(row=3, column=51)
        self.entry_online_ip = self.tk.Entry(self.mWindow1, width=20)
        self.entry_online_ip.grid(row=3, column=52)
        self.button_Capture = self.tk.Button(self.mWindow1, text='线上截屏', width=8, command=self.onlineCapture)
        self.button_Capture.grid(row=3, column=53)
        self.button_stream = self.tk.Button(self.mWindow1, text='查看', width=4, command=self.lookStream)
        self.button_stream.grid(row=3, column=54)

        self.button_stopstream = self.tk.Button(self.mWindow1, text='断开', width=4, command=self.stopStream)
        self.button_stopstream.grid(row=3, column=55)

        self.label5 = self.tk.Label(self.mWindow1, text='')
        self.label5.grid(row=1, column=52, columnspan=10, rowspan=1)
        height = 768
        self.frame = self.tk.Frame(self.mWindow1, width=1280, height=height)
        self.frame.grid(row=1, column=1, columnspan=50, rowspan=50)
        self.setSize = tk.IntVar()
        self.setSize.set(1)
        self.r1 = tk.Radiobutton(self.mWindow1, text="1280*720", variable=self.setSize, value=1)
        self.r1.grid(row=1, column=0, columnspan=1, rowspan=1)
        self.r2 = tk.Radiobutton(self.mWindow1, text="720*1280", variable=self.setSize, value=2)
        self.r2.grid(row=2, column=0, columnspan=1, rowspan=1)
        button2 = self.tk.Button(self.mWindow1, text='截屏', width=8, command=self.screenCapture)
        button2.grid(row=3, column=0, columnspan=1, rowspan=1)
        self.chVarDis = tk.IntVar()
        self.chVarDis.set(1)
        Checkbutton1 = self.tk.Checkbutton(self.mWindow1, variable=self.chVarDis, text='生成info')
        Checkbutton1.grid(row=4, column=0, columnspan=1, rowspan=1)
        button3 = self.tk.Button(self.mWindow1, text='保存', width=8, command=lambda: self.saveImg("current"))
        button3.grid(row=5, column=0, columnspan=1, rowspan=1)

        self.color_room_combobox = self.ttk.Combobox(self.mWindow1, width=6)
        self.color_room_combobox['values'] = ['RGB', 'HLS', 'HSV','二值图']
        self.color_room_combobox.current(0)
        self.color_room_combobox.grid(row=6, column=0, columnspan=1, rowspan=1)

        button4 = self.tk.Button(self.mWindow1, text='返回', width=8, command=self.recovery)
        button4.grid(row=7, column=0, columnspan=1, rowspan=1)

        button5 = self.tk.Button(self.mWindow1, text='前进', width=8, command=self.advance)
        button5.grid(row=8, column=0, columnspan=1, rowspan=1)

        button_rotate = self.tk.Button(self.mWindow1, text='旋转', width=8, command=self.rotate)
        button_rotate.grid(row=9, column=0, columnspan=1, rowspan=1)

        self.button_cut = self.tk.Button(self.mWindow1, text='裁剪', width=8, command=self.mCutPic)
        self.button_cut.grid(row=10, column=0, columnspan=1, rowspan=1)
        ######################################图片下方######################################
        self.tk.Label(self.mWindow1, text='范围', width=8).grid(row=51, column=2, columnspan=1, rowspan=1,sticky=self.tk.W)
        self.but_xy_copy = self.tk.Button(self.mWindow1, text='复制', command=self.copy_xy)
        self.but_xy_copy.grid(row=51, column=4, columnspan=1, rowspan=1, sticky=self.tk.W)
        self.entry_xy_text = self.tk.StringVar()
        self.entry_xy = self.tk.Entry(self.mWindow1, width=20, textvariable=self.entry_xy_text)
        self.entry_xy.grid(row=51, column=3, columnspan=1, rowspan=1, sticky=self.tk.W)

        self.tk.Label(self.mWindow1, text='起点+宽高', width=8).grid(row=52, column=2, columnspan=1, rowspan=1,sticky=self.tk.W)
        self.entry_wh_text = self.tk.StringVar()
        self.but_wh_copy = self.tk.Button(self.mWindow1, text='复制', command=self.copy_wh)
        self.but_wh_copy.grid(row=52, column=4, columnspan=1, rowspan=1, sticky=self.tk.W)
        self.entry_wh = self.tk.Entry(self.mWindow1, width=20, textvariable=self.entry_wh_text)
        self.entry_wh.grid(row=52, column=3, columnspan=1, rowspan=1, sticky=self.tk.W)
        self.code_label = self.tk.Label(self.mWindow1, text='code:', width=8).grid(row=53, column=2, columnspan=1,
                                                                                    rowspan=1,sticky=self.tk.W)
        self.entry_code_text = self.tk.StringVar()
        self.code_entry = self.tk.Entry(self.mWindow1, width=20, textvariable=self.entry_code_text)
        self.code_entry.grid(row=53, column=3, columnspan=1, rowspan=1, sticky=self.tk.W)
        self.code_copy = self.tk.Button(self.mWindow1, text='复制', command=self.copy_code)
        self.code_copy.grid(row=53, column=4, columnspan=1, rowspan=1, sticky=self.tk.W)

        self.find_Range_label = self.tk.Label(self.mWindow1, text='查找:', width=8).grid(row=54, column=2, columnspan=1,
                                                                                        rowspan=1,sticky=self.tk.W)
        self.find_Range_text = self.tk.StringVar()
        self.find_Range_entry = self.tk.Entry(self.mWindow1, width=15, textvariable=self.find_Range_text)
        self.find_Range_entry.grid(row=54, column=3, columnspan=1, rowspan=1, sticky=self.tk.W)
        self.find_Range_copy = self.tk.Button(self.mWindow1, text='范围', command=lambda: self.find_Range(model=0))
        self.find_Range_copy.grid(row=54, column=3, columnspan=1, rowspan=1, sticky=self.tk.E)
        self.find_Range_copy = self.tk.Button(self.mWindow1, text='宽高', command=lambda: self.find_Range(model=1))
        self.find_Range_copy.grid(row=54, column=4, columnspan=1, rowspan=1, sticky=self.tk.W)


        self.canvasEnlarge = self.tk.Canvas(self.mWindow1, bg='grey', width=200, height=200)
        self.canvasEnlarge.create_image(0, 0, anchor="nw", image=self.mImg1)
        self.canvasEnlarge.grid(row=51, column=5, columnspan=20, rowspan=20,sticky=self.tk.W) # 放大镜


        self.canvasContour = self.tk.Canvas(self.mWindow1, bg='grey', width=200, height=200)
        self.canvasContour.create_image(0, 0, anchor="nw", image=self.mImgContour)
        self.canvasContour.grid(row=51, column=19, columnspan=20, rowspan=20, sticky=self.tk.W) # canvasContour 轮廓提取展示

        # button4 = self.tk.Button(self.mWindow1, text='保存', width=8, command=self.saveImg)
        
        button4 = self.tk.Button(self.mWindow1, text='保存', width=8, command=lambda: self.saveImg("contour"))
        button4.grid(row=51, column=32, columnspan=1, rowspan=1)


        self.label_X = self.tk.Label(self.mWindow1, text='X:',width=5)
        self.label_X.grid(row=51, column=17, columnspan=1, rowspan=1)
        self.label_Y = self.tk.Label(self.mWindow1, text='Y:',width=5)
        self.label_Y.grid(row=52, column=17, columnspan=1, rowspan=1)
        self.label_RGB_ = self.tk.Label(self.mWindow1, text='RGB:')
        self.label_RGB_.grid(row=52, column=18, columnspan=1, rowspan=1, sticky=self.tk.W)


        self.lable_RGB = self.tk.Label(self.mWindow1, text='RGB:')
        self.lable_RGB.grid(row=53, column=17, columnspan=1, rowspan=1)
        self.lable_RGB_entry_text = self.tk.StringVar()
        self.lable_RGB_entry = self.tk.Entry(self.mWindow1, textvariable=self.lable_RGB_entry_text)
        self.lable_RGB_entry.grid(row=53, column=18, columnspan=1, rowspan=1)
        self.lable_XY = self.tk.Label(self.mWindow1, text='XY:')
        self.lable_XY.grid(row=54, column=17, columnspan=1, rowspan=1)
        self.lable_XY_entry_text = self.tk.StringVar()
        self.lable_XY_entry = self.tk.Entry(self.mWindow1, textvariable=self.lable_XY_entry_text)
        self.lable_XY_entry.grid(row=54, column=18, columnspan=1, rowspan=1)

        self.canvas = self.tk.Canvas(self.frame, bg='grey', height=height, width=1280, scrollregion=(0, 0, 1280, 1280))
        # windnd.hook_dropfiles(self.canvas, self.func)
        self.canvas.bind_all('<Key-Left>', self.movetLeft)
        self.canvas.bind_all('<Key-Right>', self.movetRight)
        self.canvas.bind_all('<Key-Up>', self.movetUp)
        self.canvas.bind_all('<Key-Down>', self.movetDown)
        # self.canvas.bind_all('<Control-49>',self.test_key)
        for i in range(10):
            self.canvas.bind_all('<Control-Key-'+ str(i) +'>', self.add_color)#绑定 ctrl + 键盘0-10
        self.canvas.bind('<Button-1>', self.clickDown)# 鼠标按下
        self.canvas.bind('<B1-Motion>', self.selectRegion_Press)
        self.canvas.bind('<ButtonRelease-1>', self.selectRegion_up)  # 鼠标弹起
        # self.mWindow1.bind('<ButtonRelease>',self.selectRegion_up)
        # self.canvas.bind('<Motion>',self.onMouseMove)
        self.canvas.bind('<Motion>', self.EnlargeImg)
        # self.canvas.bind_all('<Key-Return>', self.mCutPic)
        self.canvas.bind_all('<Leave>', self.minWindow)

        self.hbar = self.tk.Scrollbar(self.frame, orient=self.tk.HORIZONTAL)
        self.hbar.pack(side=self.tk.BOTTOM, fill=self.tk.X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = self.tk.Scrollbar(self.frame, orient=self.tk.VERTICAL)
        self.vbar.pack(side=self.tk.RIGHT, fill=self.tk.Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=1280, height=height)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=self.tk.LEFT, expand=True, fill=self.tk.BOTH)
        # self.cut_canvas=self.tk.Canvas(self.canvas,bg='grey',height=0,width=0)
        # self.cut_canvas.place(x=0,y=0)
        ##########################################右边选项卡##########################################
        print('-------------------------------------')
        self.tabControl = self.ttk.Notebook(self.mWindow1)
        to_Value = self.ttk.Frame(self.tabControl, width=500, height=250)
        ######二值化######
        self.tabControl.add(to_Value, text='二值化')
        self.tk.Label(to_Value, text='Minimum', width=10).place(x=0, y=10)
        self.entry_to_Value_min = self.tk.Entry(to_Value, width=15)
        self.entry_to_Value_min.place(x=80, y=10)
        self.tk.Label(to_Value, text='Maximum', width=10).place(x=0, y=40)
        self.entry_to_Value_max = self.tk.Entry(to_Value, width=15)
        self.entry_to_Value_max.place(x=80, y=40)
        to_Value_Button = self.tk.Button(to_Value, text="确定", width=8, height=1, command=self.toValue)
        to_Value_Button.place(x=210, y=30)

        to_Value_threshold = self.tk.Label(to_Value, text='阈值').place(x=10, y=70)
        self.toValue_threshold_entry_text = self.tk.StringVar()
        self.toValue_threshold_entry = self.tk.Entry(to_Value, width=15, textvariable=self.toValue_threshold_entry_text)
        self.toValue_threshold_entry.place(x=80, y=70)

        to_Value_set = self.tk.Label(to_Value, text='设定值').place(x=10, y=100)
        self.toValue_set_entry_text = self.tk.StringVar()
        self.toValue_set_entry_text.set('255')
        self.toValue_set_entry = self.tk.Entry(to_Value, width=15, textvariable=self.toValue_set_entry_text)
        self.toValue_set_entry.place(x=80, y=100)

        to_Value_mode = self.tk.Label(to_Value, text='方法').place(x=10, y=130)
        self.combobox_to_Value_mode = self.ttk.Combobox(to_Value, width=17)
        self.combobox_to_Value_mode['values'] = ['THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO',
                                                 'THRESH_TOZERO_INV']
        self.combobox_to_Value_mode.current(0)
        self.combobox_to_Value_mode.place(x=80, y=130)
        to_Value_vague_Button = self.tk.Button(to_Value, text="确定", width=8, height=1, command=self.toValue_vague)
        to_Value_vague_Button.place(x=130, y=160)
        ######轮廓提取######
        find_Contours = self.ttk.Frame(self.tabControl, width=500, height=250)  # 轮廓提取
        self.tabControl.add(find_Contours, text='轮廓提取')
        self.tabControl.grid(row=4, column=51, columnspan=10, rowspan=10)
        self.combobox_find_Contour = self.ttk.Combobox(find_Contours, width=25)
        self.combobox_find_Contour['values'] = ['cv2.RETR_LIST', 'cv2.RETR_TREE', 'cv2.RETR_CCOMP', 'cv2.RETR_EXTERNAL']
        self.combobox_find_Contour.current(0)
        self.combobox_find_Contour.place(x=0, y=5)
        self.findContours_Button = self.tk.Button(find_Contours, text='提取', width=8, height=1,
                                                  command=self.myFindContours)
        self.findContours_Button.place(x=0, y=30)
        ######锐化######
        sharpening = self.ttk.Frame(self.tabControl, width=500, height=250)  # 锐化
        self.tabControl.add(sharpening, text='锐化')
        sharpening_button_canny = self.tk.Button(sharpening, text="锐化canny", width=15, height=1,
                                                 command=lambda: self.sharpening("canny"))
        sharpening_button_canny.place(x=10, y=10)
        self.sharpening_entry_canny = self.tk.Entry(sharpening, width=15)
        self.sharpening_entry_canny.place(x=150, y=12)
        sharpening_button_filter2D = self.tk.Button(sharpening, text="锐化filter2D", width=15, height=1,
                                                    command=lambda: self.sharpening("filter2D"))
        sharpening_button_filter2D.place(x=10, y=40)
        ######腐蚀和膨胀######
        erodeAndDilate = self.ttk.Frame(self.tabControl, width=500, height=250)  # 腐蚀和膨胀
        self.tabControl.add(erodeAndDilate, text='膨胀腐蚀')
        self.tk.Label(erodeAndDilate, text='卷积核', width=10).place(x=0, y=40)
        self.entry_erodeAndDilate_kernel = self.tk.Entry(erodeAndDilate, width=15)
        self.entry_erodeAndDilate_kernel.place(x=80, y=40)
        self.combobox_erodeAndDilate_mode = self.ttk.Combobox(erodeAndDilate, width=25)
        # self.combobox_erodeAndDilate_mode['values'] = ['cv2.MORPH_BLACKHAT', 'cv2.MORPH_CLOSE', 'cv2.MORPH_CROSS',
        #                                                'cv2.MORPH_DILATE', 'cv2.MORPH_ELLIPSE', 'cv2.MORPH_ERODE',
        #                                                'cv2.MORPH_GRADIENT', 'cv2.MORPH_HITMISS', 'cv2.MORPH_OPEN',
        #                                                'cv2.MORPH_RECT', 'cv2.MORPH_TOPHAT', '自定义']
        self.combobox_erodeAndDilate_mode['values'] = ['cv2.MORPH_RECT', 'cv2.MORPH_CROSS', 'cv2.MORPH_ELLIPSE', '自定义']
        self.combobox_erodeAndDilate_mode.current(0)
        self.combobox_erodeAndDilate_mode.place(x=0, y=5)
        self.erode_button = self.tk.Button(erodeAndDilate, text="腐蚀", width=10, height=1,
                                           command=lambda: self.erodeAndDilate_("erode"))
        self.erode_button.place(x=0, y=80)
        self.dilate_button = self.tk.Button(erodeAndDilate, text="膨胀", width=10, height=1,
                                            command=lambda: self.erodeAndDilate_("dilate"))
        self.dilate_button.place(x=100, y=80)

        AIcap = self.ttk.Frame(self.tabControl, width=500, height=250)  # 腐蚀和膨胀
        self.tabControl.add(AIcap, text='AI')
        self.AI_cap(AIcap)####模型相关

        self.colorTool() ############多点找色框

    def AI_cap(self,frame):
        print('AI_cap')
        self.load_model_button=self.tk.Button(frame, text='载入模型', width=8,command=lambda: self.load_model())
        self.load_model_button.place(x=10,y=10)
        self.click_str_entry = self.tk.Entry(frame, width=8)
        self.click_str_entry.place(x=10,y=53)
        self.click_str_button=self.tk.Button(frame, text='点击', width=8,command=lambda :self.execute_model2())
        self.click_str_button.place(x=80,y=50)

    def load_model(self):
        if self.TextDetection is None:
            from model import model
            self.TextDetection=model.TextDetection()
            self.TextDistinguish=model.TextDistinguish()

    def execute_model(self):
        '''

        :return:
        '''
        time1=time.time()
        if self.TextDetection is None:
            return

        print('self.click_str_entry  ', self.click_str_entry.get())
        if self.click_str_entry.get()=='':
            print('self.click_str_entry  is empty' )
            return

        self.screenCapture()

        image = np.array(self.currentImage)
        print(image.shape)
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        self.TextDetection.image=image
        bboxes=self.TextDetection.get_bboxes()
        img_list = self.TextDetection.get_text_list()
        bbox=None
        ocr_str_all=[]
        for i in range(len(img_list)):
            self.TextDistinguish.imageToBase64(img_list[i])
            ocr_str=self.TextDistinguish.send()
            ocr_str_all.append(ocr_str)
            print('ocr_str:' ,ocr_str)
            if ocr_str==self.click_str_entry.get():
                print(bboxes[i])
                bbox=bboxes[i]
                break
                # print('ocr_str:', ocr_str)
                # print('self.click_str_entry  ', self.click_str_entry.get())
        print('length  ' , len(bboxes), ' --  ' ,len(ocr_str_all))
        if bbox is None:
            #如果指定的字符不能匹配则 找识别到语句中的字符 ,并根据需要查找字符在语句中的位置 ,计算出 bbox(图片的范围)
            for i in range(len(ocr_str_all)):
                str_=ocr_str_all[i]
                find_str_position=str_.find(self.click_str_entry.get())
                if find_str_position>-1:
                    print('str_  ' ,str_)
                    print(bboxes[i])
                    str_w=(bboxes[i][2]-bboxes[i][0]) / len(str_)
                    x1=find_str_position * str_w
                    x2=(find_str_position + len(self.click_str_entry.get())) * str_w
                    print('x1 ', int(x1) ,',x2 ',int(x2))
                    # print('find str ')
                    bbox=bboxes[i]
                    bbox[2] = bbox[0] + int(x2)
                    bbox[0]= bbox[0] + int(x1)
                    print('bbox ', bbox)

                    break

        if bbox is not None:
            img=image[bbox[1]:bbox[3],bbox[0]:bbox[2]]
            img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            img=Image.fromarray(img)
            self.mImgContourSave=img
            self.mImgContour = ImageTk.PhotoImage(img)
            self.canvasContour.create_image(0, 0, anchor="nw", image=self.mImgContour)

        print(' time ',(time.time() - time1))

    def execute_model2(self):
        if self.TextDetection is None:
            return

        print('self.click_str_entry  ', self.click_str_entry.get())
        if self.click_str_entry.get()=='':
            print('self.click_str_entry  is empty' )
            return

        # self.screenCapture()

        image = np.array(self.currentImage)
        print(image.shape)
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        self.TextDistinguish.imageToBase64(image);
        json_str = self.TextDistinguish.send_JD()

        patten = "'" + self.click_str_entry.get() + "', 'location': {'x': (\d+), 'y': (\d+), 'width': (\d+), 'height': (\d+)}"
        match=re.search(patten,str(json_str))
        print(match.group(0))
        print(match.group(1))
        print(match.group(2))
        print(match.group(3))
        print(match.group(4))
        x1=int(match.group(1))
        x2=int(match.group(1)) + int(match.group(3))
        y1=int(match.group(2))
        y2=int(match.group(2)) + int(match.group(4))


        img = image[y1:y2,x1:x2]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = Image.fromarray(img)
        self.mImgContourSave = img
        self.mImgContour = ImageTk.PhotoImage(img)
        self.canvasContour.create_image(0, 0, anchor="nw", image=self.mImgContour)


    def colorTool(self):
        Notebook_color_tool = self.ttk.Notebook(self.mWindow1)
        color_tool = self.ttk.Frame(Notebook_color_tool, width=500, height=255)
        Notebook_color_tool.add(color_tool, text='color_tool')
        Notebook_color_tool.grid(row=5, column=51, columnspan=10, rowspan=255)
        #
        self.entry_xy_StringVar_List=[]

        self.entry_xy_List=[]
        self.frame_color_List=[]
        self.entry_color_List=[]
        self.entry_color_StringVar_List=[]
        self.checkbutton_color_List=[]
        self.checkbutton_intvar_color_List=[]

        for i in range(10):
            if i==0 :
                index=10
            else:
                index = i
            y=5 + (index-1) * 25
            print('y=',y)
            self.tk.Label(color_tool, text=str(i), width=2).place(x=0, y=y)

            self.entry_xy_StringVar_List.append(self.tk.StringVar())
            self.entry_xy_List.append(self.tk.Entry(color_tool, width=8,text = self.entry_xy_StringVar_List[i]))
            self.entry_xy_List[i].place(x=20, y=y)

            self.frame_color_List.append(self.tk.Frame(color_tool, width=20,height=20,bg='#000000'))
            self.frame_color_List[i].place(x=90, y=y)

            self.entry_color_StringVar_List.append(self.tk.StringVar())
            self.entry_color_List.append(self.tk.Entry(color_tool, width=12,text=self.entry_color_StringVar_List[i]))
            self.entry_color_List[i].place(x=120, y=y)

            self.checkbutton_intvar_color_List.append(self.tk.IntVar())
            self.checkbutton_color_List.append(self.tk.Checkbutton(color_tool, variable=self.checkbutton_intvar_color_List[i],command=self.create_code))
            self.checkbutton_color_List[i].place(x=210, y=y)

            self.entry_color_code_text=self.tk.StringVar()
            self.entry_color_code=self.tk.Entry(color_tool, width=30,text=self.entry_color_code_text)
            self.entry_color_code.place(x=250, y=5)


            button_code_copy = self.tk.Button(color_tool, text='复制', command=self.copy_color_code)
            button_code_copy.place(x=250, y=30)


    def create_code(self):
        index=0;
        startDot=''
        startXY=[]
        subDot=[]
        for obj in self.checkbutton_intvar_color_List:
            # print(obj.get())
            index=index+obj.get()
        if index<2:
            print(' dot < 2  ')
            self.entry_color_code_text.set('')
            return
        for i in range(10):
            if self.checkbutton_intvar_color_List[i].get()==1 and self.entry_color_List[i].get()!='' and self.entry_xy_List[i].get()!='':
                if startDot=='':
                    startDot=self.entry_color_List[i].get()
                    startXY.append(self.entry_xy_List[i].get().split(',')[0])
                    startXY.append(self.entry_xy_List[i].get().split(',')[1])

                else:
                    x=int(self.entry_xy_List[i].get().split(',')[0])-int(startXY[0])
                    y=int(self.entry_xy_List[i].get().split(',')[1])-int(startXY[1])
                    subDot.append(str(x) + '|' + str(y) + '|' + self.entry_color_List[i].get())
            else:
                print('---error---')
        print('subDot:',subDot)
        str_subDot=subDot[0]
        subDot.remove(subDot[0])
        for ss in subDot:
            str_subDot= str_subDot + "&" + ss

        self.entry_color_code_text.set("\"" + startDot + "\"" + ';\"' + str_subDot + "\";")

    # 锐化图片
    def sharpening(self, sharpening_mode):
        print("sharpening", sharpening_mode)

        print(self.currentImage)
        img = np.array(self.currentImage)
        print(img.dtype, ",", img.size, ",", img.shape)
        if sharpening_mode == 'canny':
            print(self.sharpening_entry_canny.get())
            threshold1 = int(self.sharpening_entry_canny.get().split(',')[0])
            threshold2 = int(self.sharpening_entry_canny.get().split(',')[1])
            img = cv2.Canny(img, threshold1, threshold2)
        elif sharpening_mode == 'filter2D':
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            img = cv2.Laplacian(img, cv2.CV_16UC3)
            img = np.uint8(np.absolute(img))

        # img = cv2.filter2D(img, -1, kernel)
        # canny = cv2.Laplacian(img, cv2.CV_16UC3)  # 拉普拉斯边缘检测
        # canny = cv2.Canny(img, 100, 200)
        # canny = np.uint8(np.absolute(canny))  ##对lap去绝对值
        self.mImg = Image.fromarray(img)
        self.currentImage = self.mImg
        self.update_mImg()

    def saveImg(self,mode):
        # global filename
        # filename = tk.filedialog.askopenfilename()
        self.cancelCut(None)
        filename = tk.filedialog.asksaveasfilename()
        if filename[-4:] != '.png':
            filename = filename + '.png'

        print('x1=', self.cutPic_x1, ',y1=', self.cutPic_y1, ',x2=', self.cutPic_x2, ',y2=', self.cutPic_y2, ",chvar=",
              self.chVarDis.get())

        if self.cutPic_x1 != None and self.cutPic_y1 != None and self.cutPic_x2 != None and self.cutPic_y2 != None and self.chVarDis.get() == 1:
            f = open(filename + '.info', "w+")
            f.write('x:' + str(self.cutPic_x1) + '\n')
            f.write('y:' + str(self.cutPic_y1) + '\n')
            f.write('width:' + str(self.cutPic_x2 - self.cutPic_x1) + '\n')
            f.write('height:' + str(self.cutPic_y2 - self.cutPic_y1) + '\n')
            print("self.color_room_combobox.get()==", self.color_room_combobox.get())

            if self.color_room_combobox.get() == 'HSV':
                flag = str(40)
            elif self.color_room_combobox.get() == 'HLS':

                flag = str(52)
            elif self.color_room_combobox.get() == '二值图':
                flag = str(-1)
            else:
                flag = str(1)
            thresh=0
            maxval=0
            myType=0
            if self.color_room_combobox.get() == '二值图':
                maxval=self.toValue_set_entry.get()
                thresh=self.toValue_threshold_entry.get()
                myType=self.combobox_to_Value_mode.current()
                print(myType)
            f.write('flag:' + flag + '\n')
            f.write('thresh:'+ str(thresh)  + '\n')
            f.write('maxval:'+ str(maxval) + '\n')
            f.write('type:'+ str(myType) + '\n')
            f.close()


        # self.cutPic_x1 = None
        # self.cutPic_y1 = None
        # self.cutPic_x2 = None
        # self.cutPic_y2 = None

        if mode=='current':
            img = np.array(self.currentImage)
        else:
            img=np.array(self.mImgContourSave)

        if self.color_room_combobox.get() == 'HSV':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cv2.imwrite(filename, img)
        elif self.color_room_combobox.get() == 'HLS':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
            cv2.imwrite(filename, img)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(filename, img)

        # if self.color_room_combobox.get() != 'HSV' and self.color_room_combobox.get() != 'HLS':
        #     self.currentImage.save(filename)

        codeStr = re.search('([a-zA-Z0-9_]+)\.png', filename)

        # print(codeStr.group(1).upper())

        # JAVA 图片静态变量生成
        codeStr = 'protected static final String IMG_' + codeStr.group(1).upper() + '=\"' + codeStr.group(1) + '.png\";'

        self.entry_code_text.set(codeStr)

    def CMD(self, cmd):
        ret = subprocess.call(cmd, startupinfo=st)
        # print(ret.bit_length())
        # pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # subprocess.check_output(cmd)
        # print(pi)
        # return pi


def onMouse_leftup(event):
    print("up")


def onMouse_leftdown(event):
    print("down")


def saveH264():
    print('saveH264')
    ReceivingLength = 0
    FrontData = bytes
    time1 = int(time.time())
    s = socket.socket()  # 创建 socket 对象
    aa = s.connect_ex(('cnbj29.padyun.cn', 12400))
    msg = bytes(
        [0, 0, 0, 67, 2, 9, 33, 0, 0, 0, 0, 22, 0, 0, 0, 0, 23, 0, 0, 0, 0, 21, 0, 0, 0, 45, 115, 108, 102, 76, 106,
         102, 108, 76, 74, 70, 76, 74, 70, 68, 56, 50, 117, 50, 51, 52, 51, 52, 107, 106, 50, 108, 54, 106, 106, 75,
         106, 65, 76, 75, 50, 54, 51, 52, 50, 108, 102, 107, 106, 76, 57])

    msg1 = bytes([0, 0, 0, 22, 1, 10, 25, 0, 0, 5, 0, 26, 0, 0, 2, 208, 18, 0, 30, 132, 128, 19, 0, 0, 0, 30])
    getDataIP = socket.inet_aton('192.168.1.243')
    print(getDataIP, type(getDataIP))
    s.send(getDataIP)
    print('msg=', msg)
    s.send(msg)
    s.send(msg1)
    s.send(bytes([0, 0, 0, 2, 0, 5]))

    fileH264=open('./test.h264','wb+')
    index=0
    while True:
        data = s.recv(2097152)
        # print(data)
        fileH264.write(data)
        index=index+1
        if index>30:
            break
    fileH264.close()





if __name__ == '__main__':


    import tkinter as tk  # imports
    from ctypes import *
    import ctypes
    from tkinter import ttk
    import time
    import cv2
    import threading
    import time
    import re

    import tkinter.filedialog

    Obj = canves(tk, ttk)
    Obj.openCanves()
    Obj.mWindow1.mainloop()
