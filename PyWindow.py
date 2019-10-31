import json
import sys
import cv2
import os
# import math
import subprocess
# from tkinter import *
import cv2
import tkinter as tk  # imports
from tkinter import ttk
import tkinter.filedialog
# import windnd
import numpy as np
import re
import threading
from newCanvesTest import *
import time
from lookLog import *

import http.client

import requests



# print(windnd)
path = "D:\\jingl\\newScript\\bin\\adb\\screenshot.png"
ip = '192.168.1.79'
st = subprocess.STARTUPINFO
st.dwFlags = subprocess.STARTF_USESHOWWINDOW
st.wShowWindow = subprocess.SW_HIDE

IP_pathName='./Connect_IP.txt'
print(os.path.exists(IP_pathName))
if os.path.exists(IP_pathName)==False:
    f_IP=open(IP_pathName,'w')
    f_IP.close()
if os.path.exists('./task.uicfg')==False:
    f_task=open('./task.uicfg')
    f_task.close()

Version = "===5.0==="

def toGray():
    img = cv2.imread(path, 0)
    cv2.imwrite("D:\\jingl\\newScript\\bin\\adb\\1.png", img)


def pushJson():
    print("pushjson")
    ip = entry.get()
    f_IP = open(IP_pathName, 'r+')
    f_IP.write(ip)
    f_IP.close()
    print("combobox=", combobox.get())
    f = open(combobox.get(), "w")
    f.write(text1.get('0.0', "end"))
    f.close()
    print(os.path.exists('task.uicfg'))
    if os.path.exists('task.uicfg'):
        os.remove('task.uicfg')
    f = open('task.uicfg', "a")
    f.close()
    f = open('task.uicfg', "w+")
    f.write(text1.get('0.0', "end"))
    f.close()
    # ret = subprocess.call("adb -s " + ip + ":5555 push D:\\jingl\\newScript\\py\\task.uicfg /sdcard/yunpai_files/uicache/task.uicfg")
    ret = subprocess.call("adb -s " + ip + ":5555 push task.uicfg /sdcard/yunpai_files/uicache/task.uicfg",
                          startupinfo=st)
    # ret = subprocess.call("adb push task.uicfg /sdcard/yunpai_files/uicache/task.uicfg",
    #                       startupinfo=st)
    # os.system("adb -s " + ip + ":5555 push D:\\jingl\\newScript\\py\\task.uicfg /sdcard/yunpai_files/uicache/task.uicfg")


def startTask():
    print("startTask")
    ip = entry.get()
    # os.system("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_resume")
    ret = subprocess.call("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_resume", startupinfo=st)


def stopTask():
    print("stopTask")
    ip = entry.get()
    ret = subprocess.call("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_stop", startupinfo=st)
    # os.system("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_stop")


def startCheck():
    print("startCheck")
    ip = entry.get()
    ret = subprocess.call("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_user_disconnect", startupinfo=st)
    # os.system("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_user_disconnect")


def stopCheck():
    print("stopCheck")
    ip = entry.get()
    # os.system("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_user_connect")
    cmd = "adb -s " + ip + ":5555 shell am broadcast -a ypfairy_user_connect"

    # ret = subprocess.call(cmd,stdout=subprocess.PIPE,startupinfo=st)
    ret = subprocess.call(cmd, startupinfo=st)
    # ret = subprocess.call(cmd)


def stopTask():
    print("stopTask")
    print(entry.get())
    ip = entry.get()
    ret = subprocess.call("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_stop", startupinfo=st)
    # os.system("adb -s " + ip + ":5555 shell am broadcast -a ypfairy_stop")


