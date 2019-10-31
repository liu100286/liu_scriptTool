


from win32api import GetSystemMetrics
import socket
import threading
import six
class lookLog(object):

    def __init__(self,mTk,mTtk,CN,IP):
        print('lookLog init',"mTk=",mTk,"mTtk=",mTtk,"CN=",CN,"IP=",IP)
        if len(str(IP))>5:
            IP=self.IpToPort(IP)
        self.tk=mTk
        self.ttk=mTtk
        self.CN=CN
        self.IP=IP
        self.threads = []
        t1 = threading.Thread(target=self.getLog)
        self.threads.append(t1)
        self.threads[0].setDaemon(True)
        self.log_Stop=True
        self.pause=False



    def getLog(self):
        print("getLog,CN=",self.CN,',IP=',self.IP)
        s = socket.socket()  # 创建 socket 对象
        aa = s.connect_ex((self.CN, 12400))
        # aa = s.connect_ex((self.CN, int(self.IP)))
        print('aa=',aa)
        sendIP=''
        if len(str(self.IP))==5:
            sendIP=self.PortToIp(self.IP)
        print(sendIP)
        # msg = b'000131134600061081111039997116'
        # if self.Checkbutton_all.get()==1:
        #
        #     msg = bytes([0, 0, 0, 13, 1, 13, 46, 0, 0, 0, 6, 108, 111, 103, 99, 97, 116])
        # else:
        if self.Checkbutton_all_state.get() == 1:
            msg = bytes([0, 0, 0, 13, 1, 13, 46, 0, 0, 0, 6, 108, 111, 103, 99, 97, 116])
        else:
            msg = bytes(
                [0, 0, 0, 24, 1, 13, 46, 0, 0, 0, 17, 108, 111, 103, 99, 97, 116, 32, 45, 99, 32, 59, 108,
                 111, 103, 99, 97, 116])
        # msg = bytes([0, 0, 0, 13, 1, 13, 46, 0, 0, 0, 6, 108, 111, 103, 99, 97, 116])
        # msg = bytes(
        #             [0, 0, 0, 24, 1, 13, 46, 0, 0, 0, 17, 108, 111, 103, 99, 97, 116, 32, 45, 99, 32, 59, 108,
        #              111, 103, 99, 97, 116])

        getDataIP = socket.inet_aton(sendIP)
        print(getDataIP,type(getDataIP))
        s.send(getDataIP)
        print('msg= ',msg)
        mSend = s.send(msg)

        while True:
            data = s.recv(1024)
            # print('--------------------', data.decode('utf8', 'ignore'))
            mStr=data.decode('utf8', 'ignore')
            s2 = mStr.split('\n')
            for s1 in s2:
                # print("+++++++++++++++",self.Checkbutton_yp_fairy_state.get(),',,,',s1.strip(),",",len(s1))
                # print(str(s1.strip()).find('yp_fairy'))
                if self.Checkbutton_yp_fairy_state.get() == 1:
                    mFilter='yp_fairy'
                elif self.Checkbutton_yp_fairy_state1.get() == 1:
                    mFilter='ypfairy'
                else:
                    mFilter=str(self.Entry_log_filter.get())

                if len(s1)>0:
                    print('len(s1):',len(s1))

                    if mFilter!='':
                        if str(s1.strip()).find(mFilter) > -1:
                            # self.Listbox_log.insert(self.tk.END, s1)
                            self.add_log_ListBox(s1)
                    else:
                        self.add_log_ListBox(s1)
                        # self.Listbox_log.insert(self.tk.END, s1)


                if self.pause==False:
                    self.Listbox_log.yview_moveto(1.0)


            # print('--------------------', str(data.decode('utf8', 'ignore')).strip())
            if self.log_Stop==True:
                print("stop")
                aa.close()
                break

    def add_log_ListBox(self,log_str):
        max_len=300
        print('log_str:',log_str)
        for i in range(0,len(log_str),max_len):
            print(log_str[i:i+max_len])
            print_str=log_str[i:i+max_len]
            self.Listbox_log.insert(self.tk.END, print_str)




    def stopLog(self):
        print('stopLog')
        # self.threads[0]._Thread__stop()

        # self.threads[0].start()
        self.log_Stop=True
        self.threads[0].join(1)
        print("stopLog-stop")


    def startLog(self):
        print('startLog')
        if self.log_Stop==False:
            return
        self.threads = []
        t1 = threading.Thread(target=self.getLog)
        self.threads.append(t1)
        self.threads[0].setDaemon(True)
        self.threads[0].start()
        self.log_Stop=False

    def IpToPort(self, mIP):
        print('IPtoPort')
        ip = mIP.split('.')
        print(ip)
        x = 12400 + (int(ip[2])) * 255 + (int(ip[3]))
        print('x=', x)
        return x

    def PortToIp(self,mPort):
        print('PortToIp')
        x = int(mPort) - 12400
        ip2 = int(x / 255)
        ip3 = x % 255
        print('ip2=', ip2, ',ip3=', ip3)
        return "192.168." + str(ip2) + '.' + str(ip3)



    def save_Log(self):
        f=open('logtet.log','ab+')

        for i in range(10):
            x = ("-------------------------------------------------------------------" + '\n').encode('UTF-8')
            f.write(x)
        for ss in self.Listbox_log.get(2,self.tk.END):
            x =(ss + '\n').encode('UTF-8')
            print(x)
            f.write(x)
            # f.write('\n')
        f.close()

    def pause_log(self):
        print('pause_log')

        if self.pause==False:
            self.pause = True
            self.Button_strvar.set('继续')
        elif self.pause==True:
            self.pause = False
            self.Button_strvar.set('暂停')

    def mLookLog(self):
        self.mWindow1 = self.tk.Toplevel()
        self.mWindow1.title(str(self.CN) + ":" + str(self.IP))
        self.mWindow1.geometry(str(GetSystemMetrics(0)-100) + 'x' + str(GetSystemMetrics(1)-100) + '+0+0')
        print("w=",self.mWindow1.winfo_width())
        # frame = self.tk.Frame(self.mWindow1, width=100)
        # frame.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_log =self.tk.Scrollbar(self.mWindow1)

        scrollbar_log.pack(side=self.tk.RIGHT, fill=self.tk.Y,anchor=self.tk.N)
        self.Listbox_log=self.tk.Listbox(self.mWindow1,width=self.mWindow1.winfo_width()-5,yscrollcommand=scrollbar_log.set,bg="#303030",fg="white")
        # ck1 = self.tk.Checkbutton(self.mWindow1, text='游泳')
        # ck1.pack(anchor=self.tk.E)
        self.frame1 = self.tk.Frame(self.mWindow1)
        self.frame1.pack(side=self.tk.RIGHT, fill=self.tk.X,anchor=self.tk.N)
        self.Listbox_log.pack(side=self.tk.LEFT,expand=self.tk.YES,fill=self.tk.BOTH,anchor=self.tk.E)
        scrollbar_log.config(command=self.Listbox_log.yview)
        self.button_start=self.tk.Button(self.frame1, text="开始", width=8, height=1, command=self.startLog)
        self.button_start.pack(side=self.tk.TOP)
        self.button_stop=self.tk.Button(self.frame1, text="停止", width=8, height=1, command=self.stopLog)
        self.button_stop.pack(side=self.tk.TOP)
        self.Button_strvar = self.tk.StringVar()
        self.Button_strvar.set("暂停")
        self.button_pause=self.tk.Button(self.frame1, textvariable=self.Button_strvar, width=8, height=1, command=self.pause_log)
        self.button_pause.pack(side=self.tk.TOP)
        self.button_log_save=self.tk.Button(self.frame1, text="保存", width=8, height=1, command=self.save_Log)
        self.button_log_save.pack(side=self.tk.TOP)

        self.Checkbutton_yp_fairy_state = self.tk.IntVar()
        self.Checkbutton_yp_fairy=self.tk.Checkbutton(self.frame1,text='yp_fairy',variable=self.Checkbutton_yp_fairy_state)
        self.Checkbutton_yp_fairy.pack(side=self.tk.TOP)

        self.Checkbutton_yp_fairy_state1 = self.tk.IntVar()
        self.Checkbutton_yp_fairy1=self.tk.Checkbutton(self.frame1,text='ypfairy',variable=self.Checkbutton_yp_fairy_state1)
        self.Checkbutton_yp_fairy1.pack(side=self.tk.TOP)

        self.Checkbutton_all_state=self.tk.IntVar()
        self.Checkbutton_all=self.tk.Checkbutton(self.frame1,text='current',variable=self.Checkbutton_all_state)
        self.Checkbutton_all.pack(side=self.tk.TOP)


        self.frame1_frame = self.tk.Frame(self.frame1,width=1, height=1)
        self.frame1_frame.pack(side=self.tk.TOP)

        self.tk.Label(self.frame1_frame, text="指定关键字", width=8, height=1).pack(side=self.tk.LEFT)

        self.Entry_log_filter=self.tk.Entry(self.frame1_frame, width=10)
        self.Entry_log_filter.pack(side=self.tk.RIGHT)

        self.Entry_log_search=self.tk.Entry(self.frame1)
        self.Entry_log_search.pack(side=self.tk.TOP)

        self.button_log_search=self.tk.Button(self.frame1, text="搜索", width=8, height=1, command=self.save_Log)
        self.button_log_search.pack(side=self.tk.TOP)


        # self.getLog()
        # for i in range(10000):
        #     entry_log.insert(0,str(i))

