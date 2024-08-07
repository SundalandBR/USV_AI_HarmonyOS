import model
import multiprocessing as mp
import time
from capture_video import capture_video
from log import logger, close_log_queue
from data_processor import DataProcessor
from mavlink_interface import MAVLinkCommunicator
from voice_broadcast import sound_moudle, sound_enum
import ctypes
import os
import configparser
import logging
import cv2


class message:
    # 1 seg  2 action direction
    def __init__(
        self,
        enum=0,
        seq=None,
        direction=None,
        action=None,
    ) -> None:
        self.enum = enum
        self.seq = seq
        self.direction = direction
        self.action = action


def px4_read(
    communicator,
    _PX4_COMMUNICATION_ENABLE,
    _IS_MISSION_ARRIVAL,
    _IS_TARGET,
    _IS_ALIVE,
    _IS_MOVEING,
    _WATER_Quality,
):
    logger.info("px4_read module")
    processor = DataProcessor()
    if communicator.connect_and_check_communication():
        logger.info("px4 communication connet")
        while True:
            _PX4_COMMUNICATION_ENABLE.value = True
            communicator.receive_and_parse_messages_from_px4(processor)
            _IS_MISSION_ARRIVAL = processor.is_mission_arrival
            _IS_TARGET.value = processor.is_target
            _IS_ALIVE.value = processor.is_alive
            _IS_MOVEING = processor.is_moving
            _WATER_Quality = processor.water_quality
    else:
        logger.error(
            "Exiting the program because communication with PX4 could not be established."
        )
        _PX4_COMMUNICATION_ENABLE = False


def water_quality(_ENABLE, seq, event, px4_write_event, message_queue):
    mes = message(seq=None, action=0, direction=-1, enum=2)
    message_queue.qut(mes)
    px4_write_event.set()
    # 采集
    logger.info("water quality work")
    mes = message(seq=seq, enum=1)


def px4_write(communicator, _ENABLE, message_queue):
    # action 0悬停 1前进 2后退
    # direction 0左转 1右转 other不做操作
    # enum 1任务 2行动
    while _ENABLE.is_set():
        if not message_queue.empty():
            message = message_queue.get()
            message_enum = message.enum
            seq = message.seq
            action = message.action
            direction = message.direction
            if message_enum == 1:
                communicator.send_mission_messages_px4(seq)
            elif message_enum == 2:
                communicator.send_move_messages_to_px4(action, direction)


def Inference_seg(frame_queue, inference_message_queue, _ENABLE):
    config = configparser.ConfigParser()
    config.read("./config.ini")
    model_path = config.get("MODEL", "model")
    seg = config.getboolean("MODEL", "seg")
    # 0 left,1 right,2 up,3 down
    inference_model = model.model(model_path=model_path, seg=seg)
    while _ENABLE.is_set():
        ctrl = [0, 0, 0, 0]
        if not frame_queue.empty():
            imgs = frame_queue.get()
            if imgs:
                for img in imgs:
                    t = time.time()
                    result = inference_model.inference_seg_om(img=img)
                    cv2.imwrite("result.jpg", result.ret_img)
                    inference_message_queue.put(result)
        else:
            logger.debug("Inference : frame_queue is empty!!")
            time.sleep(0.1)
    logger.debug("Inference : Inference process exit")


def queue_clear(process, queue):
    while process.is_alive():
        if not queue.empty():
            queue.get()


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
            sound_queue.put(sound_enum._WaterQuality)
            wmeg = message(enum=2, action=0, direction=-1)
            water_quality()
            px4_write_message_queue.qut(wmeg)
        elif not inference_message_queue.empty():
            ctrl = [0, 0, 0, 0]
            result = inference_message_queue.get()
            preds = result.pred
            if preds.shape[0]:
                for pred in preds:
                    shape = result.orig_shape
                    label = pred[5]
                    boxs = pred[:4]
                    if label == 0:
                        sound_queue.put(sound_enum._FindObstacle)
                        logger.debug("Inference : obstacle!")
                        mid_w = (boxs[2] - boxs[0]) / 2
                        orig_mid_w = shape[1] / 2
                        if mid_w < orig_mid_w:
                            # turn right
                            ctrl[1] += 1
                        if mid_w >= orig_mid_w:
                            # turn left
                            ctrl[0] += 1
                    if label == 1:
                        logger.debug("Inference : river!")
                        orig_mid_h = shape[0] / 2
                        h = (boxs[3] - boxs[1]) / 2
                        if h > orig_mid_h:
                            ctrl[2] += 1
                        if h <= orig_mid_h:
                            ctrl[3] += 1
                    if ctrl[0] >= ctrl[1]:
                        direction = 0
                    else:
                        direction = 1
                    if ctrl[2] >= ctrl[3]:
                        action = 1
                    else:
                        action = 2
                    wmeg = message(enum=2, action=action, direction=direction)
                    px4_write_message_queue.put(wmeg)
            else:
                logger.debug("Inference : No obstacles and river!!!!!")


