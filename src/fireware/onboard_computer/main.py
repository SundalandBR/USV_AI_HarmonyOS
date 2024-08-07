import model
import multiprocessing as mp
import time
from capture_video1 import capture_video
import logging
from data_processor import DataProcessor
from mavlink_interface import MAVLinkCommunicator
import socket
import json
import ctypes
import os
import configparser
import logging

    

class message:
    # 1 seg  2 action direction
    def __init__(
        self,
        enum=0,
        seq=None,
        direction=None,
        action=None,
        inference_action=[0, 0, 0, 0],
    ) -> None:
        self.enum = enum
        self.seq = seq
        self.direction = direction
        self.action = action
        self.inference_action = inference_action


def px4_read(
    communicator,
    _PX4_COMMUNICATION_ENABLE,
    _IS_MISSION_ARRIVAL,
    _IS_TARGET,
    _IS_ALIVE,
    _IS_MOVEING,
    _WATER_Quality,
):
    processor = DataProcessor()
    while True:
        if communicator.connect_and_check_communication():
            _PX4_COMMUNICATION_ENABLE = True
            communicator.receive_and_parse_messages_from_px4(processor)
            _is_mission_arrival = processor.is_mission_arrival
            _is_target = processor.is_target
            _is_alive = processor.is_alive
            _is_moving = processor.is_moving
            _WATER_Quality = processor.water_quality
        else:
            _PX4_COMMUNICATION_ENABLE = False


def water_quality(_ENABLE, seq, event, px4_write_event, message_queue):
    mes = message(seq=None, action=0, direction=-1, enum=2)
    message_queue.qut(mes)
    px4_write_event.set()
    # 采集
    time.sleep(10)
    mes = message(seq=seq, enum=1)


def px4_write(communicator, _ENABLE, message_queue):
    # action 0悬停 1前进 2后退
    # direction 0左转 1右转 other不做操作
    # enum 1任务 2行动
    while _ENABLE.is_set():
        if not message_queue.empty():
            message = message_queue.get()
            message_enum = message.message_enum
            seq = message.seq
            action = message.action
            direction = message.direction
            if message_enum == 1:
                communicator.send_mission_messages_px4(seq)
            elif message_enum == 2:
                communicator.send_move_messages_to_px4(action, direction)


def Inference_seg(frame_queue, inference_message_queue, _ENABLE, frame_queue_event):

    config = configparser.ConfigParser()
    config.read('config.ini')
    model_path = config.get('MODEL', 'model')
    seg = config.getboolean('MODEL', 'seg')
    # cc2inference
    # 0 left,1 right,2 up,3 down
    inference_model = model.model(model_path)
    while _ENABLE.is_set():
        ctrl = [0, 0, 0, 0]
        if not frame_queue.empty():
            imgs = frame_queue.get()
            for img in imgs:
                t = time.time()
                result = inference_model.inference_seg(img=img)
                print("Inference : Time", time.time() - t)
                preds = result.pred
                if preds.shape[0]:
                    for pred in preds:
                        shape = result.orig_shape
                        label = pred[5]
                        boxs = pred[:4]
                        if label == 0:
                            print("Inference : obstacle!")
                            mid_w = (boxs[2] - boxs[0]) / 2
                            orig_mid_w = shape[1] / 2
                            if mid_w < orig_mid_w:
                                # turn right
                                ctrl[1] += 1
                            if mid_w >= orig_mid_w:
                                # turn left
                                ctrl[0] += 1
                        if label == 1:
                            print("Inference : river!")
                            orig_mid_h = shape[0] / 2
                            h = (boxs[3] - boxs[1]) / 2
                            if h > orig_mid_h:
                                ctrl[2] += 1
                            if h <= orig_mid_h:
                                ctrl[3] += 1
                    inference_message_queue.put(ctrl)
                else:
                    print("Inference : No obstacles and river!!!!!")
        else:
            print("Inference : frame_queue is empty!!")
            time.sleep(0.1)
    print("Inference : Inference process exit")


def queue_clear(process, queue):
    while process.is_alive():
        if not queue.empty():
            queue.get()


def sound_moudle(_ENABLE, sound_queue):
    while True:
        instruction = "play "
        path = "sound/"
        mav_file = ""
        if not sound_queue.empty():
            num = sound_queue.get()
            mav_file = ""
            if num == 1:
                # 前方发现障碍物,自动导航系统已重新规划航线，避开障碍。
                mav_file = "findObstacle_check.mav"
            elif num == 2:
                # 无人艇自动返航开始。
                mav_file = "overReturnVoyage_checks.mav"
            elif num == 3:
                # 障碍物已避开，恢复原定航线。
                mav_file = "returnOriginalRoute.mav"
            elif num == 4:
                # 无人艇关机失败，请检查。
                mav_file = "shutDown_checks_error.mav"
            elif num == 5:
                # 无人艇关机成功。
                mav_file = "shutDown_checks.mav"
            elif num == 6:
                # 无人艇正在关机。
                mav_file = "shutDowning_checks.mav"
            elif num == 7:
                # 无人艇自动返航开始。
                mav_file = "startReturnVoyage_checks.mav"
            elif num == 8:
                # 无人艇启动失败，请检查。
                mav_file = "startUp_checks_error.mav"
            elif num == 9:
                # 无人艇启动成功开始航行。
                mav_file = "startUp_checks.mav"
            elif num == 10:
                # 自动导航系统已停止，转为手动控制。
                mav_file = "voyageTypeChange_check.mav"
            elif num == 11:
                # water_quality
                mav_file = "water_quality.mav"
            os.system(instruction + path + mav_file)


