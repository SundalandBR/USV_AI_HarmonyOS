import cv2
import os
import time


def capture_video():
    # 打开默认摄像头
    cap = cv2.VideoCapture(1)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("Failed to turn on the camera")
        exit()

    # 保存的图片路径
    image_folder = "C:/Users/dell/Desktop/image"
    # 创建文件夹
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    # 图片计数
    count = 0

    # 视频
    video_folder = "C:/Users/dell/Desktop/video"
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    try:
        start_time = time.time()
        while True:
            # 读取摄像头的一帧图像
            ret, frame = cap.read()

            # 检查是否成功读取帧
            if not ret:
                print("C:/Users/dell/Desktop/video")
                break

            # 显示图像
            cv2.imshow('Video Stream', frame)
            # 构造保存的文件名
            filename = os.path.join(image_folder, f'image_{count:04d}.jpg')
            # 将文件添加到目录
            cv2.imwrite(filename, frame)
            # 计数器 + 1
            count += 1

            # 按 'q' 键退出
            if cv2.waitKey(40) & 0xFF == ord('q'):
                end_time = time.time()
                break

    finally:
        time1 = end_time - start_time
        print(time1)
        print(count/time1)
        # 释放摄像头资源
        cap.release()
        # 关闭所有OpenCV窗口
        cv2.destroyAllWindows()


if __name__ == '__main__':
    capture_video()










