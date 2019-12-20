import tensorflow as tf
import numpy as np
import cv2
import sys
sys.path.append('./model')
from pixel_link_decode import decode_image_by_join,mask_to_bboxes
import requests
import base64
import json
import hashlib
import time



##文本检测
class TextDetection():

    def __init__(self):
        print('__init__')
        self.img_data=None
        self.pixel_pos_scores=None
        self.link_pos_scores=None
        self.sess=None
        self.load_model()
        self.image=None
        self.bboxes=[]



    def load_model(self):
        # 导入 并准备好模型
        print('======load_model======')
        pb_file_path = r'./model/pixel_link_test.pb'
        self.sess = tf.Session()
        with tf.io.gfile.GFile(pb_file_path, 'rb') as f:

            graph_def = tf.compat.v1.GraphDef()

            graph_def.ParseFromString(f.read())
            print('======load_model======')
            self.sess.graph.as_default()
            tf.import_graph_def(graph_def, name='')  # 导入计算图

            self.img_data = self.sess.graph.get_tensor_by_name('test/Placeholder:0')

            self.pixel_pos_scores = self.sess.graph.get_tensor_by_name('test/strided_slice_3:0')

            self.link_pos_scores = self.sess.graph.get_tensor_by_name('test/strided_slice_4:0')
        print('======load_model======')


    def get_bboxes(self):
        # 获取传入图片有文字的范围
        print('get_bboxes')
        feed_dict={self.img_data:self.image}
        pixel_pos_scores, link_pos_scores = self.sess.run([self.pixel_pos_scores, self.link_pos_scores, ], feed_dict)
        mask = self.decode_batch(pixel_pos_scores, link_pos_scores)
        bboxes = mask_to_bboxes(mask, self.image.shape)
        # self.bboxes=bboxes
        for range_ in bboxes:
            x_list = [range_[0], range_[2], range_[4], range_[6]]
            y_list = [range_[1], range_[3], range_[5], range_[7]]
            self.bboxes.append([min(x_list),min(y_list),max(x_list),max(y_list)])
        print('self.bboxes  ', self.bboxes)
        return self.bboxes

    # 获取检测到的文本图片
    def get_text_list(self):
        image_list=[]
        for range_ in self.bboxes:
            print(range_)
            img=self.image[range_[1]:range_[3],range_[0]:range_[2]]
            image_list.append(img)
            # cv2.imshow("1",img)
            # cv2.waitKey(0)
        return image_list


    def get_draw(self):
        # 获取绘制好文字区域的图片
        print('get_draw')
        bboxes=self.bboxes
        for range_ in bboxes:
            print(range_)
            pts = np.array(
                [[range_[0], range_[1]], [range_[2], range_[3]], [range_[4], range_[5]], [range_[6], range_[7]]],
                np.int32)
            pts = pts.reshape((-1, 1, 2))
            print(pts)
            cv2.polylines(self.image, [pts], True, (0, 255, 255))

        # cv2.imshow('11',self.image)
        # cv2.waitKey(0)


    def decode_batch(self,pixel_cls_scores, pixel_link_scores,pixel_conf_threshold=None, link_conf_threshold=None):
        if pixel_conf_threshold is None:
            pixel_conf_threshold = 0.8
        if link_conf_threshold is None:
            link_conf_threshold = 0.8
        batch_size = pixel_cls_scores.shape[0]

        print(pixel_cls_scores.shape)
        print(pixel_link_scores.shape)
        print('batch_size : ', batch_size)
        batch_mask = []

        image_pos_pixel_scores = pixel_cls_scores[0]
        image_pos_link_scores = pixel_link_scores[0]

        mask =  decode_image_by_join(image_pos_pixel_scores, image_pos_link_scores,pixel_conf_threshold, link_conf_threshold)
        return mask

##文字识别
class TextDistinguish():

    def __init__(self):
        print('__init__')


    def getToken(self):
        #百度 token获取
        url = 'https://aip.baidubce.com/oauth/2.0/token'
        d = {'grant_type': 'client_credentials', 'client_id': 'mXrHgVFw9IhqkZdAs2qSmOKt',
             'client_secret': 'hHK5Icl1D2LXa97G8XF7vA6KYp5eSfWG'}
        h={'Content-Type', 'application/json; charset=UTF-8'}
        r = requests.post(url, data=d,json=h)
        text=json.loads(r.text)
        self.token =text['access_token']
        return self.token

    def getSignJD(self,secretkey):
        #京东 sign获取
        m = hashlib.md5()
        nowTime = int(time.time() * 1000)
        before = secretkey + str(nowTime)
        m.update(before.encode('utf8'))
        return nowTime, m.hexdigest()




    def imageToBase64(self,img):
        # cv2.imshow("test",img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img_str = cv2.imencode('.png', img)[1].tostring()  # 将图片编码成流数据，放到内存缓存中，然后转化成string格式
        b64_code = base64.b64encode(img_str)  # 编码成base64
        self.img_base64=b64_code
        return b64_code

    #京东识别
    def send_JD(self):
        params={"appkey":"24174a238be0dbcb5d458d7ac6656dc4"}
        params['timestamp'],params['sign']=self.getSignJD('698e0ff31172be46764dc1954e8eb977')
        print(params)
        url='https://aiapi.jd.com/jdai/ocr_universal_v2'
        print(str(self.img_base64,'utf-8'))

        data='{"imageBase64Str":"' + str(self.img_base64,'utf-8') + "\"}'"
        print(data)

        r = requests.post(url, params=params, data=data)

        try:
            text=json.loads(r.text)
            print(text)
            return text
        except :
            print(' ====    return error   ==== ')
            return ""



    # 百度识别
    def send(self):
        self.getToken()
        list=[]
         #    'https://aip.baidubce.com/rest/2.0/ocr/v1/general'
        url='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + self.token # 通用文字识别
        # url='https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' +  self.token # 通用文字识别高精度版
        # url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=' + self.token  # 通用文字识别，高精度版，含位置信息
        # url= 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + self.token # 通用文字识别,含位置信息
        h={'Content-Type', 'application/x-www-form-urlencoded'}
        d = {'image': self.img_base64}
        r = requests.post(url, data=d, json=h)
        try :
            text = json.loads(r.text)
        except:
            print(' ====    return error   ==== ')
            return ""
        print(r.text)
        print(text)
        try :
            if text['error_msg']:
                return ""
        except :
            print(' ====    error_msg   ==== ')
            pass

        if int(text['words_result_num'])==0:
            return ""

        print(text['words_result'])
        print(text['words_result'][0])

        text=text['words_result'][0]['words']

        print(text)

        return text



if __name__ == '__main__':
    import re
    Obj=TextDistinguish()
    img=cv2.imread(r'D:\jingl\newScript\py\dist\tlbb\6.png')
    timex=time.time()
    Obj.imageToBase64(img)
    json_str=Obj.send_JD()

    patten="'选择', 'location': {'x': (\d+), 'y': (\d+), 'width': (\d+), 'height': (\d+)}"
    match=re.search(patten,str(json_str))
    print(match)
    print(match.group(0))
    print(match.group(1))
    print(match.group(2))
    print(match.group(3))
    print(match.group(4))
    # Obj.image =img
    # Obj.get_bboxes()
    #
    # img_list=Obj.get_text_list()

    # textDistinguish = TextDistinguish()
    # textDistinguish.imageToBase64(img)
    # textDistinguish.send()
    # for img in img_list:
    #     textDistinguish.imageToBase64(img)
    #     textDistinguish.send()


