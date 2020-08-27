# coding:utf-8
import requests
import base64
import time
import os

'''
身份证识别
'access_token': '24.e9119afec7af049024f055d3aae0ba2d.2592000.1600930177.282335-10766749'
# E:\PycharmProjects\IDCard\img\frontXYZ
'''

'''
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?' \
       'grant_type=client_credentials&client_id=KRBEoWjLgTuQkOZgf5ffGFrx&' \
       'client_secret=vhGzm0LSmnNu3jc1ETnAVUjKrGV9GZ7Y'
response = requests.get(host)
print(response)
if response:
    print(response.json())

'''
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"
access_token = '[24.e9119afec7af049024f055d3aae0ba2d.2592000.1600930177.282335-10766749]'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}


# 二进制方式打开图片文件
def bs64code(imgs):
    with open(imgs, 'rb') as f:
        bs64 = base64.b64encode(f.read())
    return bs64


def oneImgTest():
    s = time.time()

    img = bs64code(r'E:\PycharmProjects\IDCard\img\front\1.jpg')
    params = {"id_card_side": "front", "image": img}

    postnum = 1
    for i in range(postnum):
        print(i)
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())

    e = time.time()
    allTime = e - s
    avgTime = allTime / postnum
    print('allTime:%.4fs' % allTime,
          '\noneAvgTime:%.4fs' % avgTime)


def batchImgTest():
    sourceImgPath = r'E:\PycharmProjects\IDCard\img\front'
    allImg = os.listdir(sourceImgPath)
    imgPath = []
    for item in allImg:
        imgPath.append(os.path.join(sourceImgPath, item))

    s = time.time()

    postnum = 25
    for i in range(postnum):
        for one in imgPath:
            print(i, '---', one)
            img = bs64code(one)
            params = {"id_card_side": "front", "image": img}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                print(response.json())

    e = time.time()
    allTime = e - s
    avgTime = allTime / (len(imgPath) * postnum)
    print('allTime:%.4fs' % allTime,
          '\nbatchAvgTime:%.4fs' % avgTime)


if __name__ == '__main__':
    oneImgTest()
    # batchImgTest()
