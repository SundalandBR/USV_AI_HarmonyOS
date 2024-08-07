import cv2
import os
import copy
import socket
import shutil
import configparser
from threading import Thread
import time

# 获取摄像头
def capture_camera():
    # 打开默认摄像头
    cap = cv2.VideoCapture(-1)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return None
    return cap


# 计算文件夹大小
def get_folder_size(folder_path):
    total_size = 0
    # 遍历目标目录
    for dir_path, _, filenames in os.walk(folder_path):  # dir_path:正在遍历的目录路径  _:子目录列表  filenames:文件列表
        # 遍历文件
        for file in filenames:
            file_path = os.path.join(dir_path, file)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


# 清空文件夹
def clear_folder_contents(folder_path):
    # 遍历目标目录
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # 删除文件或符号链接
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # 删除文件夹
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'文件{file_path}删除失败，原因:{e}')


# 与推理模块交互部分与视频保存
def capture_video(frame_queue, enable):
    cap = capture_camera()
    # 参数
    index = 1           # 当前使用的文件夹编号
    running_time = 600   # 程序运行时间
    save_interval = 60   # 视频保存间隔
    image_count = 0     # 图片数量
    video_count = 1     # 视频数量
    list_count = 1      # 列表数量
    frame_interval = 1  # 抽帧间隔
    # out_break = False      # 是否退出外层循环
    #tframe_queue = queue.Queue(1)     #线程帧队列
    #vedio_thread = Thread(target=video_upload,args=(tframe_queue,))
    image_list = []        # 创建列表
    save_limit = 400 * 1024 * 1024    # 视频保存上限(MB)
    fps = cap.get(cv2.CAP_PROP_FPS)     # 视频帧率
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # 视频宽
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 视频高
    fourcc = cv2.VideoWriter_fourcc(*'XVID')                # 编码格式
    # 图片路径
    image_folder = "./demo_image"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    # 视频路径
    video_folder1 = "./demo_video1"
    if not os.path.exists(video_folder1):
        os.makedirs(video_folder1)
    video_folder2 = "./demo_video2"
    if not os.path.exists(video_folder2):
        os.makedirs(video_folder2)
    video_folder = video_folder1        # 默认使用文件夹1

    image_start_time = cv2.getTickCount()   # 每个图片的开始时间
    video_start_time = cv2.getTickCount()   # 每个视频的开始时间
    list_start_time = cv2.getTickCount()    # 每个数组的开始时间
    start_time = cv2.getTickCount()         # 整个任务的创建时间
    try:
        #vedio_thread.start() #启动推流线程
        while enable.is_set():
            # 检查当前视频文件夹大小
            if get_folder_size(video_folder) >= save_limit:
                # 当前路径为文件夹1
                if index == 1:
                    clear_folder_contents(video_folder2)
                    video_folder = video_folder2
                    index = 2
                # 当前路径为文件夹2
                else:
                    clear_folder_contents(video_folder1)
                    video_folder = video_folder1
                    index = 1

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
                #tframe_queue.put(copy.deepcopy(frame))
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
                    #frame_queue_event.set()
                    # print(f"capture:{list_count}")
                    list_count += 1
                    image_list.clear()
                    list_start_time = current_time

                # 保存视频
                # 将帧写入视频文件
                out.write(frame)
                elapsed_time = (current_time - start_time) / cv2.getTickFrequency()     # 程序已运行时间
                if elapsed_time >= running_time:
                    # out_break = True
                    enable.clear()
                    break

                if (current_time - video_start_time) / cv2.getTickFrequency() >= save_interval:
                    video_start_time = current_time
                    break

            out.release()
            video_count += 1
            # print(get_folder_size(video_folder))
            # if out_break:
            #     break
        print("capture_viedo processing exit")
        #vedio_thread.join()
        print("vedio_thread_exit")

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
def video_upload(frame_queue,HOST = None,PORT=None):
    # HOST = '47.96.237.24'  # 服务端的主机名或 IP 地址
    # PORT = 5566  # 服务端监听的端口号
    # cap = capture_camera()
    # if not cap.isOpened():
    #     print("无法打开摄像头")
    #     exit()
    config = configparser.ConfigParser()
    config.read('./config.ini')
    HOST = config.get('VIDEO', 'HOST')
    PORT = config.getint('VIDEO', 'PORT')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.connect((HOST, PORT))

        while True:
            if not frame_queue.empty():
                img1 = frame_queue.get()
            else:
                continue
            quality = 30
            t1 = time.time()
            cnt = 0
            while True:
                cnt = cnt + 1
                _, img_encoded = cv2.imencode('.jpg', img1, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                if (len(img_encoded.tobytes())) < 20480:
                    break
                else:
                    quality -= 5
            #print("qua",time.time()-t1,quality,cnt)
            img_encoded = img_encoded.tobytes()
            t2 = time.time()
            #print("encoded",len(img_encoded))
            client_socket.sendall(img_encoded)
            #print("send",time.time()-t2)