def travel_control(
    _ENABLE,
    px4_write_message_queue,
    _IS_MISSION_ARRIVAL,
    _IS_TARGET,
    _IS_ALIVE,
    _IS_MOVEING,
    _WATER_Quality,
    inference_message_queue,
    sound_queue,
):
    while _ENABLE.is_set():
        if _IS_MISSION_ARRIVAL.value and _WATER_Quality.value:
            # 水质检测
            sound_queue.qut(11)
            wmeg = message(enum=2, action=0, direction=-1)
            water_quality()
            px4_write_message_queue.qut(wmeg)
        elif not inference_message_queue.empty():
            sound_queue.qut(1)
            mes = inference_message_queue.get()
            result = mes.inference_action
            if result[0] >= result[1]:
                direction = 0
            else:
                direction = 1
            if result[2] >= result[3]:
                action = 1
            else:
                action = 2
            wmeg = message(enum=2, action=action, direction=direction)
            px4_write_message_queue.qut(wmeg)


if __name__ == "__main__":
    # init
    communicator = MAVLinkCommunicator()
    _PX4_COMMUNICATION_ENABLE = mp.Manager().Value(
        ctypes.c_bool, False
    )  # px4是否正常通讯
    _OPEN = mp.Manager().Value(ctypes.c_bool, True)
    _IS_MISSION_ARRIVAL = mp.Manager().Value(ctypes.c_bool, False)  # 任务目标点是否到达
    _IS_TARGET = mp.Manager().Value(ctypes.c_bool, False)  # 是否有航点
    _IS_ALIVE = mp.Manager().Value(ctypes.c_bool, False)  # 是否武装模块
    _IS_MOVEING = mp.Manager().Value(ctypes.c_bool, False)  # 是否在移动中
    _WATER_Quality = mp.Manager().Value(ctypes.c_bool, False)
    sound_queue = mp.Queue()  # 播报队列
    frame_queue = mp.Queue()  # 摄像头-推理 图片队列
    px4_write_message_queue = mp.Queue()  # 航控-px4写 message类队列
    inference_message_queue = mp.Queue()  # 推理-航控 避障信息队列
    _ENABLE = mp.Event()  # 摄像头-推理-航控-px4写-语音 模块启动-执行信号
    sound_moudle_process = mp.Process(target=sound_moudle, args=(_ENABLE, sound_queue))
    px4_read_process = mp.Process(
        target=px4_read,
        args=(
            communicator,
            _PX4_COMMUNICATION_ENABLE,
            _IS_MISSION_ARRIVAL,
            _IS_TARGET,
            _IS_ALIVE,
            _IS_MOVEING,
            _WATER_Quality,
        ),
    )
    px4_write_process = mp.Process(
        target=px4_write, args=(communicator, _ENABLE, px4_write_message_queue)
    )
    capture_process = mp.Process(target=capture_video, args=(frame_queue, _ENABLE))
    inference_seg_process = mp.Process(
        target=Inference_seg,
        args=(frame_queue, inference_message_queue, _ENABLE),
    )
    travel_control_process = mp.Process(
        target=travel_control,
        args=(
            _ENABLE,
            px4_write_message_queue,
            _IS_MISSION_ARRIVAL,
            _IS_TARGET,
            _IS_ALIVE,
            _IS_MOVEING,
            _WATER_Quality,
            inference_message_queue,
            sound_queue,
        ),
    )
    # init
    px4_read_process.start()
    sound_moudle_process.start()
    start = time.time()
    while not _PX4_COMMUNICATION_ENABLE.value:
        print("_PX4_COMMUNICATION_ENABLE", _PX4_COMMUNICATION_ENABLE.value)
        if time.time() - start > 30:
            print("_PX4_COMMUNICATION_ENABLE ERROR!!!")
            px4_read_process.terminate()
            sound_moudle_process.terminate()
            exit(-1)
    sound_queue.qut(9)
    while _OPEN.value:
        if _IS_ALIVE.value:
            _ENABLE.set()
            if not px4_write_process.is_alive():
                px4_write_process.start()
            if not travel_control_process.is_alive():
                travel_control_process.start()
            if not capture_process.is_alive():
                capture_process.start()
            if not inference_seg_process.is_alive():
                inference_seg_process.start()
        else:
            _ENABLE.clear()
    sound_queue.qut(6)
    inference_seg_process.join()
    capture_process.join()
    travel_control_process.join()
    px4_write_process.join()
    px4_read_process.terminate()
    sound_moudle_process.terminate()
    sound_queue.qut(5)
