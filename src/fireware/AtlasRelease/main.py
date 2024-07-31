import model
import multiprocessing as mp
import time
from capture_video1 import capture_video
import logging
from data_processor import DataProcessor
from mavlink_interface import MAVLinkCommunicator
import socket
import json

def TravelDateHttp(results,HOST,PORT):
    d = dict()
    d['123'] = 123
    d['222'] = 123
    j = json.dumps(d)
    j = j.encode()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(j)
        

def px4_read(communicator,read_queue,_LauchSign,enable):
    processor = DataProcessor()
    while(enable.is_set()):
        if communicator.connect_and_check_communication():
            communicator.receive_and_parse_messages_from_px4(processor)
            processor.re
        else:
            logging.error("Exiting the program because communication with PX4 could not be established.")

def px4_write(communicator,action,direction):
    #action 0悬停 1前进 2后退
    #direction 0左转 1右转 other不做操作
    communicator.send_messages_to_px4(action,direction)
    
def Inference_seg(frame_queue, message_queue, enable, frame_queue_event):
    # cc2inference
    # 0 left,1 right,2 up,3 down
    inference_model = model.model("seg_best.om")
    while enable.is_set():
        ctrl = [0, 0, 0, 0]
        if frame_queue_event.is_set():
            imgs = frame_queue.get()
            if frame_queue.empty():
                frame_queue_event.clear()
            for img in imgs:
                t = time.time()
                result = inference_model.inference_seg_om(img=img)
                print("Inference : Time",time.time() - t)
                preds = result.pred
                print(len(preds))
                if(len(preds)!=0):
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
                    message_queue.put(ctrl)
                else:
                    print("Inference : No obstacles and river!!!!!")
        else:
            print("Inference : frame_queue is empty!!")
            time.sleep(0.1)

    print("Inference : Inference process exit")

def queue_clear(process,queue):
    while process.is_alive():
        if not queue.empty():
            queue.get()


if __name__ == "__main__":
    
    #init 
    _LauchSign = False
    #communicator = MAVLinkCommunicator() 
    lock = mp.Lock()
    enable = mp.Event()
    frame_queue = mp.Queue()
    message_queue = mp.Queue()
    read_queue = mp.Queue()
    frame_queue_event = mp.Event()
    capture_process = mp.Process(target=capture_video, args=(frame_queue, enable, frame_queue_event))
    inference_seg_process = mp.Process(
        target=Inference_seg,
        args=(frame_queue, message_queue, enable, frame_queue_event),
    )
    #px4_read_process = mp.Process(target=px4_read,args=(communicator,read_queue,_LauchSign))
    input("main : press any bottom to launch!")
    enable.set()
    capture_process.start()
    inference_seg_process.start()
    input("main : press any bottom to exit!")
    enable.clear()
    queue_clear(capture_process,frame_queue)
    capture_process.join()
    inference_seg_process.join()
