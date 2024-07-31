import cv2
import os
import copy
import time
import socket

def capture_video(frame_queue, enable, lock, frame_queue_event):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    frame_rate = 24
    save_interval = 60
    frames_to_skip = 2
    save_frame_count = frames_to_skip
    frame_count = 0
    frame_to_collect = 24
    frame_matrix = []
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    output_folder = "./demo_image"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_video_path = os.path.join(output_folder, "demo_video.avi")
    out = cv2.VideoWriter(
        output_video_path, fourcc, frame_rate, (video_width, video_height)
    )

    if not out.isOpened():
        print("无法打开输出视频文件")
        cap.release()
        return

    start_time = cv2.getTickCount()
    try:
        while enable.is_set():
            ret, frame = cap.read()
            if not ret:
                print("无法读取摄像头数据")
                break
            frame_count += 1
            frame_matrix.append(frame)
            current_time = cv2.getTickCount()
            if (current_time - start_time) / cv2.getTickFrequency() >= 1:
                frame_queue.put(copy.deepcopy(frame_matrix))
                frame_queue_event.set()
                frame_matrix.clear()
                start_time = current_time
            # if not frame_queue.full():
            #     # buffer.append(frame)
            #     frame_queue.put(frame)
            if frame_count >= save_frame_count:
                image_path = os.path.join(
                    output_folder, f"demo_image_{frame_count // frames_to_skip}.jpg"
                )
                cv2.imwrite(image_path, frame)
                save_frame_count += frames_to_skip
            out.write(frame)
            time.sleep(0.2)
            # current_time = cv2.getTickCount()
            # elapsed_time = (current_time - start_time) / cv2.getTickFrequency()
            # if elapsed_time >= save_interval:
            #     break
        print("capture_viedo processing exit")
    except KeyboardInterrupt:
        print("手动终止录制")
    except Exception as e:
        print(f"发生错误：{str(e)}")
    finally:
        cap.release()
        out.release()


def video_upload(cap,HOST,PORT):
    # HOST = '47.96.237.24'  # 服务端的主机名或 IP 地址
    # PORT = 5566  # 服务端监听的端口号
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