def calculationCoordinate():
    # 推导公式
    cy = 1
    gy = 1
    ky = 1
    k = 1
    g = 1
    c = 1
    xy1 = entry1.get()
    xy2 = entry2.get()
    xy3 = entry3.get()
    xy4 = entry4.get()
    xy5 = entry5.get()
    xy6 = entry6.get()

    testXY = entry8.get()

    gx1 = int(xy1.split(',')[0])
    gy1 = int(xy1.split(',')[1])
    gx2 = int(xy2.split(',')[0])
    gy2 = int(xy2.split(',')[1])
    gx3 = int(xy3.split(',')[0])
    gy3 = int(xy3.split(',')[1])

    sx1 = int(xy4.split(',')[0])
    sy1 = int(xy4.split(',')[1])
    sx2 = int(xy5.split(',')[0])
    sy2 = int(xy5.split(',')[1])
    sx3 = int(xy6.split(',')[0])
    sy4 = int(xy6.split(',')[1])
    ans = ((gx1 * gy2 * k) + (gy1 * g * gx3) + (c * gx2 * gy3) - (c * gy2 * gx3) - (gx1 * g * gy3) - (gy1 * gx2 * k))
    xans = ((sx1 * gy2 * k) + (gy1 * g * sx3) + (c * sx2 * gy3) - (c * gy2 * sx3) - (sx1 * g * gy3) - (gy1 * sx2 * k))
    yans = ((gx1 * sx2 * k) + (sx1 * g * gx3) + (c * gx2 * sx3) - (c * sx2 * gx3) - (gx1 * g * sx3) - (sx1 * gx2 * k))
    zans = ((gx1 * gy2 * sx3) + (gy1 * sx2 * gx3) + (sx1 * gx2 * gy3) - (sx1 * gy2 * gx3) - (gx1 * sx2 * gy3) - (
            gy1 * gx2 * sx3))
    ansy = ((gx1 * gy2 * ky) + (gy1 * gy * gx3) + (cy * gx2 * gy3) - (cy * gy2 * gx3) - (gx1 * gy * gy3) - (
            gy1 * gx2 * ky))
    xansy = ((sy1 * gy2 * ky) + (gy1 * gy * sy4) + (cy * sy2 * gy3) - (cy * gy2 * sy4) - (sy1 * gy * gy3) - (
            gy1 * sy2 * ky))
    yansy = ((gx1 * sy2 * ky) + (sy1 * gy * gx3) + (cy * gx2 * sy4) - (cy * sy2 * gx3) - (gx1 * gy * sy4) - (
            sy1 * gx2 * ky))
    zansy = ((gx1 * gy2 * sy4) + (gy1 * sy2 * gx3) + (sy1 * gx2 * gy3) - (sy1 * gy2 * gx3) - (gx1 * sy2 * gy3) - (
            gy1 * gx2 * sy4))

    x = xans / ans
    y = yans / ans
    z = zans / ans
    xy = xansy / ansy
    yy = yansy / ansy
    zy = zansy / ansy
    gamex = "x=gmx *" + str(round(x, 4)) + "+gmy *" + str(round(y, 4)) + "+" + str(round(z, 4))
    gamey = "y=gmx *" + str(round(xy, 4)) + "+gmy *" + str(round(yy, 4)) + "+" + str(round(zy, 4))
    print(gamex)
    print(gamey)
    default_value = tk.StringVar()
    default_value.set(gamex)
    tk.Entry(tab2, text=gamex, width=50, textvariable=default_value).place(x=30, y=90)
    # entry10=tk.Entry(tab2, text=gamex, width=50, textvariable=default_value).place(x=30, y=130)

    default_value = tk.StringVar()
    default_value.set(gamey)
    tk.Entry(tab2, text=gamex, width=50, textvariable=default_value).place(x=30, y=120)

    if testXY:
        print("OK")
        gmx = int(testXY.split(',')[0])
        gmy = int(testXY.split(',')[1])
        gamex = gmx * x + gmy * y + z
        gamey = gmx * xy + gmy * yy + zy
        default_value = tk.StringVar()
        default_value.set(str(round(gamex)) + "," + str(round(gamey)))
        tk.Entry(tab2, text=gamex, width=10, textvariable=default_value).place(x=210, y=40)

    else:
        print("null")


def calculationFormula():
    print("ip=", ip)
    testXY = entry8.get()
    x = entry10.get();
    y = entry11.get();
    print("testXY=", testXY, ",x=", x, ",y=", y)
    if testXY and x and y:
        print("OK")
        gmx = testXY.split(',')[0]
        print("gmx=", gmx)
        gmy = testXY.split(',')[1]
        x = x.replace("gmx", gmx)
        x = x.replace("gmy", gmy)
        print("x=", x)
        y = y.replace("gmx", gmx)
        y = y.replace("gmy", gmy)
        x = eval(x)
        y = eval(y)
        print(",x=", x, ",y=", y)
        default_value = tk.StringVar()
        default_value.set(str(round(x)) + "," + str(round(y)))
        tk.Entry(tab2, text="", width=10, textvariable=default_value).place(x=210, y=40)
        # gamex = gmx * x + gmy * y + z
        # gamey = gmx * xy + gmy * yy + zy
        # default_value = tk.StringVar()
        # default_value.set(str(round(gamex)) + "," + str(round(gamey)))
        # tk.Entry(tab2, text=gamex, width=10, textvariable=default_value).place(x=210, y=40)


#
# gmx * 3.0185 + gmy * -0.0048 + 160.1295
# gmx * -0.0093 + gmy * -3.0132 + 665.4196


def clickScreen():
    print("clickScreen")
    ip = entry.get()
    xy = entry7.get()
    x = int(xy.split(',')[0])
    y = int(xy.split(',')[1])
    ret = subprocess.call("adb -s " + ip + ":5555 shell input tap " + str(x) + " " + str(y), startupinfo=st)


def getWH():
    print("getWH")
    xy = entry9.get()
    x1 = int(xy.split(',')[0])
    y1 = int(xy.split(',')[1])
    x2 = int(xy.split(',')[2])
    y2 = int(xy.split(',')[3])
    W = x2 - x1
    H = y2 - y1
    entry9wh = "W=" + str(W) + "," + "H=" + str(H)
    label1 = tk.Label(mWindow, text=entry9wh, width=15, height=1).place(x=570, y=100)


def CMD(cmd):
    ret = subprocess.call(cmd, startupinfo=st)