def getByte():
    global wri
    global time1
    global frameList
    global bydata1
    global RecordI
    global mOpen
    global currentImg
    global lock
    f = open('D:\\jingl\\newScript\\py\\11.h264', 'wb+')
    k=0
    print('-------------getbyte')
    # ss=bytes([])
    # for i in range(1000):
    ReceivingLength=0
    FrontData=bytes
    tou=bytes

    testdata=bytearray([])
    while True:
        data = s.recv(2097152)
        print("data=",data)
        if ReceivingLength>0:
            mData=bytearray([])
            mData[0:len(FrontData)]=FrontData
            mData[len(FrontData):len(data)+len(FrontData)]=data
            data=bytes(mData)
        while len(data)>0:
            ReceivingLength=bytesToInt(data[0:4],0)
            print(ReceivingLength,"--",data[16:ReceivingLength+4])
            if len(data[4:len(data)])>=ReceivingLength:
                if bytesToShort(data[4:6],0)==769:
                    f.write(data[16:ReceivingLength + 4])
                    data=data[ReceivingLength+4:len(data)]
                else:
                    data=data[4+ReceivingLength:len(data)]
                if len(data)==0:
                    ReceivingLength=0
                    break
            else:
                FrontData=data
                break

        if int(time.time()) - time1 >= 2:
            # f.close()
            # return
            time1 = int(time.time())
            s.send(bytes([0, 0, 0, 2, 0, 5]))


if __name__ == '__main__':
    import tkinter as tk  # imports

    from tkinter import ttk
    import time
    import struct
    import cv2

    import tkinter.filedialog
    Obj= lookLog(tk,ttk,'cncz48.padyun.cn',13203)



    Obj.mLookLog()



    # Obj.threads[0].setDaemon(True)

    # Obj.threads[0].start()
    Obj.mWindow1.mainloop()
    # Obj.getLog()

























