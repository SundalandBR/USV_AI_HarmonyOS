import cv2
import os
import copy
import socket


# 获取摄像头
def capture_camera():
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()
    return cap


# 与推理模块交互部分与视频保存
def capture_video(frame_queue, enable):
    cap = capture_camera()
    # 参数
    running_time = 60   # 程序运行时间
    save_interval = 5   # 视频保存间隔
    image_count = 0     # 图片数量
    video_count = 1     # 视频数量
    list_count = 1      # 列表数量
    frame_interval = 0.2  # 抽帧间隔
    out_break = False      # 是否退出外层循环
    image_list = []        # 创建列表
    fps = cap.get(cv2.CAP_PROP_FPS)     # 视频帧率
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # 视频宽
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 视频高
    fourcc = cv2.VideoWriter_fourcc(*'XVID')                # 编码格式

    # 图片路径
    image_folder = "./demo_image"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    # 视频路径
    video_folder = "./demo_video"
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    image_start_time = cv2.getTickCount()   # 每个图片的开始时间
    video_start_time = cv2.getTickCount()   # 每个视频的开始时间
    list_start_time = cv2.getTickCount()    # 每一个数组的开始时间
    start_time = cv2.getTickCount()         # 整个任务的创建时间
    try:
        while enable.is_set():
            # 视频文件名
            output_video = os.path.join(video_folder, f'video_{video_count}.avi')
            # 创建视频对象
            out = cv2.VideoWriter(output_video, fourcc, fps, (video_width, video_height), isColor=True)
            if not out.isOpened():
                print("无法打开输出视频文件")
                cap.release()
                return

            while enable.is_set():
                # 获取帧
                ret, frame = cap.read()
                if not ret:
                    print("无法读取摄像头数据")
                    break

                # 获取当前时间
                current_time = cv2.getTickCount()

                # 控制推理模块读取的帧率
                if (current_time - image_start_time) / cv2.getTickFrequency() >= frame_interval:
                    image_list.append(frame)
                    image_start_time = current_time
                    image_count += 1
                    # 保存图片
                    # image_path = os.path.join(image_folder, f'image_{image_count}.jpg')
                    # cv2.imwrite(image_path, frame)

                # 将打包好的图片列表放入缓冲区
                if (current_time - list_start_time) / cv2.getTickFrequency() >= 1:
                    frame_queue.put(copy.deepcopy(image_list))
                    # print(f"capture:{list_count}")
                    list_count += 1
                    image_list.clear()
                    list_start_time = current_time

                # 保存视频
                # 将帧写入视频文件
                out.write(frame)
                elapsed_time = (current_time - start_time) / cv2.getTickFrequency()     # 程序已运行时间
                if elapsed_time >= running_time:
                    out_break = True
                    break

                if (current_time - video_start_time) / cv2.getTickFrequency() >= save_interval:
                    video_start_time = current_time
                    break

            out.release()
            video_count += 1
            if out_break:
                break
        print("capture_viedo processing exit")

    except KeyboardInterrupt:
        print("手动终止录制")
        exit()
    except Exception as e:
        print(f"发生错误：{str(e)}")
        exit()
    finally:
        cap.release()
        frame_queue.put(None)  # 发送结束信号
        # sys.exit(0)


# 视频推流
def video_upload(HOST, PORT):
    # HOST = '47.96.237.24'  # 服务端的主机名或 IP 地址
    # PORT = 5566  # 服务端监听的端口号
    cap = capture_camera()
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.connect((HOST, PORT))
        while True:
            ret, img1 = cap.read()
            if not ret:
                print("无法接收帧，请退出")
                break
            quality = 80
            while True:
                _, img_encoded = cv2.imencode('.jpg', img1, [int(cv2.IMWRITE_JPEG_QUALITY),quality])
                if (len(img_encoded.tobytes())) < 10240:
                    break
                else:
                    quality -= 5
            img_encoded = img_encoded.tobytes()
            print(len(img_encoded))
            client_socket.sendall(img_encoded)