def xz():
    global filename
    filename = tk.filedialog.askopenfilename()
    if filename != '':
        label5.config(text=filename);
    else:
        label5.config(text="空");


def findpic(string):
    # global setSize
    print("filename=", filename)
    print("filename=", filename.split("/"))
    arr = filename.split("/")[-1]
    ip = entry.get()
    print("ip=", ip)
    print("setSize=", setSize.get())
    print(os.path.exists('screencap.png'))
    CMD("adb -s " + ip + ":5555 shell screencap -p /sdcard/screencap.png")
    CMD("adb -s " + ip + ":5555 pull /sdcard/screencap.png ")
    print(os.path.exists('screencap.png'))
    if os.path.exists('screencap.png') != True:
        return
    img_screencap = cv2.imread("screencap.png")
    if setSize.get() == 1:
        print("旋转")
        img_screencap = np.rot90(img_screencap)
    # cv2.imwrite("screencap.png", img1)
    # print("1111111111111111111",img1.shape)
    img2 = cv2.imread(filename)
    print(img2.shape)

    res = cv2.matchTemplate(img2, img_screencap, cv2.TM_CCOEFF_NORMED)
    print("res.shape=", res.shape)
    # for ret in res:
    #     print(ret.shape)
    #     print(ret)
    #
    # print(res[380][1159])
    # # print()
    # res[380][1159]=0.1
    minandmax = cv2.minMaxLoc(res)
    minandmaxRGB = minandmax
    print("res=", minandmax)
    print("x=", minandmax[3][0])
    print("y=", minandmax[3][1])
    print("sim=", minandmax[1])
    printStr = "x=" + str(minandmax[3][0]) + ",y=" + str(minandmax[3][1]) + ",sim=" + str(minandmax[1])
    label6 = tk.Label(tab3, text=printStr, width=40, height=1).place(x=100, y=40)
    if combobox_switch.get()=='是':
        img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2HSV)

    img1 = cv2.cvtColor(img_screencap, cv2.COLOR_RGB2HSV)
    # cv2.imshow("COLOR_BGR2HSV", img1)
    res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    minandmax = cv2.minMaxLoc(res)
    minandmaxHSV = minandmax
    print("minandmax=", minandmax)
    print("minandmax=", minandmax[3])
    print("minandmax=", minandmax[3][0])
    print("minandmax=", str(minandmax[3][0]))
    printStr = "x=" + str(minandmax[3][0]) + ",y=" + str(minandmax[3][1]) + ",sim=" + str(minandmax[1])
    label7 = tk.Label(tab3, text=printStr, width=40, height=1).place(x=100, y=70)
    if combobox_switch.get()=='是':
        img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2HLS)

    img1 = cv2.cvtColor(img_screencap, cv2.COLOR_RGB2HLS)
    # cv2.imshow("COLOR_BGR2HLS",img1)
    res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    minandmax = cv2.minMaxLoc(res)
    minandmaxHLS = minandmax
    printStr = "x=" + str(minandmax[3][0]) + ",y=" + str(minandmax[3][1]) + ",sim=" + str(minandmax[1])
    label8 = tk.Label(tab3, text=printStr, width=40, height=1).place(x=100, y=100)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2XYZ)
    # img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2XYZ)
    # res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    # minandmax = cv2.minMaxLoc(res)
    # printStr = "x=" + str(minandmax[3][0]) + ",y=" + str(minandmax[3][1]) + ",sim=" + str(minandmax[1])
    # label9 = tk.Label(tab3, text=printStr, width=40, height=1).place(x=100, y=130)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2YCrCb)
    # img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2YCrCb)
    # res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    # minandmax = cv2.minMaxLoc(res)
    # printStr = "x=" + str(minandmax[3][0]) + ",y=" + str(minandmax[3][1]) + ",sim=" + str(minandmax[1])
    # label10 = tk.Label(tab3, text=printStr, width=40, height=1).place(x=100, y=160)

    print("printStr=", printStr)
    if string == "HSV":
        minandmax = minandmaxHSV
    elif string == "HLS":
        minandmax = minandmaxHLS
    else:
        minandmax = minandmaxRGB
    x_1 = minandmax[3][0] - 50
    if x_1 < 0:
        x_1 = 0;
    y_1 = minandmax[3][1] - 50
    if y_1 < 0:
        y_1 = 0
    x_2 = minandmax[3][0] + img2.shape[1] + 50
    print(x_2)
    y_2 = minandmax[3][1] + img2.shape[0] + 50
    print(setSize)
    if setSize.get() == 1:
        print(x_2)
        if x_2 >= 1280:
            x_2 = 1280
        if y_2 >= 720:
            y_2 = 720

    if string == "HSV":
        codeStr = "result = publicFunction.localFindPicHSV(" + str(x_1) + ", " + str(y_1) + ", " + str(
            x_2) + ", " + str(
            y_2) + ", " + "\"" + filename.split("/")[
                      -1] + "\"" + ");\nif (result.sim >= 0.8) {\npublicFunction.rndTapWH(result.x,result.y," + str(
            img2.shape[1]) + "," + str(img2.shape[0]) + ");\nThread.sleep(500);\n}"
    elif string == "HLS":
        codeStr = "result = publicFunction.localFindPicHLS(" + str(x_1) + ", " + str(y_1) + ", " + str(
            x_2) + ", " + str(
            y_2) + ", " + "\"" + filename.split("/")[
                      -1] + "\"" + ");\nif (result.sim >= 0.8) {\npublicFunction.rndTapWH(result.x,result.y," + str(
            img2.shape[1]) + "," + str(img2.shape[0]) + ");\nThread.sleep(500);\n}"
    else:
        codeStr = "result = publicFunction.localFindPic(" + str(x_1) + ", " + str(y_1) + ", " + str(x_2) + ", " + str(
            y_2) + ", " + "\"" + filename.split("/")[
                      -1] + "\"" + ");\nif (result.sim >= 0.8) {\npublicFunction.rndTapWH(result.x,result.y," + str(
            img2.shape[1]) + "," + str(img2.shape[0]) + ");\nThread.sleep(500);\n}"
    default_value = tk.StringVar()
    default_value.set(codeStr)
    text2 = tk.Text(tab3, width=75, height=5)
    text2.insert(tk.INSERT, codeStr)
    text2.place(x=0, y=190)


