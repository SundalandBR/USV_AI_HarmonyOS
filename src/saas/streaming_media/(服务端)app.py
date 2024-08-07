from flask import Flask, render_template, Response
import cv2
import numpy as np
import socket

app = Flask(__name__)


HOST = '0.0.0.0' 
PORT = 5566 


def video_stream():
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (HOST, PORT)
    buffer_size =20480#10
    udp_server_socket.bind(server_address)


    global data_buffer

    while True:
        data, client_address = udp_server_socket.recvfrom(buffer_size)
            
        if len(data)==0:
            continue
            
                     
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
           
def text_stream():
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (HOST, PORT+1)
    udp_server_socket.bind(server_address)
    while 1:
        data, client_address = udp_server_socket.recvfrom(1024)
        if len(data)==0:
            return "0"
        data=data.decode('utf-8')
        return data#每次访问都发送一个
        
        

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text_feed')
def text_feed():
    response = Response(text_stream())
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
