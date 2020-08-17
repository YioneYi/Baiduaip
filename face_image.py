# coding:utf-8
from aip import AipFace
import base64
import cv2
import numpy as np

APP_ID = '19535352'
API_KEY = '3GGqRFy2OPtDyVzZbuuxrbwV'
SECRET_KEY = 'hGQmC4stnXCnjw5Mw0naXbk9wwNWSFwS'


def bs64code(imgs):
    with open(imgs, 'rb') as fp:
        bs64_data = base64.b64encode(fp.read())
    img = str(bs64_data, "utf-8")
    return img


def faceDete(imgpath, imageType, options):
    img = bs64code(imgpath)

    # 人脸检测
    info = client.detect(img, imageType, options)
    print('info:', info)
    if info['error_msg'] == 'pic not has face':
        print('NoFace!')
    else:
        result = info['result']
        # print('result:', result)
        faceNum = result['face_num']
        print("faceNum:", faceNum)

        # 绘制边框
        image = cv2.imread(imgpath)
        for i in range(0, faceNum):
            location = result['face_list'][i]['location']
            print(location)
            left_top = (int(location['left']), int(location['top']))
            right_bottom = (left_top[0] + int(location['width']), left_top[1] + int(location['height']))
            cv2.rectangle(image, left_top, right_bottom, (0, 255, 0), 2)

        image = cv2.resize(image,(640,480))
        cv2.imshow('facedete', image)
        cv2.waitKey(0)


client = AipFace(APP_ID, API_KEY, SECRET_KEY)
options = {}
options['max_face_num'] = 10

imgpath = './images/3.jpg'
img_np = np.array(imgpath)
print('img_np:', img_np)
imageType = 'BASE64'
# for i in range(10):
#     print('times:', i)
faceDete(imgpath, imageType, options)
# time.sleep(3)