def toValue():
    print("toValue=")
    print("filename", filename)
    print(entry13.get(), ",", entry14.get())
    print()
    min = entry13.get()
    max = entry14.get()
    if filename != '' and min != '' and max != '':
        print("OK")
    else:
        return

    min1 = int(min.split(',')[2])
    min2 = int(min.split(',')[1])
    min3 = int(min.split(',')[0])
    max1 = int(max.split(',')[2])
    max2 = int(max.split(',')[1])
    max3 = int(max.split(',')[0])
    lower_red = np.array([min1, min2, min3])
    upper_red = np.array([max1, max2, max3])

    img2 = cv2.imread(filename)

    img2 = cv2.inRange(img2, lower_red, upper_red)

    cv2.imshow("img", img2)


def rotate(image, angle, center=None, scale=1.0):  # 1
    (h, w) = image.shape[:2]  # 2
    if center is None:  # 3
        center = (w // 2, h // 2)  # 4

    M = cv2.getRotationMatrix2D((640, 360), angle, scale)  # 5

    rotated = cv2.warpAffine(image, M, (w, h))  # 6
    return rotated  # 7


def loadTaskUICfg():
    global text1
    print("loadTaskUICfg")
    print(text1)
    print("combobox=", combobox.get())
    f = open(combobox.get(), "r+")
    # default_value = tk.StringVar()
    # default_value.set(f.readline())
    # entry8 = tk.Entry(tab1, width=100, textvariable=default_value)
    text1 = tk.Text(tab1, width=70, height=5)
    text1.insert(tk.INSERT, f.readline())
    f.close()
    text1.place(x=0, y=80)


def mCNlist():
    # f=open("./CNIP.txt","r+")
    print('mCNlist')
    list = []

    conn = http.client.HTTPConnection("api.padyun.com")

    conn.request("GET", "/ws/serverTools.php?act=getCnList")

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))
    # json_str = json.dumps(data.decode("utf-8"))
    data2 = json.loads(data.decode("utf-8"))
    # print(data2)
    if str(str(data2).strip()).find('padyun') > -1:
        print(' ok http')
        for ss in data2['data']:
            print(ss['ip'])
            list.append(str(ss['ip']).strip())

        list = sorted(list)
    # fileTXT="./CNIP.txt"
    # if os.path.exists(fileTXT):
    #     # f=open(fileTXT,"r+")
    #     # print(f)
    #     # line=f.readline()
    #     for line in open(fileTXT,"r+"):
    #         print(str(line).strip())
    #         list.append(str(line).strip())
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


def getDownload():
    print("getDownload")
    print("cn=", combobox1.get())
    print("IP=", entry12.get())
    mip = entry12.get()
    if len(mip) == 5:
        mip = PortToIp(mip)

    mIP = re.match("\d+\.\d+\.\d+\.\d+", mip)
    if mIP == None:
        print(" IP is error")
        return

    global conn
    conn = http.client.HTTPConnection(str(combobox1.get()))
    conn.request("GET", "/webscriptlog/?asip=" + mip)
    pathList = []
    print(len(pathList))
    while (len(pathList) == 0):
        try:
            res = conn.getresponse()
            print("res=", res)
        except:
            print("res is error")
            return
        print("res.status=", res.status, ",reason=", res.reason)
        data = res.read()
        print("data=", data.decode("utf-8"))
        pathList = data.decode("utf-8")
        pathList = re.findall(r"fairy_log/(\S+log)", pathList)
        print("path=", pathList)
    combobox2['values'] = pathList
    combobox2.current(0)


def PortToIp(mPort):
    print('PortToIp')
    x = int(mPort) - 12400
    ip2 = int(x / 255)
    ip3 = x % 255
    print('ip2=', ip2, ',ip3=', ip3)

    return "192.168." + str(ip2) + '.' + str(ip3)