if __name__ == "__main__":
    # init
    process_list = []
    # communicator = MAVLinkCommunicator()
    communicator = None
    _PX4_COMMUNICATION_ENABLE = mp.Manager().Value(
        ctypes.c_bool, False
    )  # px4是否正常通讯
    _OPEN = mp.Manager().Value(ctypes.c_bool, True)  # 开关机
    _IS_MISSION_ARRIVAL = mp.Manager().Value(ctypes.c_bool, False)  # 任务目标点是否到达
    _IS_TARGET = mp.Manager().Value(ctypes.c_bool, False)  # 是否有航点
    _IS_ALIVE = mp.Manager().Value(ctypes.c_bool, False)  # 是否武装模块
    _IS_MOVEING = mp.Manager().Value(ctypes.c_bool, False)  # 是否在移动中
    _WATER_QUALITY = mp.Manager().Value(ctypes.c_bool, False)  # 水质检测任务
    sound_queue = mp.Queue()  # 播报队列
    frame_queue = mp.Queue()  # 摄像头-推理 图片队列
    px4_write_message_queue = mp.Queue()  # 航控-px4写 message类队列
    inference_message_queue = mp.Queue()  # 推理-航控 避障信息队列
    _ENABLE = mp.Event()  # 摄像头-推理-航控-px4写-语音 模块启动-执行信号

    # 播报进程
    sound_moudle_process = mp.Process(target=sound_moudle, args=(_ENABLE, sound_queue))
    process_list.append(sound_moudle_process)

    # PX4读进程
    px4_read_process = mp.Process(
        target=px4_read,
        args=(
            communicator,
            _PX4_COMMUNICATION_ENABLE,
            _IS_MISSION_ARRIVAL,
            _IS_TARGET,
            _IS_ALIVE,
            _IS_MOVEING,
            _WATER_QUALITY,
        ),
    )
    process_list.append(px4_read_process)

    # PX4写进程
    px4_write_process = mp.Process(
        target=px4_write, args=(communicator, _ENABLE, px4_write_message_queue)
    )
    process_list.append(px4_write_process)

    # 摄像头进程
    capture_process = mp.Process(target=capture_video, args=(frame_queue, _ENABLE))
    process_list.append(capture_process)

    # 推理进程
    inference_seg_process = mp.Process(
        target=Inference_seg,
        args=(frame_queue, inference_message_queue, _ENABLE),
    )
    process_list.append(inference_seg_process)

    # 航控进程
    travel_control_process = mp.Process(
        target=travel_control,
        args=(
            _ENABLE,
            px4_write_message_queue,
            _IS_MISSION_ARRIVAL,
            _IS_TARGET,
            _IS_ALIVE,
            _IS_MOVEING,
            _WATER_QUALITY,
            inference_message_queue,
            sound_queue,
        ),
    )
    process_list.append(travel_control_process)

    # 初始化完成
    # 开始监听PX4
    px4_read_process.start()
    sound_moudle_process.start()
    start = time.time()
    if communicator is not None:
        while not _PX4_COMMUNICATION_ENABLE.value:
            logger.debug(f"_PX4_COMMUNICATION_ENABLE {_PX4_COMMUNICATION_ENABLE.value}")
            if time.time() - start > 30:
                logger.debug("_PX4_COMMUNICATION_ENABLE ERROR!!!")
                px4_read_process.terminate()
                sound_moudle_process.terminate()
                sound_queue.put(sound_enum._StartUp_error)
                exit(-1)
    else:
        _OPEN.value = True
        _IS_ALIVE.value = True
        time.sleep(3)

    # 无人艇启动 各个模块启动
    sound_queue.put(sound_enum._StartUp)
    cnt = 0  # debug
    while _OPEN.value:
        if _IS_ALIVE.value:
            _ENABLE.set()
            for process in process_list:
                if not process.is_alive():
                    try:
                        process.start()
                        logger.info(f"{process.name} start")
                        logger.debug(f"{process.name} start")
                    except:
                        logger.error(f"{process.name} start error")
            time.sleep(10)
            cnt += 1
        else:
            _ENABLE.clear()
        if cnt == 2:
            _ENABLE.clear()  # debug
            _OPEN.value = False
            # 2分钟自动关机

    # 无人机关机 结束各个进程
    sound_queue.put(sound_enum._ShutDowning)
    for process in process_list:
        process.join(5)
        process.terminate()
    close_log_queue()
    logger.debug("over")
    sound_queue.put(sound_enum._ShutDown)
