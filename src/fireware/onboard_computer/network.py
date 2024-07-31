import socket
import time
import cv2
import numpy as np
import http

# 定义主机和端口
HOST = '47.96.237.24'  # 服务端的主机名或 IP 地址
PORT = 5566  # 服务端监听的端口号
cap = cv2.VideoCapture(0)  # 0 通常是默认摄像头的标识
if not cap.isOpened():
    print("无法打开摄像头")
    exit()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.connect((HOST, PORT))
    while 1:
        ret, img1 = cap.read()
        if not ret:
            print("无法接收帧，请退出")
            break
        quality=80
        while 1:
            _, img_encoded = cv2.imencode('.jpg', img1,[int(cv2.IMWRITE_JPEG_QUALITY),quality])
            if (len(img_encoded.tobytes()))<10240:
                break
            else:
                quality-=5
        img_encoded=img_encoded.tobytes()
        print(len(img_encoded))
        client_socket.sendall(img_encoded)
       # time.sleep(0.01)