def Download():
    print("Download")
    print(combobox2.get())
    print("IP=", entry12.get())
    mip = entry12.get()
    if len(mip) == 5:
        mip = PortToIp(mip)

    global conn
    conn.request("GET", "/webscriptlog/?asip=" + mip + "&logname=" + combobox2.get())
    res = conn.getresponse()
    data = res.read()
    print("data", data.decode("utf-8"))
    mURL = re.search("(\d+\.\d+\.\d+\.\d+)(\S+)\'>", data.decode("utf-8"))
    print("mURL=", mURL.group(1))
    print("mURL=", mURL.group(2))
    conn = http.client.HTTPConnection(mURL.group(1))
    filename = re.search("\'>(\S+)<\/", data.decode("utf-8")).group(1)
    print("filename=", filename)
    conn.request("GET", mURL.group(2))
    res = conn.getresponse()
    data = res.read()
    print(data)
    print(len(data))
    if len(data) > 300:
        # print(data.decode("utf-8"))
        # mLogFile = open(filename, "w+",encoding='utf-8')
        mLogFile = open(filename, "wb+")
        # mLogFile.write(data.decode("utf-8"))
        mLogFile.write(data)
        combobox2['values'] = []
        combobox2.set("")
        mLogFile.close()
    else:
        print("return error")
        return


def openCanves():
    print("openCanves")
    obj = canves(tk, ttk)
    obj.openCanves()


def mLookLog():
    print('lookLog')
    print(combobox1.get())
    print("IP=", entry12.get())

    obj = lookLog(tk, ttk, combobox1.get(), entry12.get())
    obj.mLookLog()
    obj.threads[0].setDaemon(True)
    obj.threads[0].start()

def connectIP():
    print("connectIP")
    ip = entry.get()
    ret = subprocess.call("adb connect " + ip , startupinfo=st)

def rebootIP():
    print("rebootIP")
    threads = []
    t1 = threading.Thread(target=reboot)
    threads.append(t1)
    threads[0].setDaemon(True)
    threads[0].start()

def reboot():
    ip = entry.get()
    ret = subprocess.call("adb -s " + ip + ":5555 reboot", startupinfo=st)

installPath_Str=''

def setInstallPathThread():
    global installStart
    print('installStart=' , installStart)
    if installStart['text']=='wait':
        print('wait install')
        return
    threads = []
    t1 = threading.Thread(target=installApk)
    threads.append(t1)
    threads[0].setDaemon(True)
    threads[0].start()


def setInstallPath():
    global selectInstallPath_label
    global installPath_Str
    filename = tk.filedialog.askopenfilename()
    if filename != '':
        installPath_Str=filename
        mStr=re.search('\S+\/([\S+\.apk]+)',filename)
        print("mStr=", mStr[1])
        if mStr:
            selectInstallPath_label.config(text=mStr[1]);
        else:
            selectInstallPath_label.config(text='错误');
        print("filename=",filename)
    else:
        self.label5.config(text="空");

def installApk():
    global installPath_Str
    global installStart

    ip = entry.get()
    # result = os.popen('adb devices')
    # mss=(str(result.read()).replace(' ','')).replace('\n','')
    # ss=re.search(ip,mss)
    # print("ss=",ss)
    # if ss==None:
    #     installStart['text'] = 'not devices'
    #     return

    installStart['text']='wait'

    print('installApk')
    print("adb -s " + ip + ':5555 install -r ' + installPath_Str)



    ret = subprocess.call("adb -s " + ip + ':5555 install -r ' + installPath_Str, startupinfo=st)
    print("ret=" , ret)
    installStart['text']='OK'

#连接soket,将收到的数据保存
def saveH264():
    #保存h264文件
    print('saveH264')

    print('cn=',combobox1.get())
    print("IP=", entry12.get())
    mip = entry12.get()
    if len(mip) == 5:
        mip = PortToIp(mip)
    print("mip=", mip)
    # time.sleep(1000)
    time1 = int(time.time())
    s = socket.socket()  # 创建 socket 对象
    aa = s.connect_ex((combobox1.get(), 12400))
    msg = bytes(
        [0, 0, 0, 67, 2, 9, 33, 0, 0, 0, 0, 22, 0, 0, 0, 0, 23, 0, 0, 0, 0, 21, 0, 0, 0, 45, 115, 108, 102, 76, 106,
         102, 108, 76, 74, 70, 76, 74, 70, 68, 56, 50, 117, 50, 51, 52, 51, 52, 107, 106, 50, 108, 54, 106, 106, 75,
         106, 65, 76, 75, 50, 54, 51, 52, 50, 108, 102, 107, 106, 76, 57])
    #[0, 0, 0, 22, 1, 10, 25, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # msg1 = bytes([0, 0, 0, 22, 1, 10, 25, 0, 0, 5, 0, 26, 0, 0, 2, 208, 18, 0, 30, 132, 128, 19, 0, 0, 0, 30])
    msg1 = bytes([0, 0, 0, 22, 1, 10, 25, 0, 0, 5, 0, 26, 0, 0, 2, 256-48, 18, 0, 30, 256-124, 256-128, 19, 0, 0, 0, 30])
    getDataIP = socket.inet_aton(mip)
    print(getDataIP, type(getDataIP))
    s.send(getDataIP)
    print('msg=', msg)
    s.send(msg)
    s.send(msg1)
    s.send(bytes([0, 0, 0, 2, 0, 5]))

    fileH264=open('./test.h264','ab+')
    index=0
    while True:
        data = s.recv(2097152)
        # print(data)
        fileH264.write(data)
        index=index+1
        if button_RecordingH264['text'] == '录制h264':
            print('saveH264 stop')
            break
        if index>100:
            index==0
            s.send(bytes([0, 0, 0, 2, 0, 5]))

    fileH264.close()




