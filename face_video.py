# coding:utf-8
from aip import AipFace
import cv2
import base64
from PIL import Image
from io import BytesIO

APP_ID = 'xxx'
API_KEY = 'xxx'
SECRET_KEY = 'xxx'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def bs64code(frame):
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    bs64_data = base64.b64encode(byte_data)  # 转为BASE64
    img = str(bs64_data, "utf-8")
    return img


def faceDete(imageType, options):
    # times = 0
    capture = cv2.VideoCapture('rtsp://admin:dnY1230456@10.206.148.179:554/Streaming/Channels/101')
    fps = capture.get(cv2.CAP_PROP_FPS)
    print('fps:', fps)
    while True:
        ret, frame = capture.read()
        img = bs64code(frame)
        print(frame.shape[1])
        # if (times % (fps) == 0):
        # 人脸检测
        info = client.detect(img, imageType, options)
        print('info:', info)
        if info['error_msg'] == 'pic not has face':
            print('pic not has face!')
            # cv2.imshow('frame', frame)
            pass
        else:
            result = info['result']
            # print('result:', result)
            if (result['face_list'][0]['face_probability'] > 0.99):
                faceNum = result['face_num']
                print("faceNum:", faceNum)

                # 绘制边框
                for i in range(0, faceNum):
                    location = result['face_list'][i]['location']
                    print(location)
                    # if (frame.shape[1] / 16 <= max(int(result['face_list']['location']['width']),
                    #                                int(result['face_list']['location']['height']))):
                    left_top = (int(location['left']), int(location['top']))
                    right_bottom = (left_top[0] + int(location['width']), left_top[1] + int(location['height']))
                    cv2.rectangle(frame, left_top, right_bottom, (255, 0, 0), 2)

        frame = cv2.resize(frame, (640, 480))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # times += 1

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    imageType = 'BASE64'
    options = {}
    options['max_face_num'] = 10

    faceDete(imageType, options)