#开始录制h264
def getH264File():
    print(button_RecordingH264['text'])

    if button_RecordingH264['text']=='录制h264':
        button_RecordingH264['text']='停止录制'
        threads = []
        t1 = threading.Thread(target=saveH264)
        threads.append(t1)
        threads[0].setDaemon(True)
        threads[0].start()
    else:
        button_RecordingH264['text'] = '录制h264'
        time.sleep(1)
#播放h264文件
def h264Play ():
    cap = cv2.VideoCapture()
    # f = open(r'E:\h264Play\CH-VSPlayer V6.2.0_3\test.h264', 'wb+')
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('A', 'V', 'C', '1'))

    cap.open('./test.h264')
    index=0
    while True:
        try:
            ret,frame = cap.read()
        except :
            print('error')
        print(cap.isOpened())
        if ret:
            # print(frame)
            try:
                cv2.imshow('frame',frame)
            except:
                print('error')
        else:
           index=index+1
        cv2.waitKey(25)
        if index>120:
            button_playH264['text'] = '播放h264'
            break
        if button_playH264['text'] == '播放h264':
            break
    print('release')
    cv2.destroyAllWindows()
    cap.release()

def startPlay():
    if button_playH264['text']=='播放h264':
        button_playH264['text']='停止'
        print('start')
        threads = []
        t1 = threading.Thread(target=h264Play)
        threads.append(t1)
        threads[0].setDaemon(True)
        try:
            threads[0].start()
        except :
            print('error')
    else:
        button_playH264['text'] = '播放h264'
        time.sleep(1)



print(os.path.split(os.path.realpath(__file__))[0])
uicfgList = []
# for root, dirs, files in os.walk(os.path.split(os.path.realpath(__file__))[0]):
#     list1 = files
#     print(files)
list_dir = os.listdir(os.path.split(os.path.realpath(__file__))[0])
print(list_dir)
for file in list_dir:
    if os.path.splitext(file)[1] == '.uicfg':
        uicfgList.append(file)
        print(file)

print(uicfgList)

# obj = canves()
# obj.openCanves()


mWindow = tk.Tk()
mWindow.title("Python GUI")

mWindow.geometry('700x300+500+200')

mWindow.resizable(width=False, height=False)

f_IP = open(IP_pathName, 'r+')
current_ip=f_IP.read()
f_IP.close()
entry_IP =tk.StringVar()
entry_IP.set(current_ip)
entry = tk.Entry(mWindow, width=20,textvariable = entry_IP)
label1 = tk.Label(mWindow, text="IP", width=1, height=1)
butReboot=tk.Button(mWindow,text="reboot",width=8,height=1,command=rebootIP).place(x=510,y=30)
butConnect=tk.Button(mWindow,text="connect",width=8,height=1,command=connectIP).place(x=600,y=30)

selectInstallPath_button = tk.Button(mWindow, text="选择", width=5, command=setInstallPath).place(x=510,y=65)
selectInstallPath_label = tk.Label(mWindow, text='')
selectInstallPath_label.place(x=560,y=65)

install_button=tk.Button(mWindow, text="安装", width=5, command=setInstallPathThread).place(x=510,y=95)
installStart=tk.Label(mWindow,text='OK')

installStart.place(x=560,y=95)

entry7 = tk.Entry(mWindow, width=10)
button8 = tk.Button(mWindow, text="点击屏幕", width=8, height=1, command=clickScreen).place(x=600, y=140)
entry9 = tk.Entry(mWindow, width=10)
button9 = tk.Button(mWindow, text="计算宽高", width=8, height=1, command=getWH).place(x=600, y=170)
label9 = tk.Label(mWindow, text=Version, width=50, height=1).place(x=0, y=280)

butOpenCanves = tk.Button(mWindow, text="打开图像处理工具", width=15, height=1, command=openCanves).place(x=510, y=200)

tabControl = ttk.Notebook(mWindow)  # Create Tab Control
tab1 = ttk.Frame(tabControl, width=500, height=250)
tab2 = ttk.Frame(tabControl, width=500, height=250)
tab3 = ttk.Frame(tabControl, width=500, height=250)
tab4 = ttk.Frame(tabControl, width=500, height=250)
tab5 = ttk.Frame(tabControl, width=500, height=250)

tabControl.add(tab1, text='任务控制')
# button=Button(tk,text="灰度",width=10,height=3,command = toGray)
# button1=Button(tk,text="二值",width=10,height=3,command=toValue)
button2 = tk.Button(tab1, text="设置选项", width=8, height=1, command=pushJson)
button3 = tk.Button(tab1, text="开始任务", width=8, height=1, command=startTask)
button6 = tk.Button(tab1, text="停止任务", width=8, height=1, command=stopTask)
button4 = tk.Button(tab1, text="监控开始", width=8, height=1, command=startCheck)
button5 = tk.Button(tab1, text="监控停止", width=8, height=1, command=stopCheck)
button17 = tk.Button(tab1, text="载入", width=7, height=1, command=loadTaskUICfg)
combobox = ttk.Combobox(tab1, width=12)
combobox['values'] = uicfgList

for i in range(0, len(uicfgList)):
    print(uicfgList[i])
    if uicfgList[i] == 'task.uicfg':
        combobox.current(i)
print(combobox.get())
f = open(combobox.get(), "r+")
# default_value = tk.StringVar()
# default_value.set(f.readline())

# entry8 = tk.Entry(tab1, width=100, textvariable=default_value)
text1 = tk.Text(tab1, width=70, height=5)
text1.insert(tk.INSERT, f.readline())
f.close()

# tk.Entry(tab2, text=gamex, width=50, textvariable=default_value).place(x=30, y=130)

tabControl.add(tab2, text='坐标计算')
label2 = tk.Label(tab2, text="游戏坐标", width=6, height=1).place(x=40, y=0)
entry1 = tk.Entry(tab2, width=10)
entry2 = tk.Entry(tab2, width=10)
entry3 = tk.Entry(tab2, width=10)
label3 = tk.Label(tab2, text="屏幕坐标", width=6, height=1).place(x=130, y=0)
entry4 = tk.Entry(tab2, width=10)
entry5 = tk.Entry(tab2, width=10)
entry6 = tk.Entry(tab2, width=10)
label4 = tk.Label(tab2, text="测试坐标", width=6, height=1).place(x=220, y=0)
entry8 = tk.Entry(tab2, width=10)
entry10 = tk.Entry(tab2, text="", width=50)
entry11 = tk.Entry(tab2, text="", width=50)
button7 = tk.Button(tab2, text="推导公式", width=8, height=1, command=calculationCoordinate)
button16 = tk.Button(tab2, text="运算公式", width=8, height=1, command=calculationFormula)

tabControl.add(tab3, text='测试图色')
label5 = tk.Label(tab3, text='')
button10 = tk.Button(tab3, text="选择", width=8, command=xz)
button11 = tk.Button(tab3, text="RGB", width=8, command=lambda: findpic("RGB"))
button12 = tk.Button(tab3, text="HSV", width=8, command=lambda: findpic("HSV"))
button13 = tk.Button(tab3, text="HLS", width=8, command=lambda: findpic("HLS"))
button18 = tk.Button(tab3, text="二值化", width=8, command=lambda: toValue())
lable_switch=tk.Label(tab3,text='是否转换查找图')
combobox_switch=ttk.Combobox(tab3,text='转换原图',width=6)
combobox_switch['values']=['否','是']
combobox_switch.current(0)
entry13 = tk.Entry(tab3, width=15)
entry14 = tk.Entry(tab3, width=15)

tabControl.add(tab4, text='日志相关')
combobox1 = ttk.Combobox(tab4, width=25)
CNList = mCNlist()
combobox1['values'] = CNList
combobox1.current(0)
entry12 = tk.Entry(tab4, width=28)
button14 = tk.Button(tab4, text="获取文件列表", width=12, height=1, command=lambda: getDownload())
button_lookLog = tk.Button(tab4, text='查看线上日志', width=12, height=1, command=mLookLog)
combobox2 = ttk.Combobox(tab4, width=25)
combobox2['values'] = []
button15 = tk.Button(tab4, text="下载", width=5, height=1, command=lambda: Download())
button_RecordingH264=tk.Button(tab4,text='录制h264',width=8, height=1,command=lambda: getH264File())
button_playH264=tk.Button(tab4,text='播放h264',width=8, height=1,command=lambda: startPlay())

tabControl.add(tab5,text='任务配置')



setSize = tk.IntVar()
setSize.set(1)
r1 = tk.Radiobutton(mWindow, text="横屏", variable=setSize, value=1)

r2 = tk.Radiobutton(mWindow, text="竖屏", variable=setSize, value=2)
# tab1=Frame(tk)
# tk.add(tab1,text='tab 1')
# frame= tk.Frame(height = 50,width = 50,bg = "red")
# frame1=tk.Frame(height = 50,width = 50,bg = "blue")
# e=Entry(tk,show='*')

# button1.bind("<Button-1>",hhhh())
# button.pack(side='left')
# button.place(x=10,y=10,anchor=NW)
# frame1.pack()
# frame.pack()


tabControl.place(x=0, y=0)
entry.place(x=550, y=0)
entry1.place(x=30, y=20)
entry2.place(x=30, y=40)
entry3.place(x=30, y=60)
entry4.place(x=120, y=20)
entry5.place(x=120, y=40)
entry6.place(x=120, y=60)
entry7.place(x=510, y=140)
entry8.place(x=210, y=20)
entry9.place(x=510, y=170)
entry10.place(x=30, y=90)
entry11.place(x=30, y=120)
entry12.place(x=0, y=40)
entry13.place(x=100, y=135)
entry14.place(x=250, y=135)
label1.place(x=520, y=0)
label5.place(x=100, y=10)
combobox.place(x=0, y=50)
combobox1.place(x=0, y=5)
combobox2.place(x=0, y=80)
button17.place(x=120, y=45)

# button1.pack(side='left')
button2.place(x=0, y=10)
button3.place(x=100, y=10)
button4.place(x=300, y=10)
button5.place(x=400, y=10)
button6.place(x=200, y=10)
button7.place(x=30, y=150)
button10.place(x=10, y=10)
button11.place(x=10, y=40)
button12.place(x=10, y=70)
button13.place(x=10, y=100)
button14.place(x=0, y=120)
button15.place(x=150, y=120)
button_lookLog.place(x=0, y=160)
button16.place(x=120, y=150)
button18.place(x=10, y=130)
button_RecordingH264.place(x=130,y=160)
button_playH264.place(x=0,y=200)

lable_switch.place(x=10,y=160)
combobox_switch.place(x=100,y=160)
r1.place(x=510, y=260)
r2.place(x=560, y=260)
text1.place(x=0, y=80)

# entry=Entry(tk,width=10)
# entry1=Entry(tk,width=10)
# entry2=Entry(tk,width=10)
# entry.pack()
# entry1.pack()
# entry2.pack()


tk.mainloop()


# def helloButton():
#     print('hello button')
# root = Tk()
# #通过command属性来指定Button的回调函数
# Button(root,text = 'Hello Button',command = helloButton).pack()
# root.mainloop()


# if __name__ == '__main__':
#     #for arg in sys.argv:
#     #    print(arg)
#     #print (sys.argv[1])
#     if(sys.argv[2]!=None):
#         toValue(sys.argv[1], sys.argv[2], sys.argv[3])
#     toGray(sys.argv[1])

# / *第一个参数，InputArray类型的src，输入数组，填单通道, 8
# 或32位浮点类型的Mat即可。
#
# 第二个参数，OutputArray类型的dst，函数调用后的运算结果存在这里，即这个参数用于存放输出结果，且和第一个参数中的Mat变量有一样的尺寸和类型。
#
# 第三个参数，double类型的thresh，阈值的具体值。
#
# 第四个参数，double类型的maxval，当第五个参数阈值类型type取
# THRESH_BINARY
# 或THRESH_BINARY_INV阈值类型时的最大值.
# 0: THRESH_BINARY 当前点值大于阈值时，取Maxval, 也就是第四个参数，下面再不说明，否则设置为0
#
# 1: THRESH_BINARY_INV  当前点值大于阈值时，设置为0，否则设置为Maxval
#
# 2: THRESH_TRUNC  当前点值大于阈值时，设置为阈值，否则不改变
#
# 3: THRESH_TOZERO  当前点值大于阈值时，不改变，否则设置为0
# 4: THRESH_TOZERO_INV   当前点值大于阈值时，设置为0，否则不改变 * /

# bt=tkinter.Button(root,text='button')
# bt.place(x=5,y=5)
# bt.place_forget()  #隐藏控件

def toValue():
    print(entry.get())
    print(entry1.get())
    print(entry2.get())
    thresh = 0
    maxval = 0
    # path = "D:\\APK\\tlbb\\app\\src\\main\\assets\png\\accumulativeOnline.png"
    print("path", path)
    img = cv2.imread(path, 0)
    print("thresh", int(thresh))
    print("maxval", int(maxval))
    cv2.imwrite("D:\\jingl\\newScript\\bin\\adb\\1.png", img)
    ret, thresh1 = cv2.threshold(img, int(entry.get()), int(entry1.get()), int(entry2.get()))
    cv2.imwrite("D:\\jingl\\newScript\\bin\\adb\\124.png", thresh1)
    '''
    #ret, thresh1 = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    print("ret=",thresh1)
    image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   # print ("---------------------------",contours)
    #cv2.drawContours(thresh1, contours, -1, (0, 0, 255), 3)
    print (len(contours))
    print (contours[0])
    for i in range(0, len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        print ("h=",h,"---w=",w)
       # cv2.rectangle(image, (x, y), (x + w, y + h), (153, 153, 0), 5)
        if h >=10 :
            newimage = image[y :y + h , x :x + w]  # 先用y确定高，再用x确定宽
            nrootdir = ("D:\\jingl\\newScript\\bin\\adb\\567-")

            cv2.imwrite(nrootdir + str(i) + ".png", newimage)
    print (i)
    '''
    print("---------------------------")
    cv2.imwrite("D:\\jingl\\newScript\\bin\\adb\\2.png", thresh1)